import questionary
from habit import Habit, Task
from db import select_all_tasks, select_open_task, update_task, delete_task, return_habit, get_db
from datetime import datetime, timedelta


# cli-Function is used for basic navigation within the solution
def cli():
    db = get_db()
    choice = questionary.select(
        "Welcome to Habi Track! Please select an option:",
        choices=["Select pre-defined habit",
                 "Create new habit",
                 "Complete habit task",
                 "Remind of current habits",
                 "Analyze habits",
                 "Delete habit",
                 "Exit"]
    ).ask()

    if choice == "Select pre-defined habit":
        selected_habit = questionary.select(
            "Please select a habit:",
            choices=["Sport",
                     "Sleep sufficient",
                     "Eat healthy",
                     "Meditation",
                     "Cold shower"]
        ).ask()
        # Calls function select_period() to ask for check frequency
        selected_period = select_period()
        # Creates the habit object based on the selected habit and its frequency and
        # stores it on the db using Habit-class in habit.py
        habit_object = Habit(selected_habit, selected_period)
        habit_object.habit_store(db)

        # Usage of calc_due()-function to transform the selected habit period
        # (e.g. "every day") into datetime format.
        due_date = calc_due(selected_period)
        # Creation of habit task object and store it on the db using Task-class in habit.py
        habit_task_obj = Task(selected_habit, due_date, 0)
        habit_task_obj.task_store(db)

    elif choice == "Create new habit":
        new_habit = questionary.text("What is the name of the habit?").ask()
        # Calls function select_period() to ask for check frequency
        selected_period = select_period()
        # Creates the habit object based on the selected habit and its frequency and
        # stores it on the db using Habit-class in habit.py
        habit_object = Habit(new_habit, selected_period)
        habit_object.habit_store(db)

        # Usage of calc_due()-function to transform the selected habit period
        # (e.g. "every day") into datetime format.
        due_date = calc_due(selected_period)
        # Creation of habit task object and store it on the db using Task-class in habit.py
        habit_task_obj = Task(new_habit, due_date, 0)
        habit_task_obj.task_store(db)

    elif choice == "Complete habit task":
        # Get the current tasks with status "open" from db using select_open_task()-function
        # from db.py and check if any action is overdue and update it by using
        # overdue_tasks()-function
        db = get_db()
        overdue_tasks(db)
        # Get all current tasks again after having updated all overdue tasks
        task_list = select_open_task(db)
        selected_habit = questionary.select(
            "Which habit shall be completed?",
            choices=sorted(task_list["habit_name"])
        ).ask()

        completed_task_id, new_due_date, new_counter = get_id_date_counter(task_list, selected_habit)
        update_task(completed_task_id, "completed", db)

        # Creation of habit task object and store it on the db using Task-class in habit.py
        successor_task = Task(selected_habit, new_due_date, new_counter)
        successor_task.task_store(db)
        db.close()

    elif choice == "Remind of current habits":
        # Get the current tasks with status "open" from db using select_open_task()-function
        # from db.py and check if any action is overdue and update it by using
        # overdue_tasks()-function
        overdue_tasks(db)
        task_list = select_open_task(db)
        print("Here are your current tasks:")
        print(task_list)

    elif choice == "Analyze habits":
        overdue_tasks(db)
        task_list = select_all_tasks(db)
        open_tasks = select_open_task(db)
        habit_list = return_habit(db)
        choice = questionary.select(
            "Which analysis would you like to choose?",
            choices=["Return list of all currently tracked habits",
                     "Return list of all habits with the same periodicity",
                     "Return the longest run streak of all habits",
                     "Return the longest run streak of a selected habits",
                     "Return percentage of completed habits"]
        ).ask()
        if choice == "Return list of all currently tracked habits":
            print(habit_list)
        if choice == "Return list of all habits with the same periodicity":
            selected_period = select_period()
            habit_hits = habit_list.loc[habit_list["period"] == selected_period]
            print(habit_hits)
        if choice == "Return the longest run streak of all habits":
            # open_tasks = task_list.loc[task_list["status"] == "open"]
            max_value = max(open_tasks["streak_counter"])
            print("Here are you habits with the longest run streak")
            print(open_tasks.loc[open_tasks["streak_counter"] == max_value])
        if choice == "Return the longest run streak of a selected habits":
            selected_habit = questionary.select(
                "Which habit shall be selected?",
                choices=sorted(habit_list["habit_name"])
            ).ask()
            current_streak_counter = open_tasks.loc[open_tasks["habit_name"] == selected_habit]
            selected_task = task_list.loc[task_list["habit_name"] == selected_habit]
            max_streak_counter = max(selected_task["streak_counter"])
            if max_streak_counter == current_streak_counter.iloc[0,5]:
                print("Congratuliations! Your longest run streak for this habit is ", current_streak_counter.iloc[0,5], ".\nThis is also your current run streak")
            else:
                print("Your longest run streak for this habit is ", max_streak_counter, ".\nYour current run streak for this habit is ", current_streak_counter.iloc[0,5])
        if choice == "Return percentage of completed habits":
            habit_list["Percent of completed habits"] = ""
            for x in range(0, len(habit_list)):
                current_habit = habit_list.iloc[x,0]
                task_cur_hab = task_list.loc[task_list["habit_name"] == current_habit]
                completed = task_cur_hab[task_cur_hab["status"] == "completed"].count()
                missed = task_cur_hab[task_cur_hab["status"] == "missed"].count()
                if completed.iloc[0] == 0:
                    habit_list.iloc[x, 2] = "nan"
                else:
                    habit_list.iloc[x,2] = completed.iloc[0]*100 / (completed.iloc[0] + missed.iloc[0])
            print("Here are your results")
            print(habit_list[["habit_name", "Percent of completed habits"]])

    elif choice == "Delete habit":
        task_list = select_open_task(db)
        selected_habit = questionary.select(
            "Which habit shall be deleted?",
            choices=sorted(task_list["habit_name"])
        ).ask()
        # Based on the selected habit the delete_task()-function from db.py
        # selects all relevant entries and deletes them
        delete_task(selected_habit, db)
        print("The habit ", selected_habit, " has been deleted successfully. Have a nice day")

    else:
        print("Exiting Habi Track. See you soon.")
    db.close()


