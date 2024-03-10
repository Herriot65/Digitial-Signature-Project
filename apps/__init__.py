from config import ConfigClass
from flask import Flask,render_template
from extensions import db,mail,login_manager
from apps.user.routes import user
from apps.posts.routes import post
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object(ConfigClass)
    app.template_folder = '../templates'
    app.static_folder = '../static'
    
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(user)
    app.register_blueprint(post)
    
    @app.route('/')
    def home():
        return render_template('index.html')

    return app