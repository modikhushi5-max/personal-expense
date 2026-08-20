from models import Expense
from storage import load_expenses, save_expenses


class ExpenseManager:

    def __init__(self):
        self.expenses = load_expenses()

    def generate_id(self):
        if not self.expenses:
            return "E001"

        numbers = []

        for expense in self.expenses:
            number = int(expense["expense_id"][1:])
            numbers.append(number)

        next_number = max(numbers) + 1

        return f"E{next_number:03d}"

    def add_expense(self, date, category, description, amount):

        expense_id = self.generate_id()

        expense = Expense(
            expense_id,
            date,
            category,
            description,
            float(amount)
        )

        self.expenses.append(expense.to_dict())

        save_expenses(self.expenses)

        return expense_id

    def get_all_expenses(self):
        return self.expenses

    def search_expenses(self, keyword):

        keyword = keyword.lower()

        results = []

        for expense in self.expenses:

            if (
                keyword in expense["description"].lower()
                or keyword in expense["category"].lower()
            ):
                results.append(expense)

        return results

    def filter_by_category(self, category):

        return [
            expense
            for expense in self.expenses
            if expense["category"].lower() == category.lower()
        ]

    def sort_by_amount(self, descending=False):

        return sorted(
            self.expenses,
            key=lambda expense: expense["amount"],
            reverse=descending
        )

    def delete_expense(self, expense_id):

        for expense in self.expenses:

            if expense["expense_id"] == expense_id:

                self.expenses.remove(expense)

                save_expenses(self.expenses)

                return True

        return False

    def update_expense(
        self,
        expense_id,
        date,
        category,
        description,
        amount
    ):

        for expense in self.expenses:

            if expense["expense_id"] == expense_id:

                expense["date"] = date
                expense["category"] = category
                expense["description"] = description
                expense["amount"] = float(amount)

                save_expenses(self.expenses)

                return True

        return False

    def get_summary(self):

        total = 0
        category_summary = {}

        for expense in self.expenses:

            amount = expense["amount"]

            total += amount

            category = expense["category"]

            if category not in category_summary:
                category_summary[category] = 0

            category_summary[category] += amount

        return total, category_summary