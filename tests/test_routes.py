# tests/test_routes.py
import unittest
from flask import Flask, jsonify
from app import app as flask_app  # Stelle sicher, dass dies korrekt ist

class TestFlaskRoutes(unittest.TestCase):
    def setUp(self):
        self.app = flask_app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_index_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Welcome', response.get_data(as_text=True))

    def test_add_plant(self):
        # Beispielhaft angenommen, dass deine app.py die Pflanzendaten so erwartet:
        plant_data = {
            'name': 'Daisy',
            'description': 'A lovely daisy flower',
            'image_url': 'http://example.com/daisy.jpg',
            'sunlight': 'Full sun',
            'water_needs': 'Moderate',
            'temperature_range': '15-25°C',
            'status': 'active'
        }
        response = self.client.post('/add-plant', data=plant_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Pflanze erfolgreich hinzugefügt', response.get_data(as_text=True))  


if __name__ == '__main__':
    unittest.main()
