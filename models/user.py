from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
from app import mongo

class User:
    @staticmethod
    def get_all_users():
        return mongo.db.users.find({})

    @staticmethod
    def get_user_by_id(user_id):
        return mongo.db.users.find_one({"_id": ObjectId(user_id)})

    @staticmethod
    def create_user(data):
        data['password'] = generate_password_hash(data['password'])
        return mongo.db.users.insert_one(data)

    @staticmethod
    def update_user(user_id, data):
        if 'password' in data:
            data['password'] = generate_password_hash(data['password'])
        return mongo.db.users.update_one({"_id": ObjectId(user_id)}, {"$set": data})

    @staticmethod
    def delete_user(user_id):
        return mongo.db.users.delete_one({"_id": ObjectId(user_id)})
