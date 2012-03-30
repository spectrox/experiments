
from spectrobot.library.main import db

class Page:
    id = None
    host_id = None
    path = None
    def __init__(self, id='', host_id='', path=''):
        self.get(id, host_id, path)
    def get(self, id='', host_id='', path=''):
        if id or path:
            if id:
                db.query('SELECT `id`,`host_id`,`path` FROM `pages` WHERE `id`='+db.escape_string(str(id)))
                res = db.store_result()
                if res.num_rows() == 1:
                    self.id, self.host_id, self.path = res.fetch_row()[0]
                elif host_id and path:
                    self.host_id = host_id
                    self.path = path
            elif host_id and path:
                db.query('SELECT `id`,`host_id`,`path` FROM `pages` WHERE `host_id`="'+db.escape_string(str(host_id))+'" AND `path`="'+db.escape_string(path)+'"')
                res = db.store_result()
                if res.num_rows() == 1:
                    self.id, self.host_id, self.path = res.fetch_row()[0]
                else:
                    self.host_id = host_id
                    self.path = path
    def save(self):
        if self.host_id and self.path:
            if self.id:
                db.query('UPDATE `pages` SET `host_id`="'+db.escape_string(str(self.host_id))+'", `path`="'+db.escape_string(self.path)+'" WHERE `id`='+db.escape_string(str(self.id)))
                return True
            else:
                db.query('INSERT into `pages` (`host_id`,`path`) VALUES ("'+db.escape_string(str(self.host_id))+'","'+db.escape_string(self.path)+'")')
                self.id = db.insert_id()
                return True
        else:
            return False
    def delete(self):
        if self.id:
            db.query('DELETE from `pages` WHERE `id`='+db.escape_string(str(self.id)))
            return True
        else:
            return False
