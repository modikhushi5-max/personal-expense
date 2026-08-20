from datetime import datetime


def validate_date(date):
    try:
        datetime.strptime(date, "%d-%m-%Y")
        return True
    except ValueError:
        return False


def validate_amount(amount):
    try:
        amount = float(amount)

        if amount <= 0:
            return False

        return True

    except ValueError:
        return False


def validate_text(value):
    return bool(value.strip())


def validate_category(category):
    allowed_categories = [
        "Food",
        "Travel",
        "Shopping",
        "Education",
        "Entertainment",
        "Health",
        "Other"
    ]

    return category.title() in allowed_categories