import pytest
import json
from tests import app
from core import db, app
from core.models.users import User
import uuid

@pytest.fixture
def client():
    return app.test_client()

@pytest.fixture
def h_student_1():
    headers = {
        'X-Principal': json.dumps({
            'student_id': 1,
            'user_id': 1
        })
    }

    return headers

@pytest.fixture
def h_student_2():
    headers = {
        'X-Principal': json.dumps({
            'student_id': 2,
            'user_id': 2
        })
    }

    return headers

@pytest.fixture
def h_teacher_1():
    headers = {
        'X-Principal': json.dumps({
            'teacher_id': 1,
            'user_id': 3
        })
    }

    return headers

@pytest.fixture
def h_teacher_2():
    headers = {
        'X-Principal': json.dumps({
            'teacher_id': 2,
            'user_id': 4
        })
    }

    return headers

@pytest.fixture(scope='module')
def test_db():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='function')
def test_db_session(test_db):
    test_db.session.begin_nested()
    yield test_db.session
    test_db.session.rollback()



@pytest.fixture
def new_user(test_db_session):
    unique_id = uuid.uuid4()
    user_data = {
        'username': f'testuser-{unique_id}',
        'email': f'testuser-{unique_id}@example.com',
    }
    user = User(**user_data)
    test_db_session.add(user)
    test_db_session.commit()
    return user

