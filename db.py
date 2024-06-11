import sqlite3
import pandas as pd
from datetime import datetime, timedelta


#class storage:
 #   def insert_habit(self, Habit):
#        db = get_db()
 #       cur = db.cursor()
  #      try:
   #         cur.execute("INSERT INTO habit (habit_name, period) VALUES (?, ?)",
    #                    (Habit.name, Habit.period))
     #       db.commit()
      #      db.close()



# Function to initially create the database with the tables habit and habit_task
def create_db(db):
    cur = db.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS habit (
        habit_name TEXT PRIMARY KEY,
        period TEXT)""")
    cur.execute("""CREATE TABLE IF NOT EXISTS habit_task (
        task_id INTEGER PRIMARY KEY AUTOINCREMENT,
        habit_name TEXT,
        created TEXT,
        due TEXT,
        status TEXT,
        streak_counter INTEGER)""")
    db.commit()


# Function to connect to database
def get_db(name="database.db"):
    db = sqlite3.connect(name)
    create_db(db)
    return db




# Function to insert a new habit in the table habit
def insert_habit(selected_habit, selected_period, db):
    cur = db.cursor()
    try:
        cur.execute("INSERT INTO habit (habit_name, period) VALUES (?, ?)",
                    (selected_habit, selected_period))
        db.commit()
    except sqlite3.IntegrityError:
        print("You have already chosen this habit. Please try another one")
        exit()



# Function to insert a new habit task in the table habit_task
def insert_task(habit_name, created, due, status, streak_counter, db):
    cur = db.cursor()
    cur.execute("INSERT INTO habit_task "
                "(habit_name, created, due, status, streak_counter)"
                "VALUES (?, ?, ?, ?, ?)",
                (habit_name, created, due, status, streak_counter))
    db.commit()


def update_task(task_id, status, db):
    cur = db.cursor()
    cur.execute("UPDATE habit_task SET status = ? WHERE task_id = ?",
                (status, task_id,))
    db.commit()



def select_all_tasks(db):
    task_list = pd.read_sql_query("SELECT * FROM habit_task;", db)
    task_list["created"] = pd.to_datetime(task_list["created"])
    task_list["due"] = pd.to_datetime(task_list["due"])
    return task_list


# Function to select all open habit task and print the result
def select_open_task(db):
    task_list = pd.read_sql_query("SELECT * FROM habit_task WHERE status = 'open'", db)
    task_list["created"] = pd.to_datetime(task_list["created"])
    task_list["due"] = pd.to_datetime(task_list["due"])
    return task_list



def return_habit(db):
    current_habits = pd.read_sql_query("SELECT * FROM habit", db)
    return current_habits


def delete_task(selected_habit, db):
    cur = db.cursor()
    cur.execute("DELETE FROM habit WHERE habit_name = ?",
                (selected_habit,))
    db.commit()
    cur.execute("DELETE FROM habit_task WHERE habit_name = ?",
                (selected_habit,))
    db.commit()
