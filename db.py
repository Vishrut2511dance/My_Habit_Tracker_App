import sqlite3
from counter import HabitTracker  # Import the HabitTracker class

def initialize_database():
    """
    Sets up the database connection and creates the necessary tables if they don't exist.

    Returns:
        sqlite3.Connection: The database connection object.
    """
    connection = sqlite3.connect('habits.db')  # Using a different database name
    cursor = connection.cursor()

    # Create habits table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            name TEXT NOT NULL,
            description TEXT,
            periodicity TEXT NOT NULL,
            creation_date TEXT NOT NULL
        )
    ''')

    # Create progress_log table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS progress_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER,
            tracked_at TEXT NOT NULL,
            FOREIGN KEY(habit_id) REFERENCES habits(id)
        )
    ''')

    connection.commit()
    return connection

def fetch_all_habit_names(db):
    """
    Retrieves the names of all habits stored in the database.

    Args:
        db: The database connection object.

    Returns:
        list: A list of habit names.
    """
    cursor = db.cursor()
    cursor.execute('SELECT name FROM habits')
    return [row[0] for row in cursor.fetchall()]

def fetch_habits_by_periodicity(db, periodicity):
    """
    Retrieves the names of habits with a specific periodicity.

    Args:
        db: The database connection object.
        periodicity: The periodicity to filter by (e.g., 'Daily', 'Weekly').

    Returns:
        list: A list of habit names matching the periodicity.
    """
    cursor = db.cursor()
    cursor.execute('SELECT name FROM habits WHERE periodicity = ?', (periodicity,))
    return [row[0] for row in cursor.fetchall()]

def get_habit_tracker(db, name):
    """
    Retrieves a HabitTracker object for the given habit name.

    Args:
        db: The database connection object.
        name: The name of the habit to retrieve.

    Returns:
        HabitTracker or None: The HabitTracker object if found, otherwise None.
    """
    cursor = db.cursor()
    cursor.execute('SELECT * FROM habits WHERE name = ?', (name,))
    habit_data = cursor.fetchone()

    if habit_data:
        return HabitTracker(
            name=habit_data[1],
            description=habit_data[2],
            periodicity=habit_data[3],
            id=habit_data[0]
        )
    else:
        return None