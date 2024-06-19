from .utils import *
from ..routers.Users import get_db,get_current_user
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_return_user(test_user):
    response = client.get('/user')

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == 'admin'
    assert response.json()['email'] == 'admin@gmail.com'
    assert response.json()['first_name'] == 'admin'
    assert response.json()['last_name'] == 'user'
    assert response.json()['role'] == 'admin'
    assert response.json()['phone_number'] == '1234567890'
     

def test_change_password_success(test_user):
    response = client.put('/user/change-password', json={'password':'admin@123',
                                                  'new_password': 'newpassword'})
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_change_password_invalid_current_password(test_user):
    response = client.put('/user/change-password', json={'password':'admdsdssdsin@123',
                                                  'new_password': 'newpassword'})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Error on password change'}

def test_change_phone_number_success(test_user):
    response = client.put('/user/update-phone-number', json={'phone_number':'9878451264'})
    assert response.status_code == status.HTTP_204_NO_CONTENT