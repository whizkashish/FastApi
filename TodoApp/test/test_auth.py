from .utils import *
from ..routers.auth import get_db, get_current_user,authenticate_user,create_access_token, SECREY_KEY, ALGORITHM
from fastapi import HTTPException
from datetime import timedelta
from jose import jwt
import pytest

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_authenticate_user(test_user):
    db = TestingSessionLocal()

    authenticated_user = authenticate_user(test_user.username, 'admin@123', db)
    assert authenticated_user is not None
    assert authenticated_user.username == test_user.username

    non_existent_user = authenticate_user('dweweewu', 'admin@123', db)
    assert non_existent_user is False

    wrong_password_user = authenticate_user(test_user.username, 'admsain@123', db)
    assert wrong_password_user is False


def test_create_access_token(test_user):
    username = 'testuser'
    user_id = 1
    role = 'user'
    expires_data = timedelta(days=1)

    token = create_access_token(username, user_id, role, expires_data)

    decoded_token = jwt.decode(token, SECREY_KEY, algorithms=[ALGORITHM], 
                               options={'verify_signature': False})
    
    assert decoded_token['sub'] == username
    assert decoded_token['id'] == user_id
    assert decoded_token['role'] == role

@pytest.mark.asyncio
async def test_get_current_user_valid_token():
    encode = {'sub': 'testuser', 'id': 1, 'role': 'admin'}
    token = jwt.encode(encode, SECREY_KEY, algorithm=ALGORITHM)

    user = await get_current_user(token=token)
    assert user == {'username': 'testuser', 'id': 1, 'user_role': 'admin'}


@pytest.mark.asyncio
async def test_get_current_user_missing_payload():
    encode = {'role': 'user'}
    token =  jwt.encode(encode, SECREY_KEY, algorithm=ALGORITHM)

    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token=token)
    
    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == 'Could not validate user'