
from spectrobot.library.main import db

class Errors:
    visit_id = None
    errors = None
    def __init__(self, visit_id='', errors=''):
        self.get(visit_id, errors)
    def get(self, visit_id='', errors=''):
        if visit_id and not errors:
            self.visit_id = visit_id
            db.query('SELECT `id`,`visit_id`,`error_id` FROM `page_errors` WHERE `visit_id`='+db.escape_string(str(visit_id)))
            res = db.store_result()
            if res.num_rows():
                while True:
                    row = res.fetch_row()[0]
                    if not row:
                        break
                    self.errors = self.errors + [res.fetch_row()[0][2]]
        elif visit_id and errors:
            self.visit_id = visit_id
            self.errors = errors
    def save(self):
        if self.visit_id and self.errors:
            db.query('DELETE from `page_errors` WHERE `visit_id`='+db.escape_string(str(self.visit_id)))
            for er in self.errors:
                db.query('INSERT into `page_errors` (`visit_id`,`error_id`) VALUES ("'+db.escape_string(str(self.visit_id))+'","'+db.escape_string(str(er))+'")')
            return True
        else:
            return False
    def delete(self):
        if self.visit_id:
            db.query('DELETE from `page_errors` WHERE `visit_id`='+db.escape_string(str(self.visit_id)))
            return True
        else:
            return False
