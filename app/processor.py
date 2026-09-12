import csv

from app.cleaner import clean_transaction
from app.validator import validate_transaction


def process_transactions(file_path):
    valid_transactions = []
    invalid_transactions = []
    seen_ids = set()

    with open(file_path, "r", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        for transaction in reader:
            cleaned = clean_transaction(transaction)

            transaction_id = cleaned["id"]

            # Check for duplicate transaction ID
            if transaction_id in seen_ids:
                invalid_transactions.append({
                    "transaction": cleaned,
                    "errors": ["Duplicate transaction ID"]
                })
                continue

            seen_ids.add(transaction_id)

            # Validate the cleaned transaction
            errors = validate_transaction(cleaned)

            if errors:
                invalid_transactions.append({
                    "transaction": cleaned,
                    "errors": errors
                })
            else:
                valid_transactions.append(cleaned)

    return valid_transactions, invalid_transactions