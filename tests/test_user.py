from app.models import User


def test_set_password(session):
    u = User(username="pytest user")
    u.set_password("password")
    assert u.check_password('most_secret_word') is False
    assert u.check_password('password') is True
    assert u.check_password('1234') is False
    session.add(u)
    session.commit()
    users = User.query.all()
    assert len(users) > 0
    assert users[0].check_password("password") is True
    assert users[0].password_hash != "password"
