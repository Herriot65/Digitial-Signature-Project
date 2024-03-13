from models.user import User

def test_register(client):
    """
    Test registration functionality.

    Registers a new user and verifies that the registration process is successful,
    and the appropriate flash messages and redirections occur.
    """
    response = client.post('user/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password'
    }, follow_redirects=True)
    
    assert response.status_code==200
    assert b'Registration successful. Please check your email to confirm your account.' in response.data
    assert b'Login' in response.data
    assert b'Register' in response.data
    assert b'Remember me' in response.data

def test_login(client,app):
    """
    Test user login functionality.

    Registers a new user, simulates login attempts with valid and invalid credentials,
    and verifies the behavior of the application in each case.
    """
    with app.app_context():
        client.post('user/register', data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password'
        }, follow_redirects=True)
        
        #check if user is registered in database
        user=User.query.filter_by(email='test@example.com').first()
        assert user 
        
        response = client.post('user/login', data={
            'email': 'test@example.com',
            'password': 'password'
        },follow_redirects=True)

        #assume that user cannot connect without confirming his account
        assert response.status_code==200
        assert b'You have not confirmed your email address. Please check your mailbox or request a new confirmation email.' in response.data
   
        user.confirmed=1
        
        response1 = client.post('user/login', data={
            'email': 'test@example.com',
            'password': 'password'
        },follow_redirects=True)
        
        assert b'Dashboard!' in response1.data
        assert b'Here is some information about your account:' in response1.data

def test_invalid_login(client,app):
    """
    Test invalid login attempt.

    Registers a new user, confirms the email address, and then attempts to log in with incorrect credentials.
    Verifies that the application handles invalid login attempts appropriately.
    """
    with app.app_context():
        client.post('user/register',data={'username': 'testuser','email': 'test@example.com',
                                            'password': 'password'}, follow_redirects=True)
            
        user=User.query.filter_by(email='test@example.com').first()
        user.confirmed=1
        
        response = client.post('user/login', data={
            'email': 'test@example.com',
            'password': 'wrongpassword'
        },follow_redirects=True)
        
        assert response.status_code==200
        assert b'Invalid email or password' in response.data

def test_double_registration(client):
    """
    Test double registration prevention.

    Attempts to register a user with the same email address twice and verifies that the
    application prevents duplicate registrations.
    """
    client.post('user/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password'
    }, follow_redirects=True)
    
    response =client.post('user/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password'
    }, follow_redirects=True)
    
    assert response.status_code==200
    assert b'Email already registered,Please change.' in response.data

def test_invalid_registration(client):
    """
    Test invalid user registration.

    Attempts to register a user with invalid input data (empty username, email, or password).
    Verifies that the application handles invalid registration inputs appropriately.
    """
    response =client.post('user/register', data={
        'username': '',
        'email': 'test@example.com',
        'password': 'password'
    }, follow_redirects=True)
    
    assert b'Username is required.' in response.data 
    
    response1 =client.post('user/register', data={
        'username': 'testuser',
        'email': '',
        'password': 'password'
    }, follow_redirects=True)
    
    assert b'Email is required.' in response1.data
    
    response2 =client.post('user/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': ''
    }, follow_redirects=True)
    
    assert b'Password is required.' in response2.data
    
def test_resend_email_confirmation_link(client):
    """
    Test resending email confirmation link.

    Registers a new user and then attempts to resend the email confirmation link
    with both valid and invalid email addresses. Verifies the behavior of the application.
    """
    client.post('/user/register',data={
            'username':'testuser',
            'email':'test@example.com',
            'password':'password'
            })

    response_without_register=client.post('/user/resend_email_confirmation_link',data={'email':'wrong@gmail.com'})
    assert b'No user found with the provided mail address.' in response_without_register.data

    response=client.post('/user/resend_email_confirmation_link',data={'email':'test@example.com'},follow_redirects=True)
    assert response.status_code == 200
    assert b'Email confirmation link has been resent. Please check your mail box.' in response.data    

def test_logout(client,app):
    """
    Test user logout functionality.

    Registers a new user, confirms the email address, logs in the user, and then logs out.
    Verifies that the logout process is successful and the user is redirected to the home page.
    """
    with app.app_context():
        client.post('/user/register', data={'username': 'testuser', 'email': 'test@example.com', 'password': 'password'}, follow_redirects=True)
        
        user=User.query.filter_by(email='test@example.com').first()
        user.confirmed=1
        
        login_response = client.post('/user/login', data={'email': 'test@example.com', 'password': 'password'}, follow_redirects=True)
        
        assert login_response.status_code == 200
        assert b'Welcome to your Dashboard!' in login_response.data

        logout_response = client.get('/user/logout', follow_redirects=True)
        
        assert logout_response.status_code == 200 
        assert b'Login!' in logout_response.data
        assert b'Register!' in logout_response.data

    


    
            
        
        
    
    
 
    
    
    