from db import fetch_all_habit_names
from datetime import datetime

def compute_longest_streak(db, habit_name):
    """
    Calculates the longest consecutive streak of completions for a specific habit.

    Args:
        db: The database connection.
        habit_name: The name of the habit.

    Returns:
        int: The length of the longest streak.
    """

    cursor = db.cursor()
    cursor.execute('''
        SELECT tracked_at 
        FROM progress_log
        INNER JOIN habits ON progress_log.habit_id = habits.id
        WHERE habits.name = ?
        ORDER BY tracked_at ASC
    ''', (habit_name,))
    completion_dates = cursor.fetchall()

    if not completion_dates:
        return 0  # No completions recorded for this habit

    dates = [datetime.strptime(date[0], "%Y-%m-%d %H:%M:%S") for date in completion_dates]

    max_streak = 1
    current_streak = 1

    for i in range(1, len(dates)):
        if (dates[i] - dates[i - 1]).days == 1:
            current_streak += 1
        else:
            max_streak = max(max_streak, current_streak)
            current_streak = 1

    return max(max_streak, current_streak)  # Consider the final streak

def compute_longest_streak_overall(db):
    """
    Calculates the longest streak across all habits in the database.

    Args:
        db: The database connection.

    Returns:
        int: The length of the longest streak among all habits.
    """
    all_habits = fetch_all_habit_names(db)
    longest = 0

    for habit in all_habits:
        habit_streak = compute_longest_streak(db, habit)
        longest = max(longest, habit_streak)

    return longest