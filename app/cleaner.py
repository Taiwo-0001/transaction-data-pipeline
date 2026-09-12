def clean_amount(amount):
    """
    Convert a messy amount string into a number.
    """

    if amount is None:
        return None

    amount = amount.strip()

    # Remove currency symbol and commas
    amount = amount.replace("₦", "")
    amount = amount.replace(",", "")

    try:
        return float(amount)
    except ValueError:
        return None


from datetime import datetime


def clean_date(date):
    if date is None:
        return None

    date = date.strip()

    formats = [
        "%Y-%m-%d",
        "%d/%m/%Y",
    ]

    for date_format in formats:
        try:
            parsed_date = datetime.strptime(date, date_format)
            return parsed_date.strftime("%Y-%m-%d")
        except ValueError:
            continue

    return None


def clean_transaction(transaction):
    cleaned = transaction.copy()

    # Clean amount
    cleaned["amount"] = clean_amount(transaction["amount"])

    # Clean date
    cleaned["date"] = clean_date(transaction["date"])

    # Normalize transaction type
    if transaction["type"]:
        cleaned["type"] = transaction["type"].strip().lower()

    # Handle missing category
    if not transaction["category"] or not transaction["category"].strip():
        cleaned["category"] = "Uncategorized"
    else:
        cleaned["category"] = transaction["category"].strip()

    # Clean description
    if transaction["description"]:
        cleaned["description"] = transaction["description"].strip()

    return cleaned