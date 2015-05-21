from utils.time import Time

from collections import defaultdict

from core.models.stock import Stock
from core.models.user import User

from core.managers.db_manager import DBManager

class UserManager(object):
	def __init__(self):
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
			user.get('email'), user.get('password'), user.get('about'), user.get('location'), user.get('website'),
			user.get('image_url'), user.get('gender'), user.get('birthday'), '')

		return ()

	def add_one(self, user):
		query = ''' (user_id, access_time, username, name, last_name, email, password, about, 
			location, website, image_url, gender, birthday, body) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
		
		return self.db_manager.add_one(query, UserManager._serialize_user(user))

	def update_one(self, user_id, **kwargs):
		query =  " "

		for key, value in kwargs.items():
			query += "%s = \"%s\", " % (key, value)

		query = query[:-2]

		query =  query + ''' WHERE user_id=%s''' % user_id

		return self.db_manager.update_one(query)

	def get_one(self, **kwargs):
		query =  ""

		for key, value in kwargs.items():
			query += "%s = \"%s\" AND " % (key, value)

		query = query[:-5]

		user = self.db_manager.get_one(query)

		return UserManager._deserialize_user(user)

	def delete_one(self, **kwargs):
		query =  ""

		for key, value in kwargs.items():
			query += "%s = \"%s\" AND " % (key, value)

		query = query[:-5]

		return self.db_manager.delete_one(query)

