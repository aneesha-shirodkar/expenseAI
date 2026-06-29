from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient

from app.core.config import settings


class OCRService:

    def __init__(self):

        self.client = DocumentIntelligenceClient(
            endpoint=settings.azure_doc_intelligence_endpoint,
            credential=AzureKeyCredential(
                settings.azure_doc_intelligence_key
            )
        )

    def extract_text(
        self,
        file_bytes: bytes
    ) -> str:

        poller = self.client.begin_analyze_document(
            "prebuilt-read",
            body=file_bytes
        )

        result = poller.result()

        lines = []

        for page in result.pages:
            for line in page.lines:
                lines.append(
                    line.content
                )

        return "\n".join(lines)