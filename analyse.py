from datetime import datetime

# ... other imports ...

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

    # Print the fetched dates (optional - can be commented out)
    # print(f"Dates for {habit_name}: {dates}")

    max_streak = 1
    current_streak = 1

    for i in range(1, len(dates)):
        # For debugging, print the dates being compared (optional - can be commented out)
        # print(f"Comparing {dates[i]} and {dates[i - 1]}")
        if (dates[i] - dates[i - 1]).days == 1:
            current_streak += 1
            # print(f"Current streak: {current_streak}")  # Optional - can be commented out
        else:
            # print("Streak broken!")  # Remove or comment out this line
            max_streak = max(max_streak, current_streak)
            current_streak = 1

    return max(max_streak, current_streak)
