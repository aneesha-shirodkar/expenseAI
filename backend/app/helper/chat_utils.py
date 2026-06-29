import re


TIME_PHRASES = [
    "this month",
    "last month",
    "this year",
    "last year",
    "today",
    "yesterday"
]


import re


def extract_merchant_and_period(
    message: str,
) -> tuple[str | None, str | None]:

    message = message.lower()

    period = None

    if "this month" in message:
        period = "this_month"

    elif "last month" in message:
        period = "last_month"

    elif "this year" in message:
        period = "this_year"

    match = re.search(
        r"at\s+(.+?)(?:\s+this month|\s+last month|\s+this year|\?|$)",
        message
    )

    if not match:
        return None, period

    merchant = match.group(1).strip()

    return merchant.title(), period