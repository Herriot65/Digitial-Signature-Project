import pytest
from apps import create_app
from extensions import db

@pytest.fixture()
def app():
    """
    Fixture for creating a Flask application instance for testing.

    Creates a Flask application instance with the testing configuration.
    Initializes and drops the database tables within the application context.

    Yields:
        Flask app: The Flask application instance.
    """
    app = create_app(config_name='Testing')
    
    with app.app_context():
        db.create_all()

    yield app
    
    with app.app_context():
        db.drop_all()

@pytest.fixture()
def client(app):
    """
    Fixture for creating a test client.

    Args:
        app (Flask app): The Flask application instance.

    Returns:
        Flask test client: The test client for making requests to the Flask app.
    """
    return app.test_client()
