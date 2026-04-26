# Birthday Reminder coursework report

## Introduction

The project is a Python birthday reminder application. It lets multiple users save birthdays, remove birthdays, list saved birthdays, save and load data from a JSON file, and print birthday notifications on the birthday date.

Run the program from the project folder:

```bash
python main.py
```

Run the unit tests:

```bash
python -m unittest test_birthday_reminder.py
```

The program is used through a console menu. The user selects an option, enters a username, and then adds, removes, lists, saves, loads, or checks birthday reminders.

## Body and analysis

### Functional requirements

The application implements the Birthday Reminder topic requirements:

- Add birthdays: `BirthdayReminderSystem.add_birthday()` creates a `Birthday` object and stores it under a user.
- Remove birthdays: `BirthdayReminderSystem.remove_birthday()` removes a saved birthday by person name.
- Print reminders: `BirthdayReminderSystem.send_today_notifications()` prints reminders for birthdays matching today's month and day.
- Save birthdays to file: `BirthdayReminderSystem.save_to_file()` exports all users and birthdays to `birthdays.json`.
- Load birthdays from file: `BirthdayReminderSystem.load_from_file()` imports the saved JSON data.
- Support multiple users: `BirthdayReminderSystem` stores many `User` objects, and each `User` owns a list of birthdays.

### Object-oriented programming pillars

Encapsulation is used by keeping object data inside private-style attributes such as `_username`, `_birthdays`, `_person_name`, and `_birth_date`. Other classes use methods like `get_username()`, `get_birthdays()`, and `to_dict()` instead of directly changing internal data.

Abstraction is used through the `Notifier` abstract base class. It defines the required `send_message()` method without deciding how the message is displayed.

Inheritance is used by `ConsoleNotifier` and `FriendlyNotifier`, which both inherit from `Notifier`.

Polymorphism is used when `BirthdayReminderSystem` sends notifications through `_notifier.send_message(message)`. The system can work with any notifier object that implements the abstract method, so different notifier classes can change the notification style without changing the reminder logic.

### Design pattern

The project uses the Singleton design pattern in `ReminderManager`. The purpose of this class is to keep one shared `BirthdayReminderSystem` instance. This fits the application because the console program should work with one central birthday reminder system during runtime.

### Composition and aggregation

Composition is shown in the relationship between `User` and `Birthday`: a user contains a collection of birthday objects. Aggregation is shown in `BirthdayReminderSystem`, which manages many users and uses a notifier object that can be replaced with `set_notifier()`.

### File reading and writing

The program stores data in a JSON file named `birthdays.json`. JSON is suitable because users and birthdays are structured data. Saving uses `json.dump()`, and loading uses `json.load()`.

### Testing

Core functionality is covered with the `unittest` framework in `test_birthday_reminder.py`. Tests check adding birthdays, removing birthdays, date validation, duplicate prevention, birthday matching by date, notification message generation, file saving/loading, and the Singleton manager.

## Results

- The application successfully supports multiple users and birthday records.
- The JSON file storage makes the data available after restarting the program.
- Validation prevents empty names and incorrect date formats.
- Unit tests help confirm that the main functions work correctly.
- The main challenge was keeping the console program simple while still showing the required OOP principles clearly.

## Conclusions

The coursework produced a functional birthday reminder program using Python and object-oriented programming. It demonstrates encapsulation, abstraction, inheritance, polymorphism, composition, aggregation, a Singleton design pattern, file input/output, and unit testing. In the future, the application could be extended with a graphical interface, email notifications, or reminders several days before a birthday.
