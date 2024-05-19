# tests/test_routes.py
import unittest
from flask import Flask, jsonify
from app import create_app

class TestFlaskRoutes(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()

    def test_index_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Welcome', response.get_data(as_text=True))

    def test_add_plant(self):
        response = self.client.post('/add-plant', data={
            'name': 'Daisy',
            'species': 'Bellis perennis',
            'care_instructions': 'Minimal water'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Plant added', response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()