def select_period():
    selected_period = questionary.select(
        "Please select an period:",
        choices=["every day", "every second day", "every third day", "every week"]
    ).ask()
    return selected_period


def calc_due(period):
    if period == "every day":
        due = datetime.now() + timedelta(days=1)
    elif period == "every second day":
        due = datetime.now() + timedelta(days=2)
    elif period == "every third day":
        due = datetime.now() + timedelta(days=3)
    else:
        due = datetime.now() + timedelta(days=7)
    return due


def overdue_tasks(db):
    task_list = select_open_task(db)
    length = (len(task_list))
    for x in range(0, length):
        if task_list.iloc[x, 3] < datetime.now():
            missed_task_id = int(task_list.iloc[x, 0])
            missed_habit_name = task_list.iloc[x, 1]
            diff = task_list.iloc[x, 3] - task_list.iloc[x, 2]
            new_due_date = datetime.now() + diff
            update_task(missed_task_id, "missed", db)
            successor_task = Task(missed_habit_name, new_due_date, 0)
            successor_task.task_store(db)


def get_id_date_counter(task_list, selected_habit):
    selected_task = task_list.loc[task_list["habit_name"] == selected_habit]
    completed_task_id = int(selected_task.iloc[0, 0])
    diff = selected_task.iloc[0, 3] - selected_task.iloc[0, 2]
    new_due_date = datetime.now() + diff
    new_counter = int(selected_task.iloc[0, 5] + 1)
    return completed_task_id, new_due_date, new_counter


if __name__ == "__main__":
    cli()
