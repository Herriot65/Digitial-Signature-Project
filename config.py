# Database and sending email configuration file
import os
##Configuration of the mysql database and parameters for sending email.
class ConfigClass:
    SECRET_KEY=os.environ.get('SECRET_KEY') or 'password'
    SQLALCHEMY_TRACK_MODIFICATIONS=True

    MAIL_SERVER='smtp.googlemail.com'
    MAIL_PORT=465
    MAIL_USE_SSL=True 
    MAIL_USE_TLS=False 
    MAIL_USERNAME='yourmail@gmail.com'
    MAIL_PASSWORD='app password'
    MAIL_DEBUG=False
    
class DevelopmentConfig(ConfigClass):
    # Development configuration settings
    SQLALCHEMY_DATABASE_URI='mysql://root:password@localhost/database_name'

class TestingConfig(ConfigClass):
    # Testing configuration settings
    SQLALCHEMY_DATABASE_URI = 'sqlite://'  # Using SQLite for testing
    SQLALCHEMY_TRACK_MODIFICATIONS=False
