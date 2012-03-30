
from spectrobot.library.main import db

class Cache:
    id = None
    visit_id = None
    page_id = None
    encoding = None
    doctype = None
    validity = None
    content = None
    headers = None
    def __init__(self, id='', visit_id='', page_id='', browser=''):
        self.get(id, visit_id, page_id, browser)
    def get(self, id='', visit_id='', page_id='', browser=''):
        if id:
            db.query('SELECT `id`,`visit_id`,`page_id`,`encoding`,`doctype`,`validity`,`content` FROM `cache` WHERE `id`='+db.escape_string(str(id)))
            res = db.store_result()
            if res.num_rows() == 1:
                self.id, self.visit_id, self.page_id, self.encoding, self.doctype, self.validity, self.content = res.fetch_row()[0]
        elif visit_id and page_id and browser:
            self.visit_id = visit_id
            self.page_id = page_id
            self.headers = browser.headers
            if browser.validate:
                self.encoding = browser.validator.charset
                self.doctype = browser.validator.doctype
                if browser.validator.validity:
                    self.validity = int(browser.validator.validity)
            self.content = browser.page
    def save(self):
        if self.visit_id and self.page_id:
            if self.id:
                db.query('UPDATE `cache` SET `visit_id`="'+db.escape_string(str(self.visit_id))+'", `page_id`="'+db.escape_string(str(self.page_id))+'", `encoding`="'+db.escape_string(self.encoding)+'", `doctype`="'+db.escape_string(self.doctype)+'", `validity`="'+db.escape_string(str(self.validity))+'", `headers`="'+db.escape_string(str(self.headers))+'", `content`="'+db.escape_string(self.content)+'" WHERE `id`='+db.escape_string(str(self.id)))
                return True
            else:
                db.query('INSERT into `cache` (`visit_id`,`page_id`,`encoding`,`doctype`,`validity`,`content`,`headers`) VALUES ("'+db.escape_string(str(self.visit_id))+'","'+db.escape_string(str(self.page_id))+'","'+db.escape_string(self.encoding)+'","'+db.escape_string(self.doctype)+'","'+db.escape_string(str(self.validity))+'","'+db.escape_string(self.content)+'","'+db.escape_string(str(self.headers))+'")')
                self.id = db.insert_id()
                return True
        else:
            return False
    def delete(self):
        if self.id:
            db.query('DELETE from `cache` WHERE `id`='+db.escape_string(str(self.id)))
            return True
        else:
            return False
