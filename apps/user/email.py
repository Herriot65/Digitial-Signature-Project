from extensions import db 
from datetime import datetime
from models.user import User
from itsdangerous import URLSafeTimedSerializer

# Initialize the URLSafeTimedSerializer with a secret key for generating and verifying tokens
s = URLSafeTimedSerializer('SECRET_KEY')

def generate_confirmed_token(email):
    """
    Generate a confirmation token for user email.

    Args:
        email (str): The email address to generate the token for.

    Returns:
        str: The generated confirmation token.
    """
    token = s.dumps({'confirm': email})
    return token

def user_confirm_token(token):
    """
    Confirm a user's email based on the provided token.

    Args:
        token (str): The confirmation token to verify.

    Returns:
        str: The confirmed user's email address if successful, False otherwise.
    """
    try:
        data = s.loads(token.encode('utf-8'), max_age=1200)
    except Exception:
        return False
    
    user = User.query.filter_by(email=data.get('confirm')).first()
    if user:
        user.confirmed = True
        db.session.commit()
        return data.get('confirm')
    else:
        return False
