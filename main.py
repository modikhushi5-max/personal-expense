from expense_manager import ExpenseManager
from validators import (
    validate_date,
    validate_amount,
    validate_text,
    validate_category
)


manager = ExpenseManager()


def display_expenses(expenses):

    if not expenses:
        print("\nNo expenses found.")
        return

    print("\n" + "=" * 75)
    print(
        f"{'ID':<8}"
        f"{'Date':<15}"
        f"{'Category':<18}"
        f"{'Description':<20}"
        f"{'Amount':>10}"
    )
    print("=" * 75)

    for expense in expenses:

        print(
            f"{expense['expense_id']:<8}"
            f"{expense['date']:<15}"
            f"{expense['category']:<18}"
            f"{expense['description']:<20}"
            f"₹{expense['amount']:>9.2f}"
        )

    print("=" * 75)


def add_expense():

    print("\n========== ADD EXPENSE ==========")

    date = input("Enter date (DD-MM-YYYY): ")

    if not validate_date(date):
        print("Invalid date format.")
        return

    category = input(
        "Category "
        "(Food/Travel/Shopping/Education/Entertainment/Health/Other): "
    )

    if not validate_category(category):
        print("Invalid category.")
        return

    description = input("Enter description: ")

    if not validate_text(description):
        print("Description cannot be empty.")
        return

    amount = input("Enter amount: ")

    if not validate_amount(amount):
        print("Amount must be greater than 0.")
        return

    expense_id = manager.add_expense(
        date,
        category.title(),
        description,
        amount
    )

    print(f"\n✓ Expense added successfully! ID: {expense_id}")


def view_expenses():

    print("\n========== ALL EXPENSES ==========")

    expenses = manager.get_all_expenses()

    display_expenses(expenses)


def search_expense():

    keyword = input("\nEnter keyword to search: ")

    results = manager.search_expenses(keyword)

    display_expenses(results)


def filter_expense():

    category = input("\nEnter category: ")

    results = manager.filter_by_category(category)

    display_expenses(results)


def sort_expenses():

    print("\n1. Lowest to Highest")
    print("2. Highest to Lowest")

    choice = input("Enter choice: ")

    if choice == "1":

        results = manager.sort_by_amount(False)

    elif choice == "2":

        results = manager.sort_by_amount(True)

    else:

        print("Invalid choice.")
        return

    display_expenses(results)


def delete_expense():

    expense_id = input("\nEnter Expense ID to delete: ")

    success = manager.delete_expense(expense_id)

    if success:
        print("✓ Expense deleted successfully.")

    else:
        print("Expense ID not found.")


def update_expense():

    expense_id = input("\nEnter Expense ID to update: ")

    date = input("Enter new date (DD-MM-YYYY): ")

    if not validate_date(date):
        print("Invalid date.")
        return

    category = input("Enter new category: ")

    if not validate_category(category):
        print("Invalid category.")
        return

    description = input("Enter new description: ")

    if not validate_text(description):
        print("Description cannot be empty.")
        return

    amount = input("Enter new amount: ")

    if not validate_amount(amount):
        print("Invalid amount.")
        return

    success = manager.update_expense(
        expense_id,
        date,
        category.title(),
        description,
        amount
    )

    if success:
        print("✓ Expense updated successfully.")

    else:
        print("Expense ID not found.")


def show_summary():

    total, category_summary = manager.get_summary()

    print("\n========== EXPENSE SUMMARY ==========")

    print(f"\nTotal Expense: ₹{total:.2f}")

    print("\nCategory-wise Spending:")

    for category, amount in category_summary.items():

        print(f"{category:<20} ₹{amount:.2f}")


def show_menu():

    print("\n")
    print("=" * 45)
    print("      SMART EXPENSE ANALYZER")
    print("=" * 45)

    print("1. Add Expense")
    print("2. View All Expenses")
    print("3. Search Expense")
    print("4. Filter by Category")
    print("5. Sort Expenses")
    print("6. Update Expense")
    print("7. Delete Expense")
    print("8. View Summary")
    print("9. Exit")

    print("=" * 45)


def main():

    while True:

        show_menu()

        choice = input("Enter your choice: ")

        if choice == "1":
            add_expense()

        elif choice == "2":
            view_expenses()

        elif choice == "3":
            search_expense()

        elif choice == "4":
            filter_expense()

        elif choice == "5":
            sort_expenses()

        elif choice == "6":
            update_expense()

        elif choice == "7":
            delete_expense()

        elif choice == "8":
            show_summary()

        elif choice == "9":
            print("\nThank you for using Smart Expense Analyzer!")
            break

        else:
            print("\nInvalid choice. Please enter 1-9.")


if __name__ == "__main__":
    main()