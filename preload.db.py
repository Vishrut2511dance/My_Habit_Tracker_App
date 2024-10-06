from datetime import datetime

from counter import HabitTracker
from db import initialize_database

def preload_db ():
    """
    Preloads the database with predefined habits and their respective increment dates.
    """
    cursor = db.cursor()

    # Create tables if they do not exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS habits (
                        id INTEGER PRIMARY KEY,
                        name TEXT UNIQUE NOT NULL,
                        description TEXT,
                        periodicity TEXT NOT NULL,
                        creation_date TEXT
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS progress_log (
                        id INTEGER PRIMARY KEY,
                        habit_id INTEGER,
                        tracked_at TEXT,
                        FOREIGN KEY (habit_id) REFERENCES habits (id)
                    )''')
    db.commit()

    # Updated dates for October 2024
    habits = {
        "study": [
            "2024-10-01", "2024-10-02", "2024-10-03", "2024-10-04", "2024-10-05", "2024-10-06", "2024-10-07",
            "2024-10-08", "2024-10-09", "2024-10-10", "2024-10-11", "2024-10-12", "2024-10-13", "2024-10-14",
            "2024-10-15", "2024-10-16", "2024-10-17", "2024-10-18", "2024-10-19", "2024-10-20", "2024-10-21",
            "2024-10-22", "2024-10-23", "2024-10-24", "2024-10-25", "2024-10-26", "2024-10-27", "2024-10-28",
            "2024-10-29", "2024-10-30", "2024-10-31"
        ],
        "read": [
            "2024-10-01", "2024-10-02", "2024-10-03", "2024-10-05", "2024-10-06", "2024-10-07", "2024-10-08",
            "2024-10-09", "2024-10-10", "2024-10-11", "2024-10-12", "2024-10-14", "2024-10-15", "2024-10-16",
            "2024-10-17", "2024-10-18", "2024-10-19", "2024-10-20", "2024-10-21", "2024-10-22", "2024-10-23",
            "2024-10-25", "2024-10-26", "2024-10-27", "2024-10-28", "2024-10-29", "2024-10-30", "2024-10-31"
        ],
        "gaming": [
            "2024-10-01", "2024-10-02", "2024-10-03", "2024-10-05", "2024-10-06", "2024-10-21", "2024-10-24",
            "2024-10-30"
        ],
        "sport": [
            "2024-10-01", "2024-10-09", "2024-10-16", "2024-10-23", "2024-10-30"
        ],
        "laundry": [
            "2024-10-01", "2024-10-31"
        ]
    }

    for habit_name, dates in habits.items():
        habit = HabitTracker(name=habit_name, description=f"{habit_name} habit", periodicity="Daily" if habit_name != "laundry" else "Weekly")
        habit.save_to_database(db)

        for date_str in dates:
            progress_date = datetime.strptime(date_str, "%Y-%m-%d")
            habit.log_progress(db, progress_date)

if __name__ == "__main__":
    db = initialize_database()
    preload_db()  # Pass the database connection to the function
    print("Sample data loaded successfully!")