# My Habit-Tracker-App Project

This Habit Tracking App is a project developed for the *Object-Oriented and Functional Programming with Python* course at the IU International University of Applied Sciences.

## Purpose

This command-line application, programmed in Python, helps you track your habits effectively. The user-friendly interface lets you create, complete, reset, delete, and analyze your habits, providing insights into your progress and consistency.

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/RedlionEster/Habit-Tracker-App 
   ```

2. **Install Python:** 
   Ensure you have Python 3.11 or later installed on your machine.

3. **Install Dependencies:**
   Use the provided `requirements.txt` to install necessary libraries:
   ```bash
   pip install -r requirements.txt
   ```

## Preload Sample Data

For testing or exploration, you can populate the database with a month's worth of sample data:

```bash
python preload_db.py
```

## How to Use

1. **Launch the App:** 
   ```bash
   python main.py 
   ```

2. **Navigate the Menu:**
   Use your keyboard's arrow keys to choose from the following actions:

   * **Create a New Habit:** Add a new habit to track. You'll be prompted to enter the habit's name, description, and periodicity (Daily or Weekly).
   * **Increment Habit:** Mark a habit as completed for the current day or week.
   * **Reset Habit:** Clear the progress of a habit, setting its completion count back to zero.
   * **Analyze Habits:** Gain insights into your habits. You can:
     * List all your tracked habits
     * List habits filtered by their periodicity
     * See the longest streak achieved for any habit
     * See the longest streak for a specific habit
   * **Delete Habit:** Remove a habit entirely from your tracker.
   * **Exit:** Quit the application.

## Sample Habits

The preloaded data includes these habits:

* Study (Daily)
* Read (Daily)
* Gaming (Daily)
* Sport (Daily)
* Laundry (Weekly)

## Automated Testing

This project includes `test_project.py`, which uses `pytest` to automate the testing of core features and database interactions.

* **Run Tests:**
   ```bash
   python -m pytest 
   ```

* **Verbose Output:**
   ```bash
   python -m pytest -v 
   ```
