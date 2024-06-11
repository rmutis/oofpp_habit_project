from datetime import datetime
from db import insert_habit, insert_task


class Habit:
    def __init__(self, name: str, period: str):
        self.name = name
        self.period = period

    def habit_store(self, db):
        insert_habit(self.name, self.period, db)


class Task:
    def __init__(self, name: str, due: datetime, streak_counter: int):
        self.name = name
        self.created = datetime.now()
        self.due = due
        self.status = "open"
        self.streak_counter = streak_counter

    def task_store(self, db):
        insert_task(self.name, self.created, self.due, self.status, self.streak_counter, db)
