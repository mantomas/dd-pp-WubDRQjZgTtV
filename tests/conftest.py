import os
import pytest
import tempfile
from app import create_app
from app import db as _db
from alembic.command import upgrade
from alembic.config import Config
from config import Config as Conf


db_fd, db_path = tempfile.mkstemp()


class TestConfig(Conf):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + db_path


def apply_migrations():
    """Applies all alembic migrations."""
    config = Config('migrations/alembic.ini')
    upgrade(config, "head")


@pytest.fixture(scope="session")
def app(request):
    app = create_app(TestConfig)
    # Establish an application context before running the tests
    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)

    return app


@pytest.fixture(scope='session')
def db(app, request):
    """Creates session db with migrations"""
    def teardown():
        _db.drop_all()
        if os.path.exists(db_path):
            os.unlink(db_path)

    _db.app = app
    apply_migrations()

    request.addfinalizer(teardown)
    return _db


@pytest.fixture(scope='function')
def session(db, request):
    """Creates a new database session for a test"""
    connection = _db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session

@pytest.fixture
def client(app, db):
    
    with app.test_client() as client:
        with app.app_context():
            db.app = app
        yield client
