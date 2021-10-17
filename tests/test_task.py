from app.models import Task
from datetime import datetime


def test_task_model():
    task = Task(
        id=1,
        title="Some task",
        desc="Lorem ipsum",
        file_path="123_curiculum.pdf",
        file_name="curiculum.pdf",
        deadline=datetime.now(),
        finished=False,
        utc_offset=-120,
        user_id=1
        )
    assert task.title == "Some task"
    assert task.finished is False
    assert task.file_path != task.file_name
    assert isinstance(task.deadline, datetime)
    assert task.finished_time is None
    assert task.__repr__() == "<Task Some task>"


def test_mark_finished():
    task = Task(title="Some task")
    assert task.finished_time is None
    task.mark_finished()
    assert task.finished is True
    assert isinstance(task.finished_time, datetime)


def test_mark_unfinished():
    task = Task(
        title="Some task",
        finished=True,
        finished_time=datetime.now()
        )
    task.mark_unfinished()
    assert task.finished is False
    assert task.finished_time is None
