from app.config import mongo
from werkzeug.security import generate_password_hash, check_password_hash

class UserModel:
    @staticmethod
    def create_user(data):
        hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
        print('hashed_password - ', hashed_password)
        user = {
            "username": data["username"],
            "email": data["email"],
            "password": hashed_password
        }
        return mongo.db.users.insert_one(user).inserted_id

    @staticmethod
    def update_user(user_id, update_fields):
        return mongo.db.users.update_one({"_id": user_id}, {"$set": update_fields})

    @staticmethod
    def find_user_by_email(email):
        return mongo.db.users.find_one({"email": email})

    @staticmethod
    def find_user_by_id(user_id):
        return mongo.db.users.find_one({"_id": user_id})

    @staticmethod
    def check_password(user, password: str) -> bool:
        """
        Verify the user's password.
        :param user: User document containing the hashed password
        :param password: Plain text password to verify
        :return: True if valid, False otherwise
        """
        return check_password_hash(user["password"], password)