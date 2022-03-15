import os

from app import create_app, db
from flask_migrate import Migrate, command
from app.models import User, Role


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
Migrate(app, db)

if __name__ == '__main__':
    app.run()
