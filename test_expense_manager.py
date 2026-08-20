import unittest
from unittest.mock import patch

from expense_manager import ExpenseManager


class TestExpenseManager(unittest.TestCase):

    def setUp(self):
        self.test_expenses = []

        self.load_patcher = patch(
            "expense_manager.load_expenses",
            return_value=self.test_expenses
        )

        self.save_patcher = patch(
            "expense_manager.save_expenses",
            return_value=True
        )

        self.load_patcher.start()
        self.save_patcher.start()

        self.manager = ExpenseManager()

    def tearDown(self):
        self.load_patcher.stop()
        self.save_patcher.stop()

    # 1. Test adding an expense
    def test_add_expense(self):
        expense_id = self.manager.add_expense(
            "19-08-2026",
            "Food",
            "Lunch",
            200
        )

        self.assertEqual(expense_id, "E001")
        self.assertEqual(len(self.manager.expenses), 1)
        self.assertEqual(
            self.manager.expenses[0]["amount"],
            200.0
        )

    # 2. Test searching an expense
    def test_search_expense(self):
        self.manager.add_expense(
            "19-08-2026",
            "Food",
            "Pizza",
            300
        )

        results = self.manager.search_expenses("pizza")

        self.assertEqual(len(results), 1)
        self.assertEqual(
            results[0]["description"],
            "Pizza"
        )

    # 3. Test filtering by category
    def test_filter_by_category(self):
        self.manager.add_expense(
            "19-08-2026",
            "Food",
            "Lunch",
            200
        )

        self.manager.add_expense(
            "19-08-2026",
            "Travel",
            "Bus",
            50
        )

        results = self.manager.filter_by_category("food")

        self.assertEqual(len(results), 1)
        self.assertEqual(
            results[0]["category"],
            "Food"
        )

    # 4. Test sorting expenses
    def test_sort_by_amount(self):
        self.manager.add_expense(
            "19-08-2026",
            "Food",
            "Lunch",
            500
        )

        self.manager.add_expense(
            "19-08-2026",
            "Travel",
            "Bus",
            100
        )

        results = self.manager.sort_by_amount()

        self.assertEqual(
            results[0]["amount"],
            100.0
        )

        self.assertEqual(
            results[1]["amount"],
            500.0
        )

    # 5. Test updating an expense
    def test_update_expense(self):
        expense_id = self.manager.add_expense(
            "19-08-2026",
            "Food",
            "Lunch",
            200
        )

        result = self.manager.update_expense(
            expense_id,
            "20-08-2026",
            "Shopping",
            "Clothes",
            1000
        )

        self.assertTrue(result)

        updated_expense = self.manager.expenses[0]

        self.assertEqual(
            updated_expense["category"],
            "Shopping"
        )

        self.assertEqual(
            updated_expense["amount"],
            1000.0
        )

    # 6. Test deleting an expense
    def test_delete_expense(self):
        expense_id = self.manager.add_expense(
            "19-08-2026",
            "Food",
            "Lunch",
            200
        )

        result = self.manager.delete_expense(expense_id)

        self.assertTrue(result)
        self.assertEqual(len(self.manager.expenses), 0)

    # 7. Test summary
    def test_get_summary(self):
        self.manager.add_expense(
            "19-08-2026",
            "Food",
            "Lunch",
            200
        )

        self.manager.add_expense(
            "19-08-2026",
            "Food",
            "Dinner",
            300
        )

        self.manager.add_expense(
            "19-08-2026",
            "Travel",
            "Bus",
            100
        )

        total, category_summary = self.manager.get_summary()

        self.assertEqual(total, 600.0)
        self.assertEqual(
            category_summary["Food"],
            500.0
        )
        self.assertEqual(
            category_summary["Travel"],
            100.0
        )

    # 8. Test invalid expense ID for deletion
    def test_delete_invalid_expense(self):
        result = self.manager.delete_expense("E999")

        self.assertFalse(result)

    # 9. Test invalid expense ID for update
    def test_update_invalid_expense(self):
        result = self.manager.update_expense(
            "E999",
            "19-08-2026",
            "Food",
            "Lunch",
            200
        )

        self.assertFalse(result)

    # 10. Test empty expense list
    def test_empty_expenses(self):
        expenses = self.manager.get_all_expenses()

        self.assertEqual(expenses, [])


if __name__ == "__main__":
    unittest.main()