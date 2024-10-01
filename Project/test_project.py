import sqlite3
from datetime import datetime, timedelta
from counter import HabitTracker
from analyse import compute_longest_streak, compute_longest_streak_overall
from db import fetch_all_habit_names, fetch_habits_by_periodicity, get_habit_tracker


def create_test_database():
    """Creates an in-memory SQLite database for testing."""
    db = sqlite3.connect(':memory:')
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE habits (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            description TEXT,
            periodicity TEXT NOT NULL,
            creation_date TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE progress_log (
            id INTEGER PRIMARY KEY,
            habit_id INTEGER,
            tracked_at TEXT,
            FOREIGN KEY (habit_id) REFERENCES habits (id)
        )
    ''')
    return db

def test_habit_creation():
    """Tests the creation of a new habit."""
    db = create_test_database()
    tracker = HabitTracker("Reading", "Read for 30 minutes", "Daily")
    tracker.save_to_database(db)

    cursor = db.cursor()
    cursor.execute("SELECT name FROM habits WHERE name = 'Reading'")
    habit = cursor.fetchone()

    assert habit is not None
    assert habit[0] == "Reading"

def test_progress_logging():
    """Tests logging progress for a habit."""
    db = create_test_database()
    tracker = HabitTracker("Coding", "Code for 1 hour", "Daily")
    tracker.save_to_database(db)
    tracker.log_progress(db)

    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM progress_log WHERE habit_id = ?", (tracker.habit_id,))
    count = cursor.fetchone()[0]
    assert count == 1

def test_progress_clearing():
    """Tests clearing all progress logs for a habit."""
    db = create_test_database()
    tracker = HabitTracker("Meditation", "Meditate for 10 minutes", "Daily")
    tracker.save_to_database(db)
    tracker.log_progress(db)
    tracker.clear_progress(db)

    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM progress_log WHERE habit_id = ?", (tracker.habit_id,))
    count = cursor.fetchone()[0]
    assert count == 0

def test_habit_deletion():
    """Tests deleting a habit and its associated progress logs."""
    db = create_test_database()
    tracker = HabitTracker("Running", "Run for 5km", "Weekly")
    tracker.save_to_database(db)
    tracker.delete_from_database(db)

    cursor = db.cursor()
    cursor.execute("SELECT * FROM habits WHERE name = 'Running'")
    habit = cursor.fetchone()
    assert habit is None

def test_streak_calculation():
    """Tests calculating the longest streak for a habit."""
    db = create_test_database()
    tracker = HabitTracker("Journaling", "Write in journal", "Daily")
    tracker.save_to_database(db)

    today = datetime.now()
    yesterday = today - timedelta(days=1)
    two_days_ago = today - timedelta(days=2)

    cursor = db.cursor()
    cursor.execute("INSERT INTO progress_log (habit_id, tracked_at) VALUES (?, ?)",
                   (tracker.habit_id, two_days_ago.strftime("%Y-%m-%d %H:%M:%S")))
    cursor.execute("INSERT INTO progress_log (habit_id, tracked_at) VALUES (?, ?)",
                   (tracker.habit_id, yesterday.strftime("%Y-%m-%d %H:%M:%S")))
    db.commit()

    streak = compute_longest_streak(db, "Journaling")
    assert streak == 2

def test_overall_longest_streak():
    """Tests calculating the longest streak across all habits."""
    db = create_test_database()

    habit1 = HabitTracker("Yoga", "Practice yoga", "Daily")
    habit1.save_to_database(db)
    habit1.log_progress(db, datetime.now() - timedelta(days=2))
    habit1.log_progress(db, datetime.now() - timedelta(days=1))

    habit2 = HabitTracker("Piano", "Play piano", "Daily")
    habit2.save_to_database(db)
    habit2.log_progress(db)

    longest_streak = compute_longest_streak_overall(db)
    assert longest_streak == 2

def test_get_habits():
    """Tests retrieving a list of all habit names."""
    db = create_test_database()
    tracker = HabitTracker("Swimming", "Swim for 30 minutes", "Weekly")
    tracker.save_to_database(db)

    habits = fetch_all_habit_names(db)
    assert "Swimming" in habits

def test_habits_by_periodicity():
    """Tests retrieving habits filtered by periodicity."""
    db = create_test_database()

    daily_habit = HabitTracker("Drink Water", "Drink 8 glasses of water", "Daily")
    daily_habit.save_to_database(db)

    weekly_habit = HabitTracker("Grocery Shopping", "Buy groceries", "Weekly")
    weekly_habit.save_to_database(db)

    daily_habits = fetch_habits_by_periodicity(db, "Daily")
    weekly_habits = fetch_habits_by_periodicity(db, "Weekly")

    assert "Drink Water" in daily_habits
    assert "Grocery Shopping" in weekly_habits

def test_get_habit_tracker():
    """Tests retrieving a HabitTracker object for a given habit name."""
    db = create_test_database()
    tracker = HabitTracker("Learning", "Learn something new", "Daily")
    tracker.save_to_database(db)

    fetched_tracker = get_habit_tracker(db, "Learning")
    assert fetched_tracker is not None
    assert fetched_tracker.name == "Learning"


if __name__ == "__main__":
    test_habit_creation()
    test_progress_logging()
    test_progress_clearing()
    test_habit_deletion()
    test_streak_calculation()
    test_overall_longest_streak()
    test_get_habits()
    test_habits_by_periodicity()
    test_get_habit_tracker()
    print("All tests passed!")