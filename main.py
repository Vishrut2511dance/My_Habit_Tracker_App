import questionary

from analyse import compute_longest_streak
from counter import HabitTracker
from db import initialize_database, fetch_habits_by_periodicity, fetch_all_habit_names, get_habit_tracker


def cli():
    """Main function for the command-line interface."""
    db = initialize_database()

    while not questionary.confirm("Hi User! Welcome to your Habit Tracking App! Wanna proceed?").ask():
        pass

    while True:
        choice = questionary.select(
            "What do you want to do?",
            choices=[
                "Create a New Habit",
                "Increment Habit",
                "Reset Habit",
                "Analyze Habits",
                "Delete Habit",
                "Exit"
            ]).ask()

        if choice == "Create a New Habit":
            create_habit(db)
        elif choice == "Increment Habit":
            increment_habit(db)
        elif choice == "Reset Habit":
            reset_habit(db)
        elif choice == "Analyze Habits":
            analyze_habits(db)
        elif choice == "Delete Habit":
            delete_habit(db)
        elif choice == "Exit":
            break  # Exit the loop

def create_habit(db):
    """Guides the user through creating a new habit."""
    name = questionary.text("What's the name of your new habit?").ask()

    if get_habit_tracker(db, name):
        print("This habit already exists.")
    else:
        desc = questionary.text("How do you wanna describe your habit?").ask()
        while True:
            per = questionary.select("Is this a Daily or a Weekly habit?", choices=["Daily", "Weekly"]).ask()
            if per in ["Daily", "Weekly"]:  # Input validation
                break
            else:
                print("Invalid periodicity. Please select 'Daily' or 'Weekly'.")
        tracker = HabitTracker(name, desc, per)
        try:
            tracker.save_to_database(db)
            print(f"Habit '{name}' created!")
        except Exception as e:
            print(f"An error occurred while creating the habit: {e}")

def increment_habit(db):
    """Guides the user through incrementing a habit's counter."""
    habits = fetch_all_habit_names(db)
    name = questionary.select(
        "What's the name of the habit you want to increment?", choices=habits + ["Exit"]).ask()
    if name != "Exit":
        tracker = get_habit_tracker(db, name)
        tracker.log_progress(db)  # Using the new method name
        print(f"Habit '{name}' incremented!")

def reset_habit(db):
    """Guides the user through resetting a habit's progress."""
    habits = fetch_all_habit_names(db)
    name = questionary.select(
        "What's the name of the habit you want to reset?", choices=habits + ["Exit"]).ask()
    if name != "Exit":
        tracker = get_habit_tracker(db, name)
        tracker.clear_progress(db)  # Using the new method name
        print(f"Habit '{name}' reset!")

def analyze_habits(db):
    """Guides the user through analyzing their habits."""
    analysis_choice = questionary.select(
        "What analysis would you like to perform?",
        choices=[
            "List all habits",
            "List habits by periodicity",
            "Longest streak of all habits",
            "Longest streak for a habit",
            "Exit"
        ]).ask()

    if analysis_choice == "List all habits":
        habits = fetch_all_habit_names(db)
        print("Currently tracked habits:")
        for habit in habits:
            print(habit)
    elif analysis_choice == "List habits by periodicity":
        periodicity = questionary.select(
            "Which periodicity are you interested in?", choices=["Daily", "Weekly"]).ask()
        habits = fetch_habits_by_periodicity(db, periodicity)
        print(f"Habits with '{periodicity}' periodicity:")
        for habit in habits:
            print(habit)
    elif analysis_choice == "Longest streak of all habits":
        longest_streak = 0
        habit_with_longest_streak = ""
        habits = fetch_all_habit_names(db)

        for habit in habits:
            habit_streak = compute_longest_streak(db, habit)
            if habit_streak > longest_streak:
                longest_streak = habit_streak
                habit_with_longest_streak = habit

        print(f"The longest streak of all habits is {longest_streak} for habit '{habit_with_longest_streak}'.")
    elif analysis_choice == "Longest streak for a habit":
        habits = fetch_all_habit_names(db)
        name = questionary.select("Select the habit", choices=habits + ["Exit"]).ask()
        if name != "Exit":
            streak = compute_longest_streak(db, name)
            print(f"The longest streak for habit '{name}' is {streak}.")


def delete_habit(db):
    """Guides the user through deleting a habit."""
    habits = fetch_all_habit_names(db)
    name = questionary.select(
        "What's the name of the habit you want to delete?", choices=habits + ["Exit"]).ask()
    if name != "Exit":
        tracker = get_habit_tracker(db, name)
        tracker.delete_from_database(db)
        print(f"Habit '{name}' deleted!")

if __name__ == "__main__":
    cli()
