# µ-chan
A no fuzz imageboard created as a learning project to dive into Django.
As such, it is still in early development and not ready for production.

## How to run

### Preparations
#### .env file
This project uses Django and PostgreSQL. Make sure you have a PostgreSQL-server running.
To run the project, clone the repo and create a `.env` file in the root folder containing:
```
DB_HOST=<address of your postgresql server>
DB_NAME=<name of the database you want to use>
DB_USER=<postgres-username>
DB_PASSWORD=<postgres-user-password>
DB_PORT=<port to connect to your server, default is 5432>
DB_SECRET=<secret token>

```
To create a new secret token, you can import `secrets` in python and use `secrets.token_urlsafe(<bytes>)`. It's common to precede `django-insecure` for dev environments.

#### Python environment
Create a virtual python environment with the tool of your choice, for example `venv`:
`python -m venv .venv`
And activate it with `source .venv/bin/activate`.
Next, install the required modules with pip:
`pip install -r requirements/dev.txt`

For convenience, the `Makefile` includes several targets - for this case, you can use `make dev-install` to install the dependencies.

#### Migrating the models to the database
To populate your database with the required tables and relations, run `make dev-makemigrations` followed by `dev-migrate`

#### Create an admin user
To create an admin user, you can use `python manage.py createsuperuser --settings=config.settings.dev`

### Starting the server
You should now be able to start the django server with `make dev-start` and access the site on `http://127.0.0.1:8000/`