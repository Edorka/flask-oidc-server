# flask-oidc-server
OIDC service written in Python Flask using https://github.com/karec/cookiecutter-flask-restful cookiecutter


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
