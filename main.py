from reminder_system import ReminderManager
from models import ConsoleNotifier, FriendlyNotifier


def print_menu():
    print("\n=== Birthday Reminder Menu ===")
    print("1. Add birthday")
    print("2. Remove birthday")
    print("3. Show all birthdays")
    print("4. Show today's reminders")
    print("5. Save to file")
    print("6. Load from file")
    print("7. Show all users")
    print("8. Change notifier")
    print("0. Exit")


def choose_notifier():
    print("Choose notifier:")
    print("1. Console notifier")
    print("2. Friendly notifier")

    choice = input("Enter choice: ")

    if choice == "2":
        return FriendlyNotifier()

    return ConsoleNotifier()


def main():
    notifier = ConsoleNotifier()

    manager = ReminderManager()
    system = manager.get_system(notifier)

    system.load_from_file()
    print("\nProgram is ready.")
    print("Type 3 and press Enter to show all birthdays.")
    print("Type 4 and press Enter to show today's birthdays.")

    while True:
        print_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Enter username: ")
            person_name = input("Enter birthday person's name: ")
            birth_date = input("Enter birth date (YYYY-MM-DD): ")

            system.add_birthday(username, person_name, birth_date)

        elif choice == "2":
            username = input("Enter username: ")
            person_name = input("Enter name to remove: ")

            system.remove_birthday(username, person_name)

        elif choice == "3":
            system.show_all_birthdays()

        elif choice == "4":
            system.send_all_today_notifications()

        elif choice == "5":
            system.save_to_file()

        elif choice == "6":
            system.load_from_file()

        elif choice == "7":
            system.show_users()

        elif choice == "8":
            notifier = choose_notifier()
            system.set_notifier(notifier)

        elif choice == "0":
            system.save_to_file()
            print("Program ended.")
            break

        else:
            print("Wrong choice.")


if __name__ == "__main__":
    main()
