from sqlalchemy import func
from db.models import session, Income, Expense, Credit
from datetime import date


def total_expense(from_: date | None = None, to_: date | None = None) -> float:
    expenses = session.query(func.sum(Expense.cost)).filter(Expense.is_enabled.is_(True))
    if from_:
        expenses = expenses.filter(func.DATE(Expense.date) >= from_)
    if to_:
        expenses = expenses.filter(func.DATE(Expense.date) <= to_)
    total = expenses.scalar()
    return total


def total_income(from_: date | None = None, to_: date | None = None) -> float:
    incomes = session.query(func.sum(Income.price)).filter(Income.is_enabled.is_(True))
    if from_:
        incomes = incomes.filter(func.DATE(Income.date) >= from_)
    if to_:
        incomes = incomes.filter(func.DATE(Income.date) <= to_)
    total = incomes.scalar()
    return total


def remaining_credit() -> float:
    remaining_credit = session.query(func.sum(Credit.current_amount)).scalar()
    return remaining_credit


def current_capital() -> float:
    total_income = session.query(func.sum(Income.price)).filter(Income.is_enabled.is_(True)).scalar()
    total_expense = session.query(func.sum(Expense.cost)).filter(Expense.is_enabled.is_(True)).scalar()
    total_current_credit = session.query(func.sum(Credit.initial_amount)).scalar()
    paid_credit = total_current_credit - session.query(func.sum(Credit.current_amount)).scalar()
    current_amount = total_income - (total_expense - total_current_credit) - paid_credit
    return current_amount
