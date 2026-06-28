from decimal import Decimal, InvalidOperation


def read_required_text(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field is required.")


def read_optional_text(prompt):
    return input(prompt).strip()


def read_int(prompt, minimum=None, allow_blank=False):
    while True:
        value = input(prompt).strip()
        if allow_blank and value == "":
            return None
        try:
            number = int(value)
            if minimum is not None and number < minimum:
                print(f"Enter a number greater than or equal to {minimum}.")
                continue
            return number
        except ValueError:
            print("Enter a valid whole number.")


def read_decimal(prompt, minimum=None):
    while True:
        value = input(prompt).strip()
        try:
            number = Decimal(value)
            if minimum is not None and number < Decimal(str(minimum)):
                print(f"Enter an amount greater than or equal to {minimum}.")
                continue
            return number
        except InvalidOperation:
            print("Enter a valid amount.")


def confirm(prompt):
    answer = input(f"{prompt} (y/n): ").strip().lower()
    return answer == "y"
