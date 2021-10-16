from app.models import User


def test_set_password():
    u = User(username="pytest user")
    u.set_password("password")
    assert u.check_password('password') is True
    assert u.check_password('most_secret_word') is False
    assert u.check_password('1234') is False
    assert u.password_hash != "password"
    