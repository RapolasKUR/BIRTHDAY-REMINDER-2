import json
from pathlib import Path

from models import Birthday, User


class BirthdayReminderSystem:
    """Central service that manages users, birthdays and persistence."""

    def __init__(self, notifier, file_name=None):
        self._users = []
        self._notifier = notifier
        if file_name is None:
            file_name = Path(__file__).with_name("birthdays.json")
        self._file_name = Path(file_name)

    def set_notifier(self, notifier):
        self._notifier = notifier
        print("Notifier changed.")

    def find_user(self, username):
        for user in self._users:
            if user.get_username().lower() == username.lower():
                return user
        return None

    def add_user_if_needed(self, username):
        user = self.find_user(username)

        if user is None:
            user = User(username)
            self._users.append(user)

        return user

    def add_birthday(self, username, person_name, birth_date):
        try:
            user = self.add_user_if_needed(username)
            birthday = Birthday(person_name, birth_date)
            user.add_birthday(birthday)
            print("Birthday added.")
            return True
        except ValueError as error:
            print(error)
            return False

    def remove_birthday(self, username, person_name):
        user = self.find_user(username)

        if user is None:
            print("User not found.")
            return False

        was_removed = user.remove_birthday(person_name)

        if was_removed:
            print("Birthday removed.")
            return True

        print("Birthday not found.")
        return False

    def get_birthdays_for_user(self, username):
        user = self.find_user(username)
        if user is None:
            return []
        return user.get_birthdays()

    def get_users(self):
        return list(self._users)

    def get_today_birthdays(self, username, today=None):
        user = self.find_user(username)
        if user is None:
            return []

        return [
            birthday
            for birthday in user.get_birthdays()
            if birthday.is_today(today)
        ]

    def build_today_messages(self, username, today=None):
        return [
            f"Today is {birthday.get_person_name()}'s birthday!"
            for birthday in self.get_today_birthdays(username, today)
        ]

    def show_all_birthdays(self):
        if len(self._users) == 0:
            print("No birthdays saved.")
            return

        found = False
        print("All saved birthdays:")
        for user in self._users:
            for birthday in user.get_birthdays():
                print(f"{user.get_username()}: {birthday}")
                found = True

        if not found:
            print("No birthdays saved.")

    def send_all_today_notifications(self):
        found = False

        for user in self._users:
            messages = self.build_today_messages(user.get_username())
            for message in messages:
                self._notifier.send_message(
                    f"{user.get_username()}: {message}"
                )
                found = True

        if not found:
            print("No birthdays today.")

    def show_birthdays(self, username):
        user = self.find_user(username)

        if user is None:
            print("User not found.")
            return

        birthdays = user.get_birthdays()

        if len(birthdays) == 0:
            print("No birthdays saved.")
            return

        print("Saved birthdays:")
        for birthday in birthdays:
            print(birthday)

    def send_today_notifications(self, username):
        if self.find_user(username) is None:
            print("User not found.")
            return

        messages = self.build_today_messages(username)
        for message in messages:
            self._notifier.send_message(message)

        if len(messages) == 0:
            print("No birthdays today.")

    def save_to_file(self):
        data = [
            user.to_dict()
            for user in self._users
        ]

        with self._file_name.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        print("Data saved to file.")

    def load_from_file(self):
        try:
            with self._file_name.open("r", encoding="utf-8") as file:
                data = json.load(file)

            self._users = []

            for user_data in data:
                user = User(user_data["username"])

                for birthday_data in user_data["birthdays"]:
                    birthday = Birthday(
                        birthday_data["person_name"],
                        birthday_data["birth_date"]
                    )
                    user.add_birthday(birthday)

                self._users.append(user)

            print("Data loaded from file.")

        except FileNotFoundError:
            print("File not found. Starting with empty data.")

        except json.JSONDecodeError:
            print("File is empty or broken. Starting with empty data.")

    def show_users(self):
        if len(self._users) == 0:
            print("No users found.")
            return

        print("Users:")
        for user in self._users:
            print(user.get_username())


class ReminderManager:
    """Singleton manager that keeps one shared reminder system instance."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ReminderManager, cls).__new__(cls)
            cls._instance._system = None
        return cls._instance

    def get_system(self, notifier, file_name=None):
        if self._system is None:
            self._system = BirthdayReminderSystem(notifier, file_name)
        return self._system
