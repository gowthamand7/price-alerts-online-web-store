import uuid

from src.common.database import Database
from src.common.utils import Utils
import src.models.users.errors as usererrors


class User(object):
    def __init__(self, email, password, _id = None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<User : {} >".format(self.email)

    @staticmethod
    def is_login_valid(email,password):
        """
        check whether the given email and password is valid as per our DB
        :param email: email
        :param password: A sha512 hashed password
        :return: True if valid or False
        """
        user_data = Database.findOne(collection='users', query={"email": email}) # password in pbkdf2_sha512 encrypted format
        if user_data is None:
            raise usererrors.UserNotExistsError("your user does not exists", 404)

        if Utils.check_hashed_password(password,user_data['password']) is not True:
            raise usererrors.IncorrectPasswordError("Given password for a user is not a valid", 403)

        return True

    @staticmethod
    def register_user(email, password):
        """
        1. check the given email id ans password match the requirements
        2. check the user already exists
        3. if No insert and return True
        4. else raise error
        :param email:
        :param password:
        :return:
        """
        if Utils.is_valid_email(email) is False:
            raise usererrors.InvalidInput("Given email is not in a valid format", 400)

        if Utils.is_valid_password(password) is False:
            raise usererrors.InvalidInput("Given password is not in a valid format", 400)

        if User.get_by_email(email) is None:
            new_user = User(email, Utils.hash_password(password))
            new_user.save_to_db()
            return True
        else:
            raise usererrors.UserAlreadyExists("User already exists", 409)

    @classmethod
    def get_by_email(cls, email):
        user = Database.findOne(collection='users',query={'email': email})
        if user is not None:
            return cls(**user)

    def save_to_db(self):
        Database.insert(collection='users', data=self.json())

    def json(self):
        return {
            "email":self.email,
            "password":self.password,
            "_id":self._id
        }
