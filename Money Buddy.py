INCOME_FILE = "income.txt"
SPENDING_FILE = "spending.txt"
GOAL_FILE = "goal.txt"


def load_records(file_name):
    records = []

    try:
        file = open(file_name, "r")
        lines = file.readlines()
        file.close()

        for line in lines:
            line = line.strip()
            parts = line.split(":")

            if len(parts) == 2:
                records.append([parts[0], float(parts[1])])

    except FileNotFoundError:
        file = open(file_name, "w")
        file.close()

    return records


def save_records(file_name, records):
    file = open(file_name, "w")

    for record in records:
        file.write(record[0] + ":" + str(record[1]) + "\n")

    file.close()


def calculate_total(records):
    total = 0.0

    for record in records:
        total = total + record[1]

    return total


def add_record(records, file_name, record_type):
    print("\n----- Add " + record_type + " Record -----")

    name = input(record_type + " name: ")
    name = name.strip()

    if name == "":
        print(record_type + " name cannot be empty.\n")
        return

    amount = float(input("Amount: "))

    if amount < 0:
        print("Amount cannot be negative.\n")
        return

    records.append([name, amount])
    save_records(file_name, records)

    print(record_type + " record added successfully.\n")


def delete_record(records, file_name, record_type):
    print("\n----- Delete " + record_type + " Record -----")

    if len(records) == 0:
        print("There are no " + record_type.lower() + " records to delete.\n")
        return

    number = 1

    for record in records:
        print(str(number) + ". " + record[0] + " - $" + str(round(record[1], 2)))
        number = number + 1

    delete_number = int(input("Enter the record number to delete: "))

    if delete_number >= 1 and delete_number <= len(records):
        deleted_record = records[delete_number - 1]
        del records[delete_number - 1]
        save_records(file_name, records)

        print(
            record_type + " record deleted: "
            + deleted_record[0]
            + " - $"
            + str(round(deleted_record[1], 2))
            + "\n"
        )
    else:
        print("Invalid record number.\n")


def manage_records(records, file_name, record_type):
    print(
        "\n----- Manage " + record_type + " Records -----\n"
        "1. Add " + record_type.lower() + " record\n"
        "2. Delete " + record_type.lower() + " record\n"
        "3. Back to main menu"
    )

    choice = input("Choose an option: ")
    choice = choice.strip()

    if choice == "1":
        add_record(records, file_name, record_type)
    elif choice == "2":
        delete_record(records, file_name, record_type)
    elif choice == "3":
        print("Back to main menu.\n")
    else:
        print("Invalid option. Please choose 1, 2, or 3.\n")


def view_records(records, record_type):
    print("\n----- " + record_type + " Records -----")

    if len(records) == 0:
        print("There are no " + record_type.lower() + " records yet.\n")
        return

    number = 1

    for record in records:
        print(str(number) + ". " + record[0] + " - $" + str(round(record[1], 2)))
        number = number + 1

    total = calculate_total(records)
    print("\nTotal " + record_type.lower() + ": $" + str(round(total, 2)))
    print()


def view_saving_summary(income_records, spending_records):
    print("\n----- Saving Summary -----")

    total_income = calculate_total(income_records)
    total_spending = calculate_total(spending_records)
    saved_money = total_income - total_spending

    print("Total income: $" + str(round(total_income, 2)))
    print("Total spending: $" + str(round(total_spending, 2)))
    print("Saved money: $" + str(round(saved_money, 2)))
    print()


