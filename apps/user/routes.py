## @file
# Blueprint for user readers' authentication.
# Contains routes and functions related to user authentication.
from datetime import datetime
from flask import Blueprint,request,render_template, redirect
from flask_bcrypt import Bcrypt
from models.user import User
from .email import generate_confirmed_token,user_confirm_token
from extensions import mail,login_manager,db
from flask_mail import Message
from flask_login import login_user,logout_user,current_user,login_required
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash
from config import ConfigClass

user=Blueprint('user', __name__, url_prefix='/user')

## @brief Create an instance of the Bcrypt class from flask_bcrypt for password hashing.
bcrypt=Bcrypt()

login_manager.init_app(user)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def user_email_exist(email):
    user=User.query.filter_by(email=email).first()
    if user :
        return True
    else:
        return False

@user.route('/register', methods=['GET', 'POST'])
def register():
    if request.method=='POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('oassword')

        if not user_email_exist(email):
            password_hashed=bcrypt.generate_password_hash(password)
            new_user=User(username=username,email=email,password_hashed=password_hashed,created_at=datetime.now())
            db.session.add(new_user)
            db.session.commit()

            confirmation_token = generate_confirmed_token(email)
            confirm_link = f"http://localhost:5000/user/confirm/{confirmation_token}"
            confirmation_email = render_template('confirm.htm', username=username, confirm_link=confirm_link)

            msg = Message('Confirm your email address', recipients=[email],sender=ConfigClass.MAIL_USERNAME)
            msg.html = confirmation_email
            mail.send(msg)

            flash('Registration successful. Please check your email to confirm your account.')
            return redirect(url_for('user.login'))
        else:
            flash('Email already registered,Please change.')
    return render_template('users/register.html')


@user.route('/confirm/<token>')
def confirm_email(token):
    if user_confirm_token(token):
        flash('you email has succesfully been confirmed')
    else:
        flash('Invalid or expired link')
    return redirect(url_for('user.login'))

@user.route('/resend_email_confirmation_link', methods=['GET', 'POST'])
def resend_email_confirmation_link():
    if request.method=='POST':
        email = request.form.get('email')
        user=User.query.filter_by(email=email).first()
        if user:
            confirmation_token = generate_confirmed_token(email)
            confirm_link = f"http://localhost:5000/user/confirm/{confirmation_token}"
            confirmation_email = render_template('confirm.htm', username=user.username, confirm_link=confirm_link)
            
            msg = Message('Confirm your account', recipients=[email], sender=ConfigClass.MAIL_USERNAME)
            msg.html = confirmation_email 
            mail.send(msg)
            
            flash('Email confirmation link has been resent. Please check your email.')
            return redirect(url_for('user.login'))
        else:
            flash('No user found with the provided email address.')

    return render_template('users/resend_confirmation_email.html')

@user.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()

        if user is not None and bcrypt.check_password_hash(user.password_hashed,password)and user.confirmed:
            login_user(user)
            return redirect(url_for('user.dashboard'))
        elif user is not None and not user.confirmed:
            flash('You haven\'t confirmed your email address. Please check your mailbox or request a new confirmation email.')
        else:
            flash('Invalid email or password.')

    return render_template('users/login.html')

@user.route('/dashboard')
@login_required
def dashboard():
    return render_template('users/dashboard.html')

@user.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


