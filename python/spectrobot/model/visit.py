
from spectrobot.library.main import db

class Visit:
    id = None
    page_id = None
    status = None
    def __init__(self, id='', page_id='', status=''):
        self.get(id, page_id, status)
    def get(self, id='', page_id='', status=''):
        if id:
            db.query('SELECT `id`,`page_id`,`status` FROM `visits` WHERE `id`='+db.escape_string(str(id)))
            res = db.store_result()
            if res.num_rows() == 1:
                self.id, self.page_id, self.status = res.fetch_row()[0]
        elif page_id and status:
            self.page_id = page_id
            self.status = status
    def save(self):
        if self.page_id and self.status:
            if self.id:
                db.query('UPDATE `visits` SET `page_id`="'+db.escape_string(str(self.page_id))+'", `time`=UNIX_TIMESTAMP(), `status`="'+db.escape_string(str(self.status))+'" WHERE `id`='+db.escape_string(str(self.id)))
                return True
            else:
                db.query('INSERT into `visits` (`page_id`,`time`,`status`) VALUES ("'+db.escape_string(str(self.page_id))+'",UNIX_TIMESTAMP(),"'+db.escape_string(str(self.status))+'")')
                self.id = db.insert_id()
                return True
        else:
            return False
    def delete(self):
        if self.id:
            db.query('DELETE from `visits` WHERE `id`='+db.escape_string(str(self.id)))
            return True
        else:
            return False
