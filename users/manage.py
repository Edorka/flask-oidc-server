import click
from flask.cli import with_appcontext


@click.command("init")
@with_appcontext
def init():
    """Create a new admin user"""
    from users.extensions import db
    from users.models import User

    click.echo("create user")
    user = User(username="admin", email="admin@challenge.com", password="1234", active=True)
    db.session.add(user)
    db.session.commit()
    click.echo("created user admin")
