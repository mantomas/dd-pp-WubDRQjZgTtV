from app.models import Task


def test_mark_finished():
    t = Task(title="testing title", desc="Lorem ipsum", finished=True)
    assert t.finished == True


def test_tasks_query(session):
    task = Task(
        title="Some task",
        desc="Lorem ipsum"
        )
    session.add(task)
    session.commit()
    # check created task
    assert task.id > 0
    assert task.title == "Some task"
    assert task.finished == False
    # query task from DB and check again
    task_query = Task.query.get(task.id)
    assert task_query.title == "Some task"
    assert task_query.desc == "Lorem ipsum"


def test_mark_finished(session):
    task = Task(title="Some task")
    session.add(task)
    session.commit()
    task_query = Task.query.get(1)
    assert task.finished is False
    task_query.mark_finished()
    assert task_query.finished is True


def test_mark_unfinished(session):
    task = Task(title="Some task")
    task.mark_unfinished()
    session.add(task)
    session.commit()
    task_query = Task.query.get(1)
    assert task_query.finished is False
