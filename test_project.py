from main import calc_due, get_id_date_counter, overdue_tasks
from habit import Habit, Task
from db import select_all_tasks, select_open_task, update_task, delete_task, return_habit, get_db, create_db
import pytest
import os
from freezegun import freeze_time
from datetime import datetime, timedelta


@freeze_time("2024-04-01")
def test_creation():
    db = get_db("test.db")
    create_db(db)
    first_habit = Habit("Sport", "every second day")
    first_habit.habit_store(db)
    due = calc_due("every second day")
    assert due == datetime.now() + timedelta(days=2)
    first_task = Task("Sport", due, 0)
    first_task.task_store(db)
    db.close()


def success():
    db = get_db("test.db")
    task_list = select_open_task(db)
    completed_task_id, new_due_date, new_counter = get_id_date_counter(task_list, "Sport")
    update_task(completed_task_id, "completed", db)
    successor_task = Task("Sport", new_due_date, new_counter)
    successor_task.task_store(db)
    db.close()
    return new_due_date, new_counter


def missed():
    db = get_db("test.db")
    overdue_tasks(db)
    open_task = select_open_task(db)
    db.close()
    return open_task


@freeze_time("2024-04-03")
def test_success_one():
    new_due_date, new_counter = success()
    assert new_due_date == datetime.now() + timedelta(days=2)
    assert new_counter == 1


@freeze_time("2024-04-06")
def test_missed_one():
    open_task = missed()
    assert open_task.iloc[0, 5] == 0


@freeze_time("2024-04-08")


def test_success_two():
    new_due_date, new_counter = success()
    assert new_due_date == datetime.now() + timedelta(days=2)
    assert new_counter == 1


@freeze_time("2024-04-10")


def test_success_three():
    new_due_date, new_counter = success()
    assert new_due_date == datetime.now() + timedelta(days=2)
    assert new_counter == 2


@freeze_time("2024-04-12")


def test_success_four():
    new_due_date, new_counter = success()
    assert new_due_date == datetime.now() + timedelta(days=2)
    assert new_counter == 3


@freeze_time("2024-04-14")


def test_success_five():
    new_due_date, new_counter = success()
    assert new_due_date == datetime.now() + timedelta(days=2)
    assert new_counter == 4


@freeze_time("2024-04-18")


def test_missed_two():
    open_task = missed()
    assert open_task.iloc[0, 5] == 0


@freeze_time("2024-04-21")


def test_missed_three():
    open_task = missed()
    assert open_task.iloc[0, 5] == 0


@freeze_time("2024-04-23")


def test_success_six():
    new_due_date, new_counter = success()
    assert new_due_date == datetime.now() + timedelta(days=2)
    assert new_counter == 1


@freeze_time("2024-04-25")


def test_success_seven():
    new_due_date, new_counter = success()
    assert new_due_date == datetime.now() + timedelta(days=2)
    assert new_counter == 2


@freeze_time("2024-04-27")


def test_success_eight():
    new_due_date, new_counter = success()
    assert new_due_date == datetime.now() + timedelta(days=2)
    assert new_counter == 3


@freeze_time("2024-04-29")


def test_success_nine():
    new_due_date, new_counter = success()
    assert new_due_date == datetime.now() + timedelta(days=2)
    assert new_counter == 4


@freeze_time("2024-05-01")


def test_success_ten():
    new_due_date, new_counter = success()
    assert new_due_date == datetime.now() + timedelta(days=2)
    assert new_counter == 5


def test_delete():
    os.remove("test.db")

