from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

# Initialize the database instance
db = SQLAlchemy()
DB_NAME = 'database.db'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'mysecretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable track modifications
    db.init_app(app)
    
    # Import blueprints
    from .views import views
    from .auth import auth
    from .admin import admin  # Import the admin blueprint

    # Register blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/admin')  # Register the admin blueprint

    # Import User model
    from .models import User

    # Initialize the login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # Redirect to login page if not logged in
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Create the database if it doesn't exist
    create_database(app)

    return app

def create_database(app):
    if not os.path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()  # Create all database tables
        print('Created database!')