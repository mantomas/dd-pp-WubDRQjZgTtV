from app.models import User


def test_password_hashing():
    u = User(username='susan')
    u.set_password('most_secret_word')
    assert u.check_password('most_secret_word') == True
    assert u.check_password('password') == False
    assert u.check_password('1234') == False


# def test_user():
#     u = User.query.get(1)
#     assert u.username == "somebody"
