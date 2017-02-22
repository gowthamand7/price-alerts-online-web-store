import uuid
from src.common.database import Database
from src.common.utils import Utils
import src.models.users.errors as usererrors


class User(object):
    def __init__(self, email, password, _id):
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
        user_data = Database.findOne(collection='users', query={"email":email}) # password in pbkdf2_sha512 encrypted format
        if user_data is None:
            raise usererrors.UserNotExistsError("your user does not exists")

        if Utils.check_hashed_password(password,user_data['password']) is not True:
            raise usererrors.IncorrectPasswordError("Given password for a user is not a valid")

        return False

    def json(self):
        return {
            "email":self.email,
            "password":self.password,
            "_id":self._id
        }
