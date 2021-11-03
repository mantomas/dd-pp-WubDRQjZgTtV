from app.models import User


def test_index(client):
    """
    GIVEN non loged in user/client
    WHEN route is called
    THEN appropriate response
    """
    response = client.get('/')
    # homepage - redirect
    assert response.status_code == 302
  
    response = client.get('/index')
    # alternate homepage - redirect

    assert response.status_code == 302

    response = client.get('/auth/login')
    # login - OK
    assert response.status_code == 200

    response = client.get('/auth/register')
    # registration - OK
    assert response.status_code == 200

    response = client.get('/auth/logout')
    # logout - redirect
    assert response.status_code == 302

    response = client.get('/addtask')
    # add new task - redirect
    assert response.status_code == 302

    response = client.get('/finished')
    # finished tasks page - redirect
    assert response.status_code == 302
