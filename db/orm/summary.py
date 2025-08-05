from sqlalchemy import func
from db.models import session, Income, Expense, Credit
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


def remaining_credit() -> float:
    credits = session.query(Credit)
    remaining_credit = sum(credit.current_amount for credit in credits)
    return remaining_credit


def current_capital() -> float:
    incomes = session.query(Income)
    expenses = session.query(Expense)
    credits = session.query(Credit)
    total_income = sum(income.price for income in incomes)
    total_expense = sum(expense.cost for expense in expenses)
    paid_credit = sum((credit.initial_amount - credit.current_amount) for credit in credits)
    total_current_credit = sum(credit.initial_amount for credit in credits)
    current_amount = total_income - (total_expense - total_current_credit) - paid_credit
    return current_amount
