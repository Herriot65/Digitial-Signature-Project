from flask import Flask
from models.user import User
from config import ConfigClass
from extensions import mail,login_manager,db
from flask_migrate import Migrate

## @brief Create the Flask application instance.
app=Flask(__name__)

## @brief Configure the application using the configuration class from the config.py file.
app.config.from_object(ConfigClass)

## @brief Initialize the email extension.
mail.init_app(app)

## @brief Initialize the login manager extension.
login_manager.init_app(app)

## @brief Create the application context and create all tables defined in the models directory
# @param app: The application instance.
db.init_app(app)

## @brief Database migration.
migrate=Migrate(app,db)

@app.route('/')
def home():
    return "<h1>Welcome to the home page</h1>"

if __name__=='__main__':
    app.run()