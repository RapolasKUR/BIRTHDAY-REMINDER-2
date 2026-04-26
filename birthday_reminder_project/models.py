from abc import ABC, abstractmethod
from datetime import date, datetime


class Birthday:
    """Represents one saved birthday."""

    def __init__(self, person_name, birth_date):
        self._person_name = self._validate_name(person_name)
        self._birth_date = self._validate_date(birth_date)

    @staticmethod
    def _validate_name(person_name):
        person_name = person_name.strip()
        if not person_name:
            raise ValueError("Person name cannot be empty.")
        return person_name

    @staticmethod
    def _validate_date(birth_date):
        try:
            datetime.strptime(birth_date, "%Y-%m-%d")
        except ValueError as exc:
            raise ValueError("Birth date must use YYYY-MM-DD format.") from exc
        return birth_date

    def get_person_name(self):
        return self._person_name

    def get_birth_date(self):
        return self._birth_date

    def to_dict(self):
        return {
            "person_name": self._person_name,
            "birth_date": self._birth_date
        }

    def is_today(self, today=None):
        if today is None:
            today = date.today()

        today_text = today.strftime("%m-%d")
        birthday_day = self._birth_date[5:]
        return today_text == birthday_day

    def __str__(self):
        return f"{self._person_name} - {self._birth_date}"


class User:
    def __init__(self, username):
        self._username = self._validate_username(username)
        self._birthdays = []

    @staticmethod
    def _validate_username(username):
        username = username.strip()
        if not username:
            raise ValueError("Username cannot be empty.")
        return username

    def get_username(self):
        return self._username

    def add_birthday(self, birthday):
        if self.find_birthday(birthday.get_person_name()) is not None:
            raise ValueError("Birthday for this person already exists.")
        self._birthdays.append(birthday)

    def find_birthday(self, person_name):
        for birthday in self._birthdays:
            if birthday.get_person_name().lower() == person_name.lower():
                return birthday
        return None

    def remove_birthday(self, person_name):
        birthday = self.find_birthday(person_name)
        if birthday is not None:
            self._birthdays.remove(birthday)
            return True
        return False

    def get_birthdays(self):
        return list(self._birthdays)

    def to_dict(self):
        return {
            "username": self._username,
            "birthdays": [
                birthday.to_dict()
                for birthday in self._birthdays
            ]
        }


class Notifier(ABC):
    @abstractmethod
    def send_message(self, message):
        pass


class ConsoleNotifier(Notifier):
    def send_message(self, message):
        print("Reminder:", message)


class FriendlyNotifier(Notifier):
    def send_message(self, message):
        print("Hey! Don't forget!", message)
