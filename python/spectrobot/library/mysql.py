
import _mysql

class MySQL:
    db = None
    hnd = None
    res = None
    db_host = ''
    db_name = ''
    db_user = ''
    db_passwd = ''
    def connect(self, db_host='', db_user='', db_passwd='', db_name=''):
        if db_host and db_user and db_passwd and db_name:
            self.db_host = db_host
            self.db_user = db_user
            self.db_passwd = db_passwd
            self.db_name = db_name
            self.db = _mysql.connect(db_host, db_user, db_passwd, db_name)
        elif self.db_host and self.db_user and self.db_passwd and self.db_name:
            self.db = _mysql.connect(self.db_host, self.db_user, self.db_passwd, self.db_name)
    def select_db(self, name):
        self.db.select_db(name)
    def insert_id(self):
        return self.db.insert_id()
    def character_set_name(self, name):
        return self.db.character_set_name(name)
    def query(self, query):
        self.db.query(query)
    def use_result(self):
        return self.db.use_result()
    def store_result(self):
        return self.db.store_result()
    def fetch_row(self, res):
        return res.fetch_row()
    def affected_rows(self):
        return self.db.affected_rows()
    def escape_string(self, string):
        return _mysql.escape_string(string)
#	def data_seek(self, res, row):
#		res.data_seek(row)
    def num_fields(self, res):
        return res.num_fields()
    def num_rows(self, res):
        return res.num_rows()
    def ping(self):
        if self.db:
            try:
                self.db.ping()
            except MySQLdb.OperationalError, message:
                self.db.close()
                self.db = None
        if self.db is None:
            self.connect()
    def close(self):
        self.db.close()
