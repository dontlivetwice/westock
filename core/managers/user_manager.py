from utils.time import Time

from collections import defaultdict

from core.models.stock import Stock
from core.models.user import User

from core.managers.base_manager import Manager, ManagerException
from core.managers.db_manager import DBManager
from core.utils import password_utils

class UserManagerException(ManagerException):
	pass


class UserManager(Manager):
	def __init__(self, **kwargs):
		self.db_manager = DBManager('users')

	@classmethod
	def _deserialize_user(cls, user):
		if user:
			args = {}

			count = 0

			for var in user:
				args.update({User.DB_MAPPINGS[count]: var})
				count = count + 1

			return User(**args)

		return None

	@classmethod
	def _serialize_user(cls, user):
		if user:
			return (user.get('id'), Time.get_time(), user.get('username'), user.get('first_name'), user.get('last_name'),
			user.get('email'), password_utils.encrypt_password(user.get('password')), user.get('about'), user.get('location'), user.get('website'),
			user.get('image_url'), user.get('gender'), user.get('birthday'), user.get('stock_list'))

		return ()

	def add_one(self, user):
		query = ''' (user_id, access_time, username, name, last_name, email, password, about, 
			location, website, image_url, gender, birthday, body) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
		
		return self.db_manager.add_one(query, UserManager._serialize_user(user))

	def update_one(self, user):
		if user:
			query =  " "

			serialized_user = UserManager._serialize_user(user)

			count = 0

			for value in serialized_user:
				if User.DB_MAPPINGS[count] not in User.unmutable_fields():
					query += "%s = \"%s\", " % (User.DB_MAPPINGS[count], value)
				
				count = count + 1

			query = query[:-2]

			query =  query + ''' WHERE user_id=%s''' % user.get('id')

			return self.db_manager.update_one(query)

		raise UserManagerException('UserIsNoneError')

	def get_one(self, **kwargs):
		query =  ""

		for key, value in kwargs.items():
			query += "%s = \"%s\" AND " % (key, value)

		query = query[:-5]

		user = self.db_manager.get_one(query)

		return UserManager._deserialize_user(user)

	def delete_one(self, user):
		if user:
			query = "user_id = \"%s\"" % user.get('id')

			return self.db_manager.delete_one(query)

		raise UserManagerException('UserIsNoneError')

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
