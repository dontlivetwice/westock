import json
from utils.time import Time
from core.models.interest import Interest
from core.managers.base_manager import Manager, ManagerException


class InterestManagerException(ManagerException):
    pass


class InterestManager(Manager):
    def __init__(self):
        super(InterestManager, self).__init__('interests')

    @classmethod
    def _serialize(cls, interest):
        if interest:
            return (Time.get_utc_time(), interest.get('name'), interest.get('image_url'),
                    json.dumps(interest.get('body')), interest.get('followers'))

        return ()

    @classmethod
    def _deserialize(cls, obj):
        if obj:
            args = {}

            count = 0

            for var in obj:
                args.update({Interest.DB_MAPPINGS[count]: var})
                count += 1

            return Interest(**args)

        return None

    def add_one(self, interest):
        query = ''' (access_time, name, image_url, body, followers) VALUES (%s, %s, %s, %s, %s)'''

        return self.db_manager.add_one(query, InterestManager._serialize(interest))
