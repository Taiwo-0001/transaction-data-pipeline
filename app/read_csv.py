import json

from app.processor import process_transactions
from app.analytics import generate_report


valid_transactions, invalid_transactions = process_transactions(
    "data/messy_transactions.csv"
)

report = generate_report(
    valid_transactions,
    invalid_transactions,
)

print(json.dumps(report, indent=2))