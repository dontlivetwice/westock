from utils.time import Time

from core.models.user import User
from core.managers.base_manager import Manager, ManagerException
from core.utils import password_utils


class UserManagerException(ManagerException):
    pass


class UserManager(Manager):
    def __init__(self):
        super(UserManager, self).__init__('users')

    @classmethod
    def _serialize(cls, user):
        if user:
            return (Time.get_time(), user.get('username'), user.get('first_name'),
                    user.get('last_name'), user.get('email'), password_utils.encrypt_password(user.get('password')),
                    user.get('about'), user.get('location'), user.get('website'), user.get('image_url'),
                    user.get('gender'), user.get('birthday'), user.get('stock_list'))

        return ()

    @classmethod
    def _deserialize(cls, obj):
        """ Deserializes the passed in object based on DB mapping """
        if obj:
            args = {}

            count = 0

            for var in obj:
                args.update({User.DB_MAPPINGS[count]: var})
                count += 1

            return User(**args)

        return None

    def add_one(self, user):
        query = ''' (access_time, username, first_name, last_name, email, password, about, location, website,
        image_url, gender, birthday, body) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''

        return self.db_manager.add_one(query, UserManager._serialize(user))

    def login(self, username_or_email, password):
        if "@" in username_or_email:
            user = self.get_one(email=username_or_email)
        else:
            user = self.get_one(username=username_or_email)

        if not user:
            return None

        if not user.check_password(password):
            return None

        return user
