def calculate_summary(transactions):
    total_income = 0
    total_expenses = 0

    for transaction in transactions:
        amount = transaction["amount"]

        if transaction["type"] == "income":
            total_income += amount

        elif transaction["type"] == "expense":
            total_expenses += amount

    balance = total_income - total_expenses

    return {
        "totalIncome": total_income,
        "totalExpenses": total_expenses,
        "balance": balance,
    }


def calculate_expenses_by_category(transactions):
    expenses_by_category = {}

    for transaction in transactions:
        if transaction["type"] == "expense":
            category = transaction["category"]
            amount = transaction["amount"]

            if category not in expenses_by_category:
                expenses_by_category[category] = 0

            expenses_by_category[category] += amount

    return expenses_by_category


def generate_report(valid_transactions, invalid_transactions):
    summary = calculate_summary(valid_transactions)

    expenses_by_category = calculate_expenses_by_category(valid_transactions)

    return {
        "summary": summary,
        "expensesByCategory": expenses_by_category,
        "invalidTransactions": invalid_transactions,
        "transactionsProcessed": len(valid_transactions),
    }