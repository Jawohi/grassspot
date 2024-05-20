# tests/test_models.py
import unittest
from pymongo import MongoClient
from bson import ObjectId

# tests/test_models.py
import unittest
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime

class Plant:
    def __init__(self, db, name, description, image_url, sunlight, water_needs, temperature_range, status):
        self.db = db
        self.name = name
        self.description = description
        self.image_url = image_url
        self.sunlight = sunlight
        self.water_needs = water_needs
        self.temperature_range = temperature_range
        self.status = status
        self.created_at = datetime.now().isoformat()

    def save(self):
        plant_data = {
            "name": self.name,
            "description": self.description,
            "image_url": self.image_url,
            "sunlight": self.sunlight,
            "water_needs": self.water_needs,
            "temperature_range": self.temperature_range,
            "status": self.status,
            "created_at": self.created_at
        }
        return self.db.plants.insert_one(plant_data).inserted_id


class TestPlantModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = MongoClient('mongodb://localhost:27017/')
        cls.db = cls.client['test_db']

    @classmethod
    def tearDownClass(cls):
        cls.client.drop_database('test_db')
        cls.client.close()

    def test_plant_creation(self):
        plant = Plant(self.db, "Rose", "Beautiful rose", "url", "Full sun", "Regular watering", "10-30°C", "active")
        result = plant.save()
        self.assertIsInstance(result, ObjectId)


if __name__ == '__main__':
    unittest.main()
