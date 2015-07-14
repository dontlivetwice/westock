from core.models.user_interest_model import UserInterest
from core.managers.base_manager import Manager, ManagerException


class UserInterestManagerException(ManagerException):
    pass


class UserInterestManager(Manager):
    def __init__(self):
        super(UserInterestManager, self).__init__('users_interests')

    @classmethod
    def _serialize(cls, user_interest):
        if user_interest:
            return user_interest.get('user_id'), user_interest.get('interest_id')

        return ()

    @classmethod
    def _deserialize(cls, obj):
        """ Deserializes the passed in object based on DB mapping """
        if obj:
            args = {}

            count = 0

            for var in obj:
                args.update({UserInterest.DB_MAPPINGS[count]: var})
                count += 1

            return UserInterest(**args)

        return None

    def add_one(self, user_interest):
        query = ''' (user_id, interest_id) VALUES (%s, %s)'''
        return self.db_manager.add_one(query, UserInterestManager._serialize(user_interest))

    def get_interests_for_user(self, user_id, limit=100):
        query = "user_id = \"%s\"" % user_id

        users_interests = self.db_manager.get_many(limit, query)

        result_list = []

        if users_interests:
            for interest in users_interests:
                result_list.append(UserInterestManager._deserialize(interest))

        return result_list
