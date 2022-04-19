# flask-oidc-server
OIDC service written in Python Flask using https://github.com/karec/cookiecutter-flask-restful cookiecutter

## Questions

Note that this is an updated version of a cookiecutter, see the commit list to understand any changes made.

* How much time did you end up spending on it?
About 3-4 non-consecutive hours

* What are some of the design decisions you made?
I opted to use the cookiecutter as allows me to prevent code repetition. However the structure is far from ideal:
There is bussiness logic code inside the API code, this should be decoupled into a `logic` layer sibling to `model` and `api`. This way opening the API to GRPC or similar would take less effort.
Persistence `model` is as good as it can be, has migrations and all good stuff.
OpenAPI/Swagger is available from the beginning all docs are generated from a single place.

* What do you like about your implementation?
Fixed some things from the original as user's tests not telling between different users and admin on updates and deletion.
Love JWT, this can make authentication transversal to other services that trusts this one.

* What would you improve next time?
Move all business logic to a `logic` module; leaving all HTTP and representation stuff into `api` module.
Logic module has to be tested apart from the API module.
Remove all docker-compose stuff.

* What things are missing to make it production-ready?
If this was to be a proper OIDC service a `.well-known` endpoint would be neccesary to provide public keys and all configuration details.
Provide helm charts and container building scripts will be handly to publish the service.
Blacklist is Ok but not a very good choice for a microservices architecture, probably using Redis (or similar) to condemm sessions would be more performant.


## setup 


To run locally a few commands have to be run:
```
virtualenv -p3.8 venv
source venv/bin/activate
pip install -r requirements.txt
# or if you want to run tests an use linters
pip install -p requirements/dev.txt
```
To perform DB setup and configure an admin user:


```
flask db init
flask db migrate
flask db upgrade
flask init
```

## Running 

```
source venv/bin/activate

flask run
```

### Giving a look to the Dcos 

While the service is running, use your favourite browser to access to http://localhost:5000/swagger-ui

## Running tests

Ensure that the packages listed on `requirements/dev.txt` were installed

```
pytest
```
