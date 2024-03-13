from extensions import db
from apps import create_app
from flask_migrate import Migrate

"""
Initialize Flask application and set up database migrations.

This script initializes a Flask application and configures it using the `create_app()` function from the `apps` module. It also sets up database migrations using Flask-Migrate, allowing for easy management of database schema changes.

Attributes:
    app: The Flask application instance.
    migrate: The Flask-Migrate object for database migrations.
"""
app=create_app()
migrate=Migrate(app,db)