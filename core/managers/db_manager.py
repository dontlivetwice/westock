import memcache
import MySQLdb
from utils.decorators import memoized_property
import settings.prod as prod


class DBManagerException():
    pass


class DBManager(object):
    def __init__(self, db_name):
        self.db.autocommit(True)
        self.cursor = self.db.cursor()
        self.table_name = 'stockinterest.%s' % db_name
        self.CREATE_TEMPLATE = '''INSERT INTO ''' + self.table_name
        self.UPDATE_TEMPLATE = '''UPDATE ''' + self.table_name + ''' SET '''
        self.SELECT_TEMPLATE = '''SELECT * FROM ''' + self.table_name + ''' WHERE '''
        self.SELECT_MANY_TEMPLATE = '''SELECT * FROM ''' + self.table_name
        self.DELETE_TEMPLATE = '''DELETE FROM ''' + self.table_name + ''' WHERE '''
        self.expiration = prod.WS_MEMCACHE_EXPIRATION

    @memoized_property
    def db(self):
        return MySQLdb.connect(user=prod.WS_DB_USER, passwd=prod.WS_DB_PASSWORD, db=prod.WS_DB_NAME)

    @memoized_property
    def mc(self):
        return memcache.Client([prod.WS_MEMCACHE_SERVER + ':' + prod.WS_MEMCACHE_PORT], debug=prod.WS_MEMCACHE_DEBUG)

    def add_one(self, query, query_data):
        ret = self.cursor.execute(self.CREATE_TEMPLATE + query, query_data)
        self.db.commit()
        return ret

    def update_one(self, query):
        ret = self.cursor.execute(self.UPDATE_TEMPLATE + query)
        self.db.commit()
        return ret

    def get_one(self, query):
        ret = self.cursor.execute(self.SELECT_TEMPLATE + query)

        if ret:
            return self.cursor.fetchone()

        return None

    def get_many(self, limit=None, query=None):
        if query:
            ret = self.cursor.execute(self.SELECT_TEMPLATE + query)
        else:
            ret = self.cursor.execute(self.SELECT_MANY_TEMPLATE)

        if ret:
            if limit:
                return self.cursor.fetchmany(size=limit)
            return self.cursor.fetchall()

        return None

    def delete_one(self, query):
        ret = self.cursor.execute(self.DELETE_TEMPLATE + query)
        self.db.commit()
        return ret
