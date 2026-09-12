from datetime import datetime


def validate_transaction(transaction):
    errors = []

    # Validate date
    try:
        datetime.strptime(transaction["date"], "%Y-%m-%d")
    except (ValueError, TypeError):
        errors.append("Invalid date")

    # Validate description
    if not transaction["description"] or not transaction["description"].strip():
        errors.append("Missing description")

    # Validate amount
    try:
        amount = float(transaction["amount"])

        if amount < 0:
            errors.append("Amount cannot be negative")

    except (ValueError, TypeError):
        errors.append("Invalid amount")

    # Validate type
    if transaction["type"].lower() not in ["income", "expense"]:
        errors.append("Invalid transaction type")

    return errors