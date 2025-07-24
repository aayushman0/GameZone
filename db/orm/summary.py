from sqlalchemy import func
from db.models import session, Income, Expense
from datetime import date


def total_expense(from_: date | None = None, to_: date | None = None) -> float:
    expenses = session.query(Expense)
    if from_:
        expenses = expenses.filter(func.DATE(Expense.date) >= from_)
    if to_:
        expenses = expenses.filter(func.DATE(Expense.date) <= to_)
    total = sum(expense.cost for expense in expenses)
    return total


def total_income(from_: date | None = None, to_: date | None = None) -> float:
    incomes = session.query(Income)
    if from_:
        incomes = incomes.filter(func.DATE(Income.date) >= from_)
    if to_:
        incomes = incomes.filter(func.DATE(Income.date) <= to_)
    total = sum(income.price for income in incomes)
    return total
