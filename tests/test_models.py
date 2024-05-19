# tests/test_models.py
import unittest
from pymongo import MongoClient
from bson import ObjectId

# Angenommen, Ihre Modellklasse sieht so aus:
class Plant:
    def __init__(self, db, name, species, care_instructions):
        self.db = db
        self.name = name
        self.species = species
        self.care_instructions = care_instructions

    def save(self):
        plant_data = {
            "name": self.name,
            "species": self.species,
            "care_instructions": self.care_instructions
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
        plant = Plant(self.db, "Rose", "Rosa", "Water daily")
        result = plant.save()
        self.assertIsInstance(result, ObjectId)

if __name__ == '__main__':
    unittest.main()
