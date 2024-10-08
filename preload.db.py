from datetime import datetime
from counter import HabitTracker
from db import initialize_database

def preload_database(db):
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

    cursor.execute('''CREATE TABLE IF NOT EXISTS counters (
                           id INTEGER PRIMARY KEY,
                           habit_id INTEGER,
                           increment_date TEXT,
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
            "2024-10-01", "2024-10-02", "2024-10-04", "2024-10-06", "2024-10-08", "2024-10-10", "2024-10-12",
            "2024-10-14", "2024-10-16", "2024-10-18", "2024-10-20", "2024-10-22", "2024-10-24", "2024-10-26",
            "2024-10-28", "2024-10-30"
        ],
        "coding": [  # New habit: coding
            "2024-10-03", "2024-10-07", "2024-10-10", "2024-10-14", "2024-10-17", "2024-10-20", "2024-10-24",
            "2024-10-27", "2024-10-30"
        ],
        "writing": [  # New habit: writing
            "2024-10-05", "2024-10-12", "2024-10-19", "2024-10-26"
        ],
        "music": [  # New habit: music
            "2024-10-02", "2024-10-09", "2024-10-16", "2024-10-23", "2024-10-30"
        ],
        # ... (rest of your habits data) ...
    }

    for habit_name, dates in habits.items():  # Changed habit_id to habit_name
        cursor.execute('SELECT id FROM habits WHERE name = ?', (habit_name,))  # Use habit_name here
        habit_id = cursor.fetchone()
        if not habit_id:
            habit = HabitTracker(habit_name, f"{habit_name} habit",
                                 "Daily" if habit_name != "laundry" else "Weekly")  # Use habit_name here
            habit.save_to_database(db)  # Changed habit.store(db) to habit.save_to_database(db)
            cursor.execute('SELECT id FROM habits WHERE name = ?', (habit_name,))  # Use habit_name here
            habit_id = cursor.fetchone()[0]
        else:
            habit_id = habit_id[0]

        for date in dates:
            current_time = datetime.strptime(date, "%Y-%m-%d")
            cursor.execute('''INSERT INTO counters (habit_id, increment_date)
                                      VALUES (?, ?)''', (habit_id, current_time.strftime("%Y-%m-%d %H:%M:%S")))
            db.commit()

    if __name__ == "__main__":
        db = initialize_database()
        preload_database(db)
        print("Sample data loaded successfully!")
