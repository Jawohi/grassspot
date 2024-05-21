from datetime import datetime
from pymongo import MongoClient
from bson import ObjectId
import os

# Laden der Umgebungsvariablen
MONGO_URI = os.getenv('MONGO_URI')
DB_NAME = os.getenv('DB_NAME', 'Grassspot_DB') 

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
plants_collection = db['plants']
entries_collection = db['care_journal_entries']




class Plant:
    def __init__(self, _id, name, description, image_url, sunlight, water_needs, temperature_range, status='active'):
        self._id = _id
        self.name = name
        self.description = description
        self.image_url = image_url
        self.sunlight = sunlight
        self.water_needs = water_needs
        self.temperature_range = temperature_range
        self.status = status
        self.created_at = datetime.now().isoformat()

    def save(self):
        plants_collection.insert_one(self.__dict__)
    
    @staticmethod
    def get_by_id(plant_id):
        plant_data = plants_collection.find_one({'_id': ObjectId(plant_id)})
        if plant_data and plant_data['status'] == 'active':
            return Plant(**plant_data)
        else:
            return None
        
    @staticmethod
    def get_all():
        # Query the database to fetch all plants with status active
        plants = plants_collection.find({'status': 'active'}, projection={"created_at": False})
        return [Plant(**plant) for plant in plants]

    @classmethod
    def deactivate_plant(cls, plant_id):
        try:
            result = plants_collection.update_one(
                {'_id': ObjectId(plant_id)},
                {'$set': {'status': 'inactive'}}
            )
            if result.modified_count == 1:
                return True, "Plant has been successfully deactivated."
            else:
                return False, "No changes made. Plant may already be inactive or doesn't exist."
        except Exception as e:
            return False, str(e)
        
class CareJournalEntry:
    def __init__(self, _id, plant_id, user_id, entry_date, notes, images, status):
        self._id = _id
        self.plant_id = plant_id
        self.user_id = user_id
        self.entry_date = entry_date
        self.notes = notes
        self.images = images
        self.status = status
    

    @staticmethod
    def get_entries_by_plant_id(plant_id):
        # Query the database to fetch care journal entries for the given plant_id
        entries = entries_collection.find({'plant_id': ObjectId(plant_id)})
        return [CareJournalEntry(**entry) for entry in entries]
    
    def to_dict(self):
        return {
            '_id': str(self._id),  # ObjectId zu string konvertieren
            'plant_id': str(self.plant_id),
            'user_id': str(self.user_id),
            'entry_date': self.entry_date.isoformat() if self.entry_date else None,
            'notes': self.notes,
            'images': self.images,
            'status': self.status
        }
    
    @staticmethod
    def get_by_id(entry_id):
        entry_data = entries_collection.find_one({'_id': ObjectId(entry_id)})
        if entry_data:
            return CareJournalEntry(**entry_data)
        return None

    @classmethod
    def deactivate_entry(cls, entry_id):
        # Logik zum Deaktivieren des Eintrags
        result = entries_collection.update_one(
            {'_id': ObjectId(entry_id)},
            {'$set': {'status': 'inactive'}}
        )
        if result.modified_count == 1:
            return True, "Eintrag wurde erfolgreich deaktiviert."
        else:
            return False, "Keine Änderungen vorgenommen. Eintrag ist bereits deaktiviert oder existiert nicht."

    @classmethod
    def update_entry(cls, entry_id, data):
        # Logik zum Aktualisieren des Eintrags
        result = entries_collection.update_one(
            {'_id': ObjectId(entry_id)},
            {'$set': data}
        )
        if result.modified_count == 1:
            return True, "Eintrag wurde erfolgreich geändiert."
        else:
            return False, "Keine Änderungen vorgenommen. Eintrag ist bereits geändert oder existiert nicht."
    
    def save(self):
        entries_collection.insert_one(self.__dict__)

class Image:
    def __init__(self, _id, filename, url, uploaded_by, uploaded_at):
        self._id = _id
        self.filename = filename
        self.url = url
        self.uploaded_by = uploaded_by
        self.uploaded_at = uploaded_at