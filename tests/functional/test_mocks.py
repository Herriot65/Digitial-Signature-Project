import unittest
from unittest.mock import patch, MagicMock
from apps.user.routes import *
from apps import create_app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app=create_app(config_name='Testing')
        self.client = self.app.test_client()
        
    @patch('apps.user.routes.render_template')
    @patch('apps.user.routes.login_required', return_value=lambda f: f)
    @patch('apps.user.routes.current_user', return_value=MagicMock(is_authenticated=True))
    def test_dashboard_authenticated(self, mock_current_user, mock_login_required, mock_render_template):
        response = self.client.get('/user/dashboard')
        self.assertEqual(response.status_code, 200)
        mock_render_template.assert_called_with('users/dashboard.html')
    
    @patch('apps.user.routes.render_template')
    @patch('apps.user.routes.login_required', return_value=lambda f: f)
    @patch('apps.user.routes.current_user', return_value=MagicMock(is_authenticated=True))
    def test_invalid_dashboard_access(self, mock_current_user, mock_login_required, mock_render_template):
        response = self.client.post('/user/dashboard')
        self.assertEqual(response.status_code, 405)
        mock_render_template.assert_not_called()
    
    @patch('apps.user.routes.logout_user')
    @patch('apps.user.routes.redirect')
    @patch('apps.user.routes.login_required', return_value=lambda f: f)
    @patch('apps.user.routes.current_user', return_value=MagicMock(is_authenticated=True))
    def test_logout(self, mock_login_required, mock_redirect, mock_logout_user, mock_current_user):
        response = self.client.get('/user/logout')
        self.assertEqual(response.status_code, 200)
        mock_logout_user.assert_called_once()
    
    @patch('apps.user.routes.logout_user')
    @patch('apps.user.routes.redirect')
    @patch('apps.user.routes.login_required', return_value=lambda f: f)
    @patch('apps.user.routes.current_user', return_value=MagicMock(is_authenticated=True))
    def test_invalid_logout(self, mock_current_user, mock_login_required, mock_redirect, mock_logout_user):
        response = self.client.post('/user/logout')
        self.assertEqual(response.status_code, 405)
        mock_logout_user.assert_not_called()
    
    @patch('apps.user.routes.render_template')
    @patch('apps.user.routes.login_required', return_value=lambda f: f)
    @patch('apps.user.routes.current_user', return_value=MagicMock(is_authenticated=True))
    @patch('apps.user.routes.User')
    @patch('apps.user.routes.login_user')
    @patch('apps.user.routes.redirect')
    def test_login(self, mock_redirect, mock_login_user, mock_user, mock_current_user, mock_login_required, mock_render_template):
        user = MagicMock()
        user.email = 'test@example.com'
        user.password_hashed = 'hashed_password'
        user.confirmed = True
        mock_user.query.filter_by.return_value.first.return_value = user

        with self.app.test_request_context('/login', method='POST', data={'email': 'test@example.com', 'password': 'password'}):
            from apps.user.routes import login
            login()
            
        mock_redirect.assert_called_once_with('/user/dashboard')

if __name__ == '__main__':
    unittest.main()