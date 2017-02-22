from passlib.hash import pbkdf2_sha512


class Utils(object):

    @staticmethod
    def hash_pasword(password):
        """
        Hashed a password using pbkdf2_sha512
        :param password: sha512 password from login or register
        :return: pbkdf2_sha512 encrypted password
        """
        return pbkdf2_sha512.encrypt(password)

    @staticmethod
    def check_hashed_password(password, hashed_password):
        """
        Check the password users sends and database password
        The database password is encrypted more than the user's password at this stage
        :param password: sha512 hashed password
        :param hashed_password: pbkdf2_sha512 encrypted password
        :return: True if password match else False
        """
        return pbkdf2_sha512.verify(password,hashed_password)