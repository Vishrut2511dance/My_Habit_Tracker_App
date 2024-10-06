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
        return 0

    # Ensure the dates are sorted chronologically
    dates = sorted([datetime.strptime(date[0], "%Y-%m-%d %H:%M:%S") for date in completion_dates])

    max_streak = 1
    current_streak = 1
    prev_date = dates[0]  # Initialize prev_date

    for date in dates[1:]:  # Iterate from the second date
        # Calculate the difference in days, considering potential time differences
        diff = (date - prev_date).days
        if diff == 1:
            current_streak += 1
        elif diff > 1:  # Reset streak if the gap is more than one day
            max_streak = max(max_streak, current_streak)
            current_streak = 1
        # For gaps of 0 days (multiple entries on the same day), continue the streak
        prev_date = date  # Update prev_date for the next iteration

    return max(max_streak, current_streak)


def compute_longest_streak_overall(db):
    """
    Calculates the longest streak across all habits in the database.

    Args:
        db: The database connection.

    Returns:
        int: The length of the longest streak among all habits.
    """
    # ... (Your existing code for compute_longest_streak_overall) ...