def manage_long_term_goal():
    print(
        "\n----- Manage Long-Term Purchase Goal -----\n"
        "1. Add new goal\n"
        "2. Delete goal\n"
        "3. Back to main menu"
    )

    choice = input("Choose an option: ")
    choice = choice.strip()

    if choice == "1":
        goal_name = input("Goal item: ")
        goal_name = goal_name.strip()

        if goal_name == "":
            print("Goal item cannot be empty.\n")
            return

        goal_price = float(input("Goal price: "))

        if goal_price < 0:
            print("Goal price cannot be negative.\n")
            return

        file = open(GOAL_FILE, "a")
        file.write(goal_name + ":" + str(goal_price) + "\n")
        file.close()

        print("Long-term goal added successfully.\n")

    elif choice == "2":
        try:
            file = open(GOAL_FILE, "r")
            lines = file.readlines()
            file.close()

            if len(lines) == 0:
                print("There are no goals to delete.\n")
                return

            number = 1

            for line in lines:
                line = line.strip()
                parts = line.split(":")

                if len(parts) == 2:
                    print(str(number) + ". " + parts[0] + " - $" + parts[1])

                number = number + 1

            delete_number = int(input("Enter the goal number to delete: "))

            if delete_number >= 1 and delete_number <= len(lines):
                del lines[delete_number - 1]

                file = open(GOAL_FILE, "w")

                for line in lines:
                    file.write(line)

                file.close()

                print("Goal deleted successfully.\n")
            else:
                print("Invalid goal number.\n")

        except FileNotFoundError:
            print("There are no goals to delete.\n")

    elif choice == "3":
        print("Back to main menu.\n")

    else:
        print("Invalid option. Please choose 1, 2, or 3.\n")


def view_long_term_goal(income_records, spending_records):
    print("\n----- View Long-Term Purchase Goal -----")

    try:
        file = open(GOAL_FILE, "r")
        lines = file.readlines()
        file.close()

        if len(lines) == 0:
            print("No long-term goal has been set yet.\n")
            return

        total_income = calculate_total(income_records)
        total_spending = calculate_total(spending_records)
        saved_money = total_income - total_spending

        for line in lines:
            line = line.strip()
            parts = line.split(":")

            if len(parts) == 2:
                goal_name = parts[0]
                goal_price = float(parts[1])
                still_needed = goal_price - saved_money

                if goal_price > 0:
                    progress = saved_money / goal_price * 100
                else:
                    progress = 0

                if still_needed <= 0:
                    need_text = "You already have enough saving for this goal."
                else:
                    need_text = "You still need: $" + str(round(still_needed, 2))

                print(
                    "Goal item: " + goal_name +
                    ", Goal price: $" + str(round(goal_price, 2)) +
                    ", Progress: " + str(round(progress, 2)) + "%" +
                    ", " + need_text + "\n"
                )

        print("Current saved money: $" + str(round(saved_money, 2)) + "\n")

    except FileNotFoundError:
        print("No long-term goal has been set yet.\n")


def show_menu():
    print(
        "----- Money Buddy -----\n"
        "1. Manage income records\n"
        "2. View income records\n"
        "3. Manage spending records\n"
        "4. View spending records\n"
        "5. View saving summary\n"
        "6. Manage long-term purchase goal\n"
        "7. View long-term purchase goal\n"
        "8. Exit"
    )


def main():
    income_records = load_records(INCOME_FILE)
    spending_records = load_records(SPENDING_FILE)

    print("Welcome to Money Buddy!")
    print("This program helps you track income, spending, and saving.\n")

    running = True

    while running:
        show_menu()
        choice = input("Choose an option: ")
        choice = choice.strip()

        if choice == "1":
            manage_records(income_records, INCOME_FILE, "Income")
        elif choice == "2":
            view_records(income_records, "Income")
        elif choice == "3":
            manage_records(spending_records, SPENDING_FILE, "Spending")
        elif choice == "4":
            view_records(spending_records, "Spending")
        elif choice == "5":
            view_saving_summary(income_records, spending_records)
        elif choice == "6":
            manage_long_term_goal()
        elif choice == "7":
            view_long_term_goal(income_records, spending_records)
        elif choice == "8":
            print("\nThank you for using Money Buddy. Goodbye!")
            running = False
        else:
            print("\nInvalid option. Please choose a number from 1 to 8.\n")


if __name__ == "__main__":
    main()
