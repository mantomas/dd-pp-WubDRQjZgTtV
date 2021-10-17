from app.models import User, load_user


def test_set_password():
    u = User(username="pytest user")
    u.set_password("password")
    assert u.check_password('password') is True
    assert u.check_password('most_secret_word') is False
    assert u.check_password('1234') is False
    assert u.password_hash != "password"
    assert u.__repr__() == "<User pytest user>"


def test_load_user(session):
    u = User(username="pytest user")
    session.add(u)
    session.commit()
    assert load_user(1)


def test_user_tasks(session):
    u = User(username="pytest user")
    session.add(u)
    session.commit()
    assert u.user_tasks()
    assert u.user_tasks_finished()
