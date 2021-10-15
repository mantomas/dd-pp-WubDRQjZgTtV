from app.models import Task


def test_mark_finished():
    t = Task(title="testing title", desc="Lorem ipsum")
    assert t.title == "testing title"
    assert t.desc == "Lorem ipsum"


def test_tasks_query(session):
    task = Task(title="Some task")

    session.add(task)
    session.commit()

    assert task.id > 0
