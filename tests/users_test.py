from core.models.users import User

def test_user_repr(new_user):
    assert repr(new_user) == f'<User {new_user.username!r}>'

def test_user_filter(new_user, test_db_session):
    users = User.filter(User.id == new_user.id).all()
    assert len(users) == 1
    assert users[0].id == new_user.id

def test_user_get_by_id(new_user, test_db_session):
    user = User.get_by_id(new_user.id)
    assert user.id == new_user.id

def test_user_get_by_email(new_user, test_db_session):
    user = User.get_by_email(new_user.email)
    assert user.email == new_user.email
