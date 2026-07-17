from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
import os


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


def init_db(app):
    """Initialize the database with the Flask app"""

    # Ensure the database directory exists
    db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')

    if db_uri.startswith('sqlite:///'):
        # Extract the database file path from the URI
        db_path = db_uri.replace('sqlite:///', '')

        # Handle relative paths
        if not os.path.isabs(db_path):
            db_path = os.path.join(app.instance_path, db_path)
            app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

        # Create the directory if it doesn't exist
        db_dir = os.path.dirname(db_path)
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)

        print(f"Database path: {db_path}")

    db.init_app(app)

    # Import models to ensure they are registered
    from database.models import Job, JobLog, JobConfiguration

    # Create all tables
    with app.app_context():
        try:
            db.create_all()
            print("Database tables created successfully")
        except Exception as e:
            print(f"Error creating database tables: {e}")
            raise
