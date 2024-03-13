from config import ConfigClass  
from apps.user.routes import user  
from apps.posts.routes import post  
from flask import Flask, render_template  
from extensions import db, mail, login_manager  

def create_app(config_name='development'):
    """
    Factory function to create a Flask application instance.

    Args:
        config_name (str): Name of the configuration to use. Defaults to 'development'.

    Returns:
        Flask app: The Flask application instance.
    """
    app = Flask(__name__)  # Creating Flask application instance
    
    # Load configuration based on the specified config_name
    if config_name == 'development':
        app.config.from_object('config.DevelopmentConfig')
    else:
        app.config.from_object('config.TestingConfig')
    
    # Setting template and static folders
    app.template_folder = '../templates'
    app.static_folder = '../static'
    
    # Initializing extensions
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    
    # Registering blueprints
    app.register_blueprint(user)
    app.register_blueprint(post)
    
    # Home route
    @app.route('/')
    def home():
        return render_template('index.html')

    return app  # Returning the Flask application instance
