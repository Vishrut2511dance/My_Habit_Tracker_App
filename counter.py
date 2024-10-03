from datetime import datetime

class HabitTracker:
    """Represents a habit to be tracked, along with its progress over time.

    Attributes:
        habit_id (int): A unique identifier for the habit (optional, assigned by the database).
        name (str): The name or title of the habit.
        description (str): A more detailed description of the habit.
        periodicity (str): How frequently the habit should be performed (e.g., "Daily", "Weekly").
        creation_date (str): The date and time the habit was created.

    Methods:
        save_to_database(database): Saves the habit details to the provided database.
        log_progress(database, timestamp=None): Logs a completion of the habit at the given or current time.
        clear_history(database): Removes all completion records for the habit.
        delete_from_database(database): Deletes the habit and all associated completion records.
    """

    def __init__(self, name: str, description: str, periodicity: str, habit_id: int = None) -> None:
        """
        Initializes a new HabitTracker instance.

        Args:
            name: The name of the habit.
            description: A brief description of the habit.
            periodicity: The frequency with which the habit should be tracked (e.g., 'Daily', 'Weekly').
            habit_id: (Optional) A unique identifier for the habit. If not provided, it will be assigned upon saving to the database.
        """
        self.habit_id = habit_id
        self.name = name
        self.description = description
        self.periodicity = periodicity
        self.creation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def save_to_database(self, db):
        """
        Saves the habit information to the database.

        Args:
            db: The database connection object.
        """
        cursor = db.cursor()
        cursor.execute(
            """
            INSERT INTO habits (name, description, periodicity, creation_date)
            VALUES (?, ?, ?, ?)
            """,
            (self.name, self.description, self.periodicity, self.creation_date),
        )
        db.commit()
        self.habit_id = cursor.lastrowid  # Retrieve the auto-generated ID

    def log_progress(self, db, tracked_at: datetime = None) -> None:
        """
        Logs progress for the habit on a specific date and time.

        Args:
            db: The database connection object.
            tracked_at: (Optional) The datetime when the progress was made.
                        Defaults to the current datetime if not provided.
        """
        if self.habit_id is None:  # Check if habit is saved before logging
            raise ValueError("Habit must be saved to the database before logging progress.")

        cursor = db.cursor()
        tracked_at = tracked_at or datetime.now()  # Use current time if not provided

        cursor.execute(
            """
            INSERT INTO progress_log (habit_id, tracked_at)
            VALUES (?, ?)
            """,
            (self.habit_id, tracked_at.strftime("%Y-%m-%d %H:%M:%S")),
        )
        db.commit()

    def clear_progress(self, db) -> None:
        """
        Clears all progress logs for this habit from the database.

        Args:
            db: The database connection object.
        """
        if self.habit_id is None:  # Check if habit is saved before clearing
            raise ValueError("Habit must be saved to the database before clearing progress.")

        cursor = db.cursor()
        cursor.execute(
            """
            DELETE FROM progress_log
            WHERE habit_id = ?
            """,
            (self.habit_id,),
        )
        db.commit()

    def delete_from_database(self, db) -> None:
        """
        Deletes the habit and all its progress logs from the database.

        Args:
            db: The database connection object.
        """
        if self.habit_id is None:  # Check if habit is saved before deleting
            raise ValueError("Habit must be saved to the database before deleting.")

        cursor = db.cursor()
        cursor.execute("DELETE FROM habits WHERE id = ?", (self.habit_id,))
        cursor.execute("DELETE FROM progress_log WHERE habit_id = ?", (self.habit_id,))
        db.commit()
