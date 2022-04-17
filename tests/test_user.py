from flask import url_for

from users.extensions import pwd_context
from users.models import User


def test_get_user(client, db, user, admin_headers):
    # test 404
    user_url = url_for("api.user_by_id", user_id="100000")
    rep = client.get(user_url, headers=admin_headers)
    assert rep.status_code == 404

    db.session.add(user)
    db.session.commit()

    # test get_user
    user_url = url_for("api.user_by_id", user_id=user.id)
    rep = client.get(user_url, headers=admin_headers)
    assert rep.status_code == 200

    data = rep.get_json()["user"]
    assert data["username"] == user.username
    assert data["email"] == user.email
    assert data["active"] == user.active
    assert data["firstname"] == "firstname"
    assert data["lastname"] == "lastname"


def test_put_user(client, db, user, admin_headers):
    # test 404
    user_url = url_for("api.user_by_id", user_id="100000")
    rep = client.put(user_url, headers=admin_headers)
    assert rep.status_code == 404

    db.session.add(user)
    db.session.commit()

    data = {
        "username": "updated",
        "password": "new_password",
        "firstname": "John",
        "lastname": "Anderson",
    }

    user_url = url_for("api.user_by_id", user_id=user.id)
    # test update user
    rep = client.put(user_url, json=data, headers=admin_headers)
    assert rep.status_code == 200

    data = rep.get_json()["user"]
    assert data["username"] == "updated"
    assert data["email"] == user.email
    assert data["active"] == user.active
    assert data["firstname"] == "John"
    assert data["lastname"] == "Anderson"

    db.session.refresh(user)
    assert pwd_context.verify("new_password", user.password)


def test_put_user_by_another(client, db, user_factory, user_headers):
    user, another = user_factory.create_batch(2)
    data = {"firstname": "just", "lastname": "testing"}

    user_url = url_for("api.user_by_id", user_id=user.id)
    # test update user
    rep = client.put(user_url, json=data, headers=user_headers(another))
    assert rep.status_code == 403
    assert rep.json.get("msg") == "Only admin or user can modify"


def test_delete_user(client, db, user, admin_headers):
    # test 404
    user_url = url_for("api.user_by_id", user_id="100000")
    rep = client.delete(user_url, headers=admin_headers)
    assert rep.status_code == 404

    db.session.add(user)
    db.session.commit()

    # test get_user

    user_url = url_for("api.user_by_id", user_id=user.id)
    rep = client.delete(user_url, headers=admin_headers)
    assert rep.status_code == 200
    assert db.session.query(User).filter_by(id=user.id).first() is None


def test_delete_user_by_another(client, db, user_factory, user_headers):
    user, another = user_factory.create_batch(2)
    data = {"firstname": "just", "lastname": "testing"}

    user_url = url_for("api.user_by_id", user_id=user.id)
    # test update user
    rep = client.delete(user_url, json=data, headers=user_headers(another))
    assert rep.status_code == 403
    assert rep.json.get("msg") == "Only admin or user can modify"


def test_put_user_by_another(client, db, user_factory, user_headers):
    user, another = user_factory.create_batch(2)
    data = {"firstname": "just", "lastname": "testing"}

    user_url = url_for("api.user_by_id", user_id=user.id)
    # test update user
    rep = client.put(user_url, json=data, headers=user_headers(another))
    assert rep.status_code == 403
    assert rep.json.get("msg") == "Only admin or user can modify"


def test_create_user(client, db, admin_headers):
    # test bad data
    users_url = url_for("api.users")
    data = {"username": "created"}
    rep = client.post(users_url, json=data, headers=admin_headers)
    assert rep.status_code == 400

    data["password"] = "admin"
    data["email"] = "create@mail.com"
    data["firstname"] = "John"
    data["lastname"] = "Anderson"

    rep = client.post(users_url, json=data, headers=admin_headers)
    assert rep.status_code == 201

    data = rep.get_json()
    user = db.session.query(User).filter_by(id=data["user"]["id"]).first()

    assert user.username == "created"
    assert user.email == "create@mail.com"
    assert user.firstname == "John"
    assert user.lastname == "Anderson"


def test_get_all_user(client, db, user_factory, admin_headers):
    users_url = url_for("api.users")
    users = user_factory.create_batch(30)

    db.session.add_all(users)
    db.session.commit()

    rep = client.get(users_url, headers=admin_headers)
    assert rep.status_code == 200

    results = rep.get_json()
    for user in users:
        assert any(u["id"] == user.id for u in results["results"])
