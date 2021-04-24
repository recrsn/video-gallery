import pytest


@pytest.fixture
def client(app):
    with app.test_client() as flask_client:
        yield flask_client
