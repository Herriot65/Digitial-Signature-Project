## @file
# Database and sending email configuration file

import os

## @brief Configuration of the mysql database and parameters for sending email.
class ConfigClass:
    SQLALCHEMY_DATABASE_URI='mysql://root:0000@localhost/digital_signature_database'
    SECRET_KEY=os.environ.get('SECRET_KEY') or 'password'
    SQLALCHEMY_TRACK_MODIFICATIONS=True

    MAIL_SERVER='smtp.googlemail.com'
    MAIL_PORT=465
    MAIL_USE_SSL=True 
    MAIL_USE_TLS=False 
    MAIL_USERNAME='yourmail@gmail.com'
    MAIL_PASSWORD='yourapplicationpassword'
    MAIL_DEBUG=False