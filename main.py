#####################################
# Miguel Angel Gutierrez Serrano    #
# ID: 101449899                     #
# Comp 2152                         #
#                                   #
#                                   #
#####################################


from datetime import datetime

class InvalidDateError(Exception):
    pass

def parse_date(date_str):
    return datetime.strptime(date_str, '%Y-%m-%d')

def get_valid_month():
    while True:
        try:
            month = int(input("Enter the month number (1-12): "))
            if month < 1 or month > 12:
                raise ValueError("Enter a valid month number (1-12).")
            return month
        except ValueError as e:
            print(e)

class Expense:
    def __init__(self, amount, category, date):
        self.amount = amount
        self.category = category
        self.date = date

class ExpenseTracker:
    def __init__(self):
        self.expenses = []

    def add_expense(self, expense):
        self.expenses.append(expense)

    def calculate_total_expenses(self, month):
        total_expenses = 0
        category_expenses = {}  # Dictionary to store expenses by category
        for expense in self.expenses:
            if expense.date.month == month:
                total_expenses += expense.amount
                # Add expense to the corresponding category
                if expense.category not in category_expenses:
                    category_expenses[expense.category] = expense.amount
                else:
                    category_expenses[expense.category] += expense.amount
        return total_expenses, category_expenses

    def detailed_report(self, month):
        categories = set(expense.category for expense in self.expenses)
        print(f"Detailed expense report for month {month}:")
        for category in categories:
            total_category_expenses = sum(expense.amount for expense in self.expenses if
                                          expense.category == category and expense.date.month == month)
            print(f"{category}: {total_category_expenses}")

    def calculate_annual_average_expenses(self):
        annual_expenses = {}
        for expense in self.expenses:
            if expense.category not in annual_expenses:
                annual_expenses[expense.category] = [expense.amount]
            else:
                annual_expenses[expense.category].append(expense.amount)
        annual_average_expenses = {category: sum(expenses) / len(expenses) for category, expenses in
                                   annual_expenses.items()}
        return annual_average_expenses

    def save_to_file(self, filename):
        with open(filename, 'w') as file:
            for expense in self.expenses:
                formatted_date = expense.date.strftime('%Y-%m-%d')  # Format the date as YYYY-MM-DD
                file.write(f"{formatted_date},{expense.category},{expense.amount}\n")


def main():
    tracker = ExpenseTracker()

    while True:
        print("\nMenu:")
        print("1. Add expense")
        print("2. View monthly report")
        print("3. Save and exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            try:
                amount = float(input("Enter the expense amount: "))
                category = input("Enter the expense category: ")
                date_str = input("Enter the date (YYYY-MM-DD): ")
                date = parse_date(date_str)
                expense = Expense(amount, category, date)
                tracker.add_expense(expense)
                print("Expense added successfully.")
            except ValueError:
                print("Error: Please enter a valid amount and date in YYYY-MM-DD format!")
            except InvalidDateError:
                print("Error: Please enter a valid date!")

        elif choice == "2":
            month = get_valid_month()
            total_expenses, category_expenses = tracker.calculate_total_expenses(month)
            print(f"\nMonthly report for month {month}:")
            print(f"Total expenses: {total_expenses}")

            # Display expenses by category
            print("Expenses by category:")
            for category, amount in category_expenses.items():
                print(f"{category}: {amount}")

            # Detailed report
            tracker.detailed_report(month)

            # Comparison with annual average
            annual_average_expenses = tracker.calculate_annual_average_expenses()
            total_annual_expenses = sum(annual_average_expenses.values())
            print(f"\nAnnual average expenses: {total_annual_expenses:.2f}")
            if total_expenses < total_annual_expenses:
                print("Your expenses this month are lower than the annual average!")
            elif total_expenses > total_annual_expenses:
                print("Your expenses this month are higher than the annual average!")
            else:
                print("Your expenses this month are equal to the annual average.")

            # Percentage of expenses by category
            print(f"\nPercentage of expenses for each category:")
            for category, amount in category_expenses.items():
                percentage = (amount / total_expenses) * 100
                print(f"{category}: {percentage:.2f}%")

        elif choice == "3":
            filename = input("Enter the filename to save the data: ")
            try:
                tracker.save_to_file(filename)
                print(f"Data saved to {filename} successfully.")
            except Exception as e:
                print(f"Error saving data: {e}")
            break

        else:
            print("Invalid option. Please enter again.")

if __name__ == "__main__":
    main()
