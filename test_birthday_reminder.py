import unittest
from datetime import date
from tempfile import TemporaryDirectory
from pathlib import Path

from models import Birthday, ConsoleNotifier
from reminder_system import BirthdayReminderSystem, ReminderManager


class TestBirthdayReminder(unittest.TestCase):
    def test_add_user_and_birthday(self):
        notifier = ConsoleNotifier()
        system = BirthdayReminderSystem(notifier)

        system.add_birthday("anna", "Jonas", "2000-05-10")

        user = system.find_user("anna")

        self.assertIsNotNone(user)
        self.assertEqual(len(user.get_birthdays()), 1)
        self.assertEqual(user.get_birthdays()[0].get_person_name(), "Jonas")

    def test_invalid_date_is_rejected(self):
        notifier = ConsoleNotifier()
        system = BirthdayReminderSystem(notifier)

        added = system.add_birthday("anna", "Jonas", "10-05-2000")

        self.assertFalse(added)
        self.assertEqual(system.get_birthdays_for_user("anna"), [])

    def test_duplicate_birthday_is_rejected(self):
        notifier = ConsoleNotifier()
        system = BirthdayReminderSystem(notifier)

        self.assertTrue(system.add_birthday("anna", "Jonas", "2000-05-10"))
        self.assertFalse(system.add_birthday("anna", "jonas", "2001-06-11"))

        user = system.find_user("anna")
        self.assertEqual(len(user.get_birthdays()), 1)

    def test_remove_birthday(self):
        notifier = ConsoleNotifier()
        system = BirthdayReminderSystem(notifier)

        system.add_birthday("anna", "Jonas", "2000-05-10")
        removed = system.remove_birthday("anna", "Jonas")

        user = system.find_user("anna")
        self.assertTrue(removed)
        self.assertEqual(len(user.get_birthdays()), 0)

    def test_birthday_matches_today_by_month_and_day(self):
        birthday = Birthday("Jonas", "2000-05-10")

        self.assertTrue(birthday.is_today(date(2026, 5, 10)))
        self.assertFalse(birthday.is_today(date(2026, 5, 11)))

    def test_build_today_messages(self):
        notifier = ConsoleNotifier()
        system = BirthdayReminderSystem(notifier)
        system.add_birthday("anna", "Jonas", "2000-05-10")
        system.add_birthday("anna", "Ieva", "2001-05-11")

        messages = system.build_today_messages("anna", date(2026, 5, 10))

        self.assertEqual(messages, ["Today is Jonas's birthday!"])

    def test_get_users(self):
        notifier = ConsoleNotifier()
        system = BirthdayReminderSystem(notifier)
        system.add_birthday("anna", "Jonas", "2000-05-10")
        system.add_birthday("petras", "Ieva", "2001-05-11")

        users = system.get_users()

        self.assertEqual(len(users), 2)

    def test_save_and_load_file(self):
        notifier = ConsoleNotifier()
        project_directory = Path(__file__).parent

        with TemporaryDirectory(dir=project_directory) as temporary_directory:
            file_name = Path(temporary_directory) / "birthdays.json"
            system = BirthdayReminderSystem(notifier, file_name)
            system.add_birthday("anna", "Jonas", "2000-05-10")
            system.save_to_file()

            loaded_system = BirthdayReminderSystem(notifier, file_name)
            loaded_system.load_from_file()

            user = loaded_system.find_user("anna")
            self.assertIsNotNone(user)
            self.assertEqual(len(user.get_birthdays()), 1)
            self.assertEqual(
                user.get_birthdays()[0].get_birth_date(),
                "2000-05-10"
            )

    def test_singleton_manager(self):
        manager1 = ReminderManager()
        manager2 = ReminderManager()

        self.assertIs(manager1, manager2)


if __name__ == "__main__":
    unittest.main()
