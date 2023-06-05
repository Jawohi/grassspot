from datetime import datetime
from pymongo import MongoClient
from bson import ObjectId



client = MongoClient('mongodb+srv://jawohi_gs:myedMz0mDterDuRl@grasscluster.bcqofix.mongodb.net/')
db = client['Grassspot_DB']
plants_collection = db['plants']

class Plant:
    def __init__(self, _id, name, description, image_url, sunlight, water_needs, temperature_range):
        self._id = _id
        self.name = name
        self.description = description
        self.image_url = image_url
        self.sunlight = sunlight
        self.water_needs = water_needs
        self.temperature_range = temperature_range
        self.created_at = datetime.now().isoformat()

    def save(self):
        plants_collection.insert_one(self.__dict__)

    @staticmethod
    def get_all():
        #plants = plants_collection.find()
        plants = plants_collection.find(projection={"created_at": False})
        return [Plant(**plant) for plant in plants]
