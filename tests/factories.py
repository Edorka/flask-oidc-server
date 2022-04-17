import factory
from users.models import User


class UserFactory(factory.Factory):

    username = factory.Sequence(lambda n: "user%d" % n)
    email = factory.Sequence(lambda n: "user%d@mail.com" % n)
    firstname = "firstname"
    lastname = "lastname"
    password = "mypwd"

    class Meta:
        model = User
