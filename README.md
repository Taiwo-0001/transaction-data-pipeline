To create a virtual environment, I used python -m venv venv and since I am using Windows PowerShell, I used .\venv\Scripts\Activate.

## Running the API

Start the FastAPI server with:

uvicorn app.main:app 

Once the server starts, the API can be accessed at:

http://127.0.0.1:8000

FastAPI also provides interactive API documentation at:

http://127.0.0.1:8000/docs

## Running the Tests

The project used pytest for automated testing.

Run the tests with:

python -m pytest

At the time of writing, the test suite contains 17 tests.

## Architecture
I split the project into different files so that each part of the pipeline has a specific responsibility.

The data starts from the CSV file and is processed one transaction at a time.

* app/read_csv.py is used to run the pipeline and generate a report from the CSV file.

* app/processor.py reads the CSV rows and controls the main processing flow. It sends each transaction through cleaning and validation and also checks for duplicate transaction IDs.

* app/cleaner.py handles values that can be safely normalized, such as currency symbols, commas in amounts, date formats, transaction type casing, and missing categories.

* app/validator.py checks whether a cleaned transaction is valid. It checks the date, description, amount, negative values, and transaction type.

* Transactions that pass validation are kept as valid transactions. Transactions that fail validation are stored in invalidTransactions together with the reason they were rejected.
app/analytics.py works with the valid transactions to calculate total income, total expenses, balance, and expenses by category.

* app/main.py contains the FastAPI application and exposes the processed data and analytics through the API endpoints.

* tests/test_cleaner.py contains the automated tests for the cleaning functions, analytics, and API endpoints.


## Data Validation
It separates cleaning from validation.Cleaning handles values that can be safely normalized, while validation determines whether the cleaned transaction can be accepted.

## Cleaning decisions I made
* Currency symbols and commas: I removed them and converted the amount to a number.

* Date format: I converted supported dates such as 01/09/2026 to 2026-09-01.

* Transaction type such as Income: Normalized it to lowercase (income).

* Missing category: Use Uncategorized.

* Missing description: Keep it empty during cleaning and reject it during validation.

* Invalid amount such as abc: I converted it to None during cleaning and rejected it during validation.

* Invalid date: Convert to None and reject during validation.

## Validation rules

A transaction is considered valid when:

* The date is valid.
* The description is present.
* The amount is numeric.
* The amount is not negative.
* The transaction type is either income or expense.
* The transaction ID has not already been processed.

Invalid transactions are not included in the financial calculations. Instead they are returned in the invalidTransactions section with the reason they were rejected.

* Duplicate transaction IDs are treated as invalid. The first occurrence is processed normally while subsequent occurrences with the same ID are rejected.

* Missing category does not make a transaction invalid. Instead it is normalized to Uncategorized. This allows the transaction to remain part of the valid dataset while still making the missing information visible.

* Invalid transaction types: Only income and expense are supported. Other values, such as refund, are rejected.

* Negative amounts are rejected rather than automatically converted to positive values. This avoids changing the meaning of the original transaction.

Invalid amounts: Amounts that cannot be converted to numbers such as abc, are rejected.

## Assumptions
* Dates in DD/MM/YYYY format are interpreted as day/month/year.
* The first occurrence of a duplicate transaction ID is kept and later occurrences are rejected.
* Missing categories are treated as Uncategorized.
* Invalid transactions are excluded from analytics.
* Financial values are currently represented using Python float. For a production financial system, Decimal would be preferable to avoid floating-point precision issues.

## API 
I built the API with FastAPI.



* GET /transactions:
Returns all valid transactions after cleaning and validation.

GET http://127.0.0.1:8000/transactions

Response: [ { "id": "txn_101", 
               "date": "2026-09-01", "description": "Instagram Sale", "amount": 25000.0, 
               "type": "income", 
               "category": "Sales"
                }
                 ]

* GET /transactions/{transaction_id}:

Returns a single valid transaction using its transaction ID.

GET http://127.0.0.1:8000/transactions/txn_101

If the transaction does not exist, the API returns a 404 response.

* GET /analytics/summary:

Returns the total income, total expenses, balance, and number of valid transactions processed.

GET http://127.0.0.1:8000/analytics/summary

Response:

{
  "totalIncome": 285000.0,
  "totalExpenses": 9500.0,
  "balance": 275500.0,
  "transactionsProcessed": 7
}


* GET /analytics/categories

Returns expense totals grouped by category.


GET http://127.0.0.1:8000/analytics/categories

Response:

{
  "Marketing": 5000.0,
  "Transport": 4500.0
}

* FastAPI provides interactive documentation at:

http://127.0.0.1:8000/docs
This can be used to test the endpoints directly from the browser.

## Testing

The project used pytest for automated testing.
The test suite covers:

* Amount cleaning
* Date cleaning
* Transaction normalization
* Missing categories
* Transaction type normalization
* Financial summary calculations
* Expense calculations by category
* API endpoints
* Handling transactions that are not found

The current test suite contains 17 tests, all of which pass.
17 passed

## Clean Dataset Observation
While testing the provided clean dataset, I noticed a difference between the expected totals in the assignment and the actual transaction records provided.
The supplied transactions contain the following expenses:

Marketing: 5,000
Transport: 4,500
Operations: 12,000
Utilities: 8,500

This gives total expenses of 30,000, not 30,500.

So the resulting balance is:

220,000 - 30,000 = 190,000

The test example states total expenses of 30,500 and a balance of 189,500.

I chose not to hardcode the expected values. The implementation calculates the totals directly from the transaction records so the result for the supplied clean dataset is 30,000 expenses and 190,000 balance.