import factory
from users.models import User
from users.extensions import db as _db


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):

    id = factory.Sequence(lambda n: n)
    username = factory.Sequence(lambda n: "user%d" % n)
    email = factory.Sequence(lambda n: "user%d@mail.com" % n)
    firstname = "firstname"
    lastname = "lastname"
    password = "mypwd"

    class Meta:
        model = User
        sqlalchemy_session = _db.session  # the SQLAlchemy session object
