import base64
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from bs4 import BeautifulSoup

from app.core.config import settings
from app.services.document_intelligence import OCRService
from app.services.expense_extractor import ExpenseExtractor
from app.services.duplicate_service import DuplicateService
from app.models.expense import Expense as ExpenseModel
from datetime import datetime




class GmailService:

    SCOPES = [
        "https://www.googleapis.com/auth/gmail.readonly"
    ]

    def create_flow(self):

        return Flow.from_client_config(

            {
                "web": {

                    "client_id":
                        settings.google_client_id,

                    "client_secret":
                        settings.google_client_secret,

                    "auth_uri":
                        "https://accounts.google.com/o/oauth2/auth",

                    "token_uri":
                        "https://oauth2.googleapis.com/token"

                }
            },

            scopes=self.SCOPES,

            redirect_uri=
                settings.google_redirect_uri

        )


    def get_auth_url(self):

        self.flow = self.create_flow()

        auth_url, state = self.flow.authorization_url(

            access_type="offline",

            include_granted_scopes="true",

            prompt="consent"

        )

        return auth_url

    def exchange_code(
        self,
        code: str
    ):

        #flow = self.create_flow()
        if not hasattr(self, "flow"):
            raise Exception(
            "OAuth session expired. Please reconnect Gmail."
        )

        self.flow.fetch_token(
            code=code
        )

        #credentials = flow.credentials

        # Temporary for development
        self.credentials = self.flow.credentials
        gmail = build("gmail", "v1", credentials=self.credentials )
        profile = (
                gmail.users()
                .getProfile(userId="me")
                .execute()
            )
        self.email = profile["emailAddress"]


        return profile
    
    def sync_receipts( self,db):

        if not hasattr(self, "credentials"):

            return {
                "error": "Connect Gmail first."
            }

        gmail = build(
            "gmail",
            "v1",
            credentials=self.credentials
        )

        response = gmail.users().messages().list(
            userId="me",
            q="""
                newer_than:30d
                (receipt OR invoice OR "order summary")
            """
        ).execute()

        messages = response.get(
            "messages",
            []
        )

        ocr_service = OCRService()
        extractor = ExpenseExtractor()
        duplicate_service = DuplicateService()

        imported = 0
        duplicates = 0

        receipt_keywords = [

            "receipt",
            "invoice",
            "order total",
            "amount paid",
            "thank you for your purchase",
            "subtotal",
            "tax",
            "payment method"

        ]

        for message in messages:

            try:

                message_id = message["id"]

                msg = gmail.users().messages().get(
                    userId="me",
                    id=message_id,
                    format="full"
                ).execute()

                payload = msg["payload"]
                parts = payload.get("parts", [])

                has_pdf = False

                # ======================
                # PROCESS PDF ATTACHMENTS
                # ======================

                for part in parts:

                    filename = part.get(
                        "filename",
                        ""
                    )

                    if not filename.lower().endswith(".pdf"):
                        continue

                    has_pdf = True

                    attachment_id = part["body"].get(
                        "attachmentId"
                    )

                    if not attachment_id:
                        continue

                    attachment = (
                        gmail.users()
                        .messages()
                        .attachments()
                        .get(
                            userId="me",
                            messageId=message_id,
                            id=attachment_id
                        )
                        .execute()
                    )

                    pdf_bytes = base64.urlsafe_b64decode(
                        attachment["data"]
                    )

                    raw_text = ocr_service.extract_text(
                        pdf_bytes
                    )

                    expense = extractor.extract(
                        raw_text
                    )

                    is_duplicate = (
                        duplicate_service.check_duplicate(
                            db,
                            expense.merchant_name,
                            expense.amount,
                            expense.expense_date
                        )
                    )

                    if is_duplicate:

                        duplicates += 1
                        continue

                    expense_data = ExpenseModel(

                        merchant_name=expense.merchant_name,

                        merchant_address=
                            expense.merchant_address,

                        amount=expense.amount,

                        currency=expense.currency,

                        expense_date=
                            expense.expense_date,

                        category=expense.category,

                        tax_amount=
                            expense.tax_amount,

                        confidence=
                            expense.confidence,

                        receipt_url=filename,

                        raw_receipt_text=raw_text
                    )

                    db.add(expense_data)
                    db.commit()
                    db.refresh(expense_data)

                    imported += 1

                # ======================
                # PROCESS EMAIL BODY
                # ======================

                if has_pdf:
                    continue

                raw_text = self.extract_email_body(
                    payload
                )

                if len(raw_text.strip()) < 50:
                    continue

                if not any(
                    keyword.lower() in raw_text.lower()
                    for keyword in receipt_keywords
                ):
                    continue

                expense = extractor.extract(
                    raw_text
                )

                if not expense.amount:
                    continue

                is_duplicate = (
                    duplicate_service.check_duplicate(
                        db,
                        expense.merchant_name,
                        expense.amount,
                        expense.expense_date
                    )
                )

                if is_duplicate:

                    duplicates += 1
                    continue

                expense_data = ExpenseModel(

                    merchant_name=expense.merchant_name,

                    merchant_address=
                        expense.merchant_address,

                    amount=expense.amount,

                    currency=expense.currency,

                    expense_date=
                        expense.expense_date,

                    category=expense.category,

                    tax_amount=
                        expense.tax_amount,

                    confidence=
                        expense.confidence,

                    receipt_url="gmail-body",

                    raw_receipt_text=raw_text
                )

                db.add(expense_data)
                db.commit()
                db.refresh(expense_data)

                imported += 1

            except Exception as e:

                print(
                    f"Failed to process message: {e}"
                )

                continue

        self.last_sync = (
            datetime.now().isoformat()
        )

        self.total_imported = imported
        self.total_duplicates = duplicates

        return {

            "emails_scanned":
                len(messages),

            "imported":
                imported,

            "duplicates":
                duplicates,

            "last_sync":
                self.last_sync
        }


    def extract_email_body(
        self,
        payload
    ):

        data = payload.get(
            "body",
            {}
        ).get(
            "data"
        )

        if data:

            content = base64.urlsafe_b64decode(
                data
            ).decode(
                "utf-8",
                errors="ignore"
            )

            if payload.get("mimeType") == "text/html":

                soup = BeautifulSoup(
                    content,
                    "html.parser"
                )

                return soup.get_text(
                    separator="\n"
                )

            return content

        for part in payload.get(
            "parts",
            []
        ):

            text = self.extract_email_body(
                part
            )

            if text:
                return text

        return ""
    
    # def sync_receipts(self,db):
    #     if not hasattr(self, "credentials"):
    #         return {
    #              "error":
    #             "Connect Gmail first."
    #         }
    #     gmail = build( "gmail","v1", credentials=self.credentials)
    #     response = (
    #                 gmail.users().messages().list(
    #                 userId="me",
    #                 q="""
    #                      has:attachment
    #                     filename:pdf OR "receipt" OR "order summary" OR "invoice"
    #                     newer_than:30d
    #                 """).execute()
    #                 )
    #     messages = response.get("messages",[])

    #     ocr_service = OCRService()
    #     extractor = ExpenseExtractor()
    #     duplicate_service = DuplicateService()
        
    #     imported = 0
    #     duplicates = 0

    #     for message in messages:
    #         message_id = message["id"]
    #         msg = (
    #                 gmail.users().messages().get(
    #                     userId="me",
    #                      id=message_id
    #                 ).execute())

    #         payload = msg["payload"]

    #         parts = payload.get("parts",[])

    #         for part in parts:
    #             filename = part.get("filename","")
    #             if not filename.endswith(".pdf"):
    #                 continue

    #             attachment_id = (part["body"].get("attachmentId"))
                
    #             if not attachment_id:
    #                 continue

    #             attachment = (gmail.users()
    #                             .messages()
    #                             .attachments()
    #                             .get(
    #                                 userId="me",
    #                                 messageId=message_id,
    #                                 id=attachment_id
    #                             ).execute()
    #                         )

    #             pdf_bytes = base64.urlsafe_b64decode(attachment["data"])


    #             # YOUR EXISTING PIPELINE
    #             raw_text = (ocr_service.extract_text(pdf_bytes))

    #             expense = (extractor.extract(raw_text))
    #             is_duplicate = (duplicate_service.check_duplicate(
    #                 db,expense.merchant_name,expense.amount,expense.expense_date
    #                 ))

    #             if is_duplicate:
    #                 duplicates += 1
    #                 continue


    #             # Create Expense ORM object here
    #             # (reuse your upload endpoint code)
    #             expense_data = ExpenseModel(
    #                         merchant_name=expense.merchant_name,
    #                         merchant_address=expense.merchant_address,
    #                         amount=expense.amount,
    #                         currency=expense.currency,
    #                         expense_date=expense.expense_date,
    #                         category=expense.category,
    #                         tax_amount=expense.tax_amount,
    #                         confidence=expense.confidence,
    #                         receipt_url=filename,
    #                         raw_receipt_text=raw_text
    #                         )

    #             db.add(expense_data)
    #             db.commit()
    #             db.refresh(expense_data)
    #             imported += 1

    #     self.last_sync = datetime.now().isoformat()
    #     self.total_imported = imported
    #     self.total_duplicates = duplicates
    #     return {

    #     "emails_scanned":
    #         len(messages),

    #     "imported":
    #         imported,

    #     "duplicates":
    #         duplicates

    #     }
