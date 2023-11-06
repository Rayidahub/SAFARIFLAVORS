import unittest
from app import app  
from flask import url_for

class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_home_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_about_route(self):
        response = self.app.get('/about/')
        self.assertEqual(response.status_code, 200)

    def test_country_recipe_route(self):
        response = self.app.get('/recipe/Nigeria')  
        self.assertEqual(response.status_code, 200)

    def test_country_recipe_route_invalid_country(self):
        response = self.app.get('/recipe/InvalidCountryName')
        self.assertEqual(response.status_code, 404)

    def test_submit_food_route(self):
        with app.test_request_context('/recipe/submit-food', method='POST'):
            form_data = {
                'food-name': 'GItheri',
                'food-category': 'Kenyan',
                'food-country': 'Kenya',
                'food-description': 'Delicious Gither',
                'food-ingredient': 'onion,tomatoes,royco cubes',
                'food-instructions': 'let it semmer for 10 min',
            }

            response = self.app.post('/recipe/submit-food', data=form_data, content_type='multipart/form-data')
            self.assertEqual(response.status_code, 302)

    def test_food_detail_route(self):
        with app.test_request_context('/food_detail/1', method='GET'):
            response = self.app.get('/food_detail/1')
            self.assertEqual(response.status_code, 200)

    def test_food_detail_route_invalid_id(self):
        response = self.app.get('/food_detail/invalid_id')
        self.assertEqual(response.status_code, 404)

    def test_other_page_route(self):
        response = self.app.get('/static/')
        self.assertEqual(response.status_code, 200)

    def test_success_route(self):
        response = self.app.get('/success')
        self.assertEqual(response.status_code, 200)

    def test_login_route_get(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_logout_route(self):
        response = self.app.get('/logout')
        self.assertEqual(response.status_code, 302)

    def test_load_user_function(self):
        with app.test_request_context('/'):
            user = load_user(1)  
            self.assertIsNotNone(user)

    def test_home_template(self):
        response = self.app.get('/')
        self.assertIn(b'Welcome to the Home Page', response.data)

    def test_about_template(self):
        response = self.app.get('/about/')
        self.assertIn(b'About Us', response.data)

    def test_country_recipe_route_nigeria(self):
    response = self.app.get('/recipe/Nigeria')
    self.assertEqual(response.status_code, 200)

def test_country_recipe_route_kenya(self):
    response = self.app.get('/recipe/Kenya')
    self.assertEqual(response.status_code, 200)


    def test_country_recipe_template_invalid_country(self):
        response = self.app.get('/recipe/InvalidCountryName')
        self.assertIn(b'Country not found', response.data)

    def test_submit_food_route_get(self):
        response = self.app.get('/recipe/submit-food')
        self.assertEqual(response.status_code, 405)

    def test_login_route_post(self):
        with app.test_request_context('/login', method='POST'):
            form_data = {
                'username': 'testuser',
                'password': 'testpassword',
            }

            response = self.app.post('/login', data=form_data)
            self.assertEqual(response.status_code, 302)

if __name__ == '__main__':
    unittest.main()


