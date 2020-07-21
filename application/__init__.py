from flask import Flask, url_for
from flask_login import LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisisdsajkhsdajkdsaasecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
login_manager = LoginManager(app)
login_manager.login_view = '/login'
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Blueprint
from application.posts.routes import posts
from application.users.routes import users

app.register_blueprint(posts)
app.register_blueprint(users)
