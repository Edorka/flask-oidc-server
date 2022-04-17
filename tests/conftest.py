import json
import pytest
from dotenv import load_dotenv

from users.models import User
from users.app import create_app
from users.extensions import db as _db
from pytest_factoryboy import register
from tests.factories import UserFactory


register(UserFactory)


@pytest.fixture(scope="session")
def app():
    load_dotenv(".testenv")
    app = create_app(testing=True)
    return app


@pytest.fixture
def db(app):
    _db.app = app

    with app.app_context():
        _db.create_all()

    yield _db

    _db.session.close()
    _db.drop_all()


@pytest.fixture
def admin_user(db):
    user = User(
        username='admin',
        email='admin@admin.com',
        password='admin'
    )

    db.session.add(user)
    db.session.commit()

    return user


@pytest.fixture
def some_users(db):
    users = []
    for index in range(1, 3):
        username = "user{index}"
        user = User(
            username=username,
            email=f"{username}@company.com",
            password=f"{username}-password",  # what a bad idea
        )
        db.session.add(user)
        users.append(user)
    db.session.commit()
    return users


def do_login(username, password, client):
    data = {
        'username': username,
        'password': password,
    }
    rep = client.post(
        '/auth/login',
        data=json.dumps(data),
        headers={'content-type': 'application/json'}
    )
    print(dir(rep))
    tokens = json.loads(rep.get_data(as_text=True))
    return {
        'content-type': 'application/json',
        'authorization': 'Bearer %s' % tokens['access_token']
    }


@pytest.fixture
def admin_headers(admin_user, client):
    return do_login(admin_user.username, 'admin')


@pytest.fixture
def user_headers(client):

    def login(user):
        return do_login(user.username, f"{user.username}-password", client)

    return login


@pytest.fixture
def admin_refresh_headers(admin_user, client):
    data = {
        'username': admin_user.username,
        'password': 'admin'
    }
    rep = client.post(
        '/auth/login',
        data=json.dumps(data),
        headers={'content-type': 'application/json'}
    )

    tokens = json.loads(rep.get_data(as_text=True))
    return {
        'content-type': 'application/json',
        'authorization': 'Bearer %s' % tokens['refresh_token']
    }
