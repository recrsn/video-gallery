# Flask SQLAlchemy Starter

Bare minimum starter template using Flask and SQLAlchemy.

## Installation

### Requirements

- python 3.6 +
- Pipenv for dependency management

## Usage

1. Clone this repository
2. Copy `.env.example` to `.env` and modify the required values.
2. Rename the `flask_sqlalchemy_starter` folder to your package name.
3. Add/remove models
4. Create migrations using `flask db migrate`
5. Apply migrations to database using `flask db upgrade`
6. Run tests with `pytest -v tests`

## Configuring database

You can use any SQLAlchemy compatible URI string for the database. By default, the template uses a SQLite database.

To use a different database like Postgres, edit the `DATABASE_URI` accordingly and install the appropriate python
package to connect to the DB.

### Postgres

1. Run `pipenv install psycopg2`
2. Edit `DATABASE_URI` to `postgres://<user>:<password>@<host>:5432/<database>`

### MySQL

1. Run `pipenv install mysql-connector`
2. Edit `DATABASE_URI` to `mysql://<user>:<password>@<host>:3306/<database>`
