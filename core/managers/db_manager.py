import MySQLdb

class DBManager(object):
    def __init__(self, db_name):
        self.db = MySQLdb.connect(user='db_user', passwd='db_pass', db='stockinterest')
        self.cursor = self.db.cursor()
        self.table_name = 'stockinterest.%s' % db_name
        self.CREATE_TEMPLATE = '''INSERT INTO ''' + self.table_name
        self.UPDATE_TEMPLATE = '''UPDATE ''' + self.table_name + ''' SET '''
        self.SELECT_TEMPLATE = '''SELECT * FROM ''' + self.table_name + ''' WHERE '''
        self.DELETE_TEMPLATE = '''DELETE FROM ''' + self.table_name + ''' WHERE '''

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

    def get_many(self, query, limit=None):
        ret = self.cursor.execute(self.SELECT_TEMPLATE + query)

        if ret:
            if limit:
                return self.cursor.fetchmany(size=limit)
            return self.cursor.fetchall()

        return None

    def delete_one(self, query):
        ret = self.cursor.execute(self.DELETE_TEMPLATE + query)
        self.db.commit()
        return ret
