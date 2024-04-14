from flask_login import UserMixin
from pymongo import MongoClient
import bcrypt
from bson import ObjectId

# Create a connection to MongoDB
client = MongoClient('mongodb+srv://jawohi_gs:myedMz0mDterDuRl@grasscluster.bcqofix.mongodb.net/')
db = client['Grassspot_DB']  
users_collection = db['users']  


class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data.get('_id')) if user_data.get('_id') else None
        self.username = user_data['username']
        self.password_hash = user_data['password']

    def set_password(self, password):
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.password_hash = password_hash

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash)

    def save(self):
        user_data = {
            'username': self.username,
            'password': self.password_hash
        }
        if self.id:
            users_collection.update_one({'_id': ObjectId(self.id)}, {'$set': user_data})
        else:
            result = users_collection.insert_one(user_data)
            self.id = str(result.inserted_id)

    @staticmethod
    def get(user_id):
        print("User ID:", user_id)
        user_id = ObjectId(user_id)
        user_data = users_collection.find_one({'_id': user_id})
        print("User data:", user_data)
        if user_data:
            return User(user_data)
        return None

    @staticmethod
    def get_by_username(username):
        user_data = users_collection.find_one({'username': username})
        if user_data:
            return User(user_data)
        return None

    def __repr__(self):
        return f"User(id={self.id}, username={self.username})"
