from app.analytics import (
    calculate_summary,
    calculate_expenses_by_category,
)
from fastapi import FastAPI
from app.processor import process_transactions
from app.analytics import calculate_summary
from fastapi import FastAPI, HTTPException
app = FastAPI(title="Transaction Data Pipeline")


@app.get("/")
def root():
    return {"message": "Transaction Data Pipeline API is running"}

@app.get("/transactions")
def get_transactions():
    valid_transactions, invalid_transactions = process_transactions(
        "data/messy_transactions.csv"
    )

    return valid_transactions
@app.get("/transactions/{transaction_id}")
def get_transaction(transaction_id: str):
    valid_transactions, invalid_transactions = process_transactions(
        "data/messy_transactions.csv"
    )

    for transaction in valid_transactions:
        if transaction["id"] == transaction_id:
            return transaction

    raise HTTPException(
        status_code=404,
        detail="Transaction not found"
    )
@app.get("/analytics/summary")
def get_summary():
    valid_transactions, invalid_transactions = process_transactions(
        "data/messy_transactions.csv"
    )

    summary = calculate_summary(valid_transactions)

    summary["transactionsProcessed"] = len(valid_transactions)

    return summary
@app.get("/analytics/categories")
def get_categories():
    valid_transactions, invalid_transactions = process_transactions(
        "data/messy_transactions.csv"
    )

    return calculate_expenses_by_category(valid_transactions)