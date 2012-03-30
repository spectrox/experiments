
from spectrobot.library.main import db
import re

class Host:
    id = None
    host = None
    def __init__(self, id='', host=''):
        self.get(id, host)
    def get(self, id='', host=''):
        if id or host:
            if id:
                db.query('SELECT `id`,`host` FROM `hosts` WHERE `id`='+db.escape_string(str(id)))
                res = db.store_result()
                if res.num_rows() == 1:
                    self.id, self.host = res.fetch_row()
                elif host:
                    self.host = host
            elif host:
                host = re.sub('^www.', '', host)
                db.query('SELECT `id`,`host` FROM `hosts` WHERE `host`="'+db.escape_string(host)+'"')
                res = db.store_result()
                if res.num_rows() == 1:
                    self.id, self.host = res.fetch_row()[0]
                else:
                    self.host = host
    def save(self):
        if self.host:
            if self.id:
                db.query('UPDATE `hosts` SET `host`="'+db.escape_string(self.host)+'" WHERE `id`='+db.escape_string(str(self.id)))
                return True
            else:
                db.query('INSERT into `hosts` (`host`) VALUES ("'+db.escape_string(self.host)+'")')
                self.id = db.insert_id()
                return True
        else:
            return False
    def delete(self):
        if self.id:
            db.query('DELETE from `hosts` WHERE `id`='+db.escape_string(str(self.id)))
            return True
        else:
            return False
