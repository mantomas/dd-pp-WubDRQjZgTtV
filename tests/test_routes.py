from app.models import User


def test_index(client):
    """not logged in user
    / or /index should redirect (302)
    """
    response = client.post('/')
    assert response.status_code == 302
  
    response = client.post('/index')
    assert response.status_code == 302
