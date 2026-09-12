from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
from app.cleaner import clean_amount, clean_date, clean_transaction
from app.analytics import (
    calculate_summary,
    calculate_expenses_by_category,
    generate_report,
)

def test_clean_naira_amount():
    assert clean_amount("₦25,000") == 25000


def test_clean_comma_amount():
    assert clean_amount("4,500") == 4500


def test_clean_regular_amount():
    assert clean_amount("85000") == 85000


def test_invalid_amount():
    assert clean_amount("abc") is None


def test_clean_iso_date():
    assert clean_date("2026-09-01") == "2026-09-01"


def test_clean_slash_date():
    assert clean_date("01/09/2026") == "2026-09-01"


def test_invalid_date():
    assert clean_date("invalid-date") is None


def test_clean_transaction():
    transaction = {
        "id": "txn_101",
        "date": "2026-09-01",
        "description": "Instagram Sale",
        "amount": "₦25,000",
        "type": "income",
        "category": "Sales",
    }

    cleaned = clean_transaction(transaction)

    assert cleaned["amount"] == 25000
    assert cleaned["date"] == "2026-09-01"
    assert cleaned["type"] == "income"
    assert cleaned["category"] == "Sales"


def test_missing_category_becomes_uncategorized():
    transaction = {
        "id": "txn_108",
        "date": "2026-09-08",
        "description": "Consulting Payment",
        "amount": "65000",
        "type": "income",
        "category": "",
    }

    cleaned = clean_transaction(transaction)

    assert cleaned["category"] == "Uncategorized"


def test_income_is_normalized():
    transaction = {
        "id": "txn_106",
        "date": "2026-09-06",
        "description": "Online Store Sale",
        "amount": "45000",
        "type": "Income",
        "category": "Sales",
    }

    cleaned = clean_transaction(transaction)

    assert cleaned["type"] == "income"

  


def test_calculate_summary():
    transactions = [
        {
            "id": "txn_1",
            "amount": 25000,
            "type": "income",
        },
        {
            "id": "txn_2",
            "amount": 5000,
            "type": "expense",
        },
        {
            "id": "txn_3",
            "amount": 85000,
            "type": "income",
        },
    ]

    summary = calculate_summary(transactions)

    assert summary["totalIncome"] == 110000
    assert summary["totalExpenses"] == 5000
    assert summary["balance"] == 105000


def test_calculate_expenses_by_category():
    transactions = [
        {
            "amount": 5000,
            "type": "expense",
            "category": "Marketing",
        },
        {
            "amount": 4500,
            "type": "expense",
            "category": "Transport",
        },
        {
            "amount": 3000,
            "type": "expense",
            "category": "Marketing",
        },
        {
            "amount": 25000,
            "type": "income",
            "category": "Sales",
        },
    ]

    result = calculate_expenses_by_category(transactions)

    assert result["Marketing"] == 8000
    assert result["Transport"] == 4500
    assert "Sales" not in result


def test_generate_report():
    valid_transactions = [
        {
            "id": "txn_1",
            "amount": 25000,
            "type": "income",
            "category": "Sales",
        },
        {
            "id": "txn_2",
            "amount": 5000,
            "type": "expense",
            "category": "Marketing",
        },
    ]

    invalid_transactions = [
        {
            "transaction": {
                "id": "txn_3",
                "amount": None,
                "type": "income",
                "category": "Sales",
            },
            "errors": ["Invalid amount"],
        }
    ]

    report = generate_report(
        valid_transactions,
        invalid_transactions,
    )

    assert report["summary"]["totalIncome"] == 25000
    assert report["summary"]["totalExpenses"] == 5000
    assert report["summary"]["balance"] == 20000

    assert report["expensesByCategory"]["Marketing"] == 5000
    assert report["transactionsProcessed"] == 2
    assert len(report["invalidTransactions"]) == 1
def test_get_transaction():
    response = client.get("/transactions/txn_101")

    assert response.status_code == 200
    assert response.json()["id"] == "txn_101"

def test_get_transaction_not_found():
    response = client.get("/transactions/txn_999")

    assert response.status_code == 404


def test_get_summary():
    response = client.get("/analytics/summary")

    assert response.status_code == 200
    assert response.json()["totalIncome"] == 285000.0
    assert response.json()["totalExpenses"] == 9500.0


def test_get_categories():
    response = client.get("/analytics/categories")

    assert response.status_code == 200
    assert response.json()["Marketing"] == 5000.0
    assert response.json()["Transport"] == 4500.0