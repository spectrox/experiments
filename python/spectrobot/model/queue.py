
try:
    from spectrobot.library.main import db
except:
    pass
import re

class Queue:
    query = None
    def next(self):
        db.query('SELECT * from `queue` WHERE `finished`=0 ORDER by `id` ASC LIMIT 1')
        res = db.store_result()
        if res.num_rows() == 1:
            self.query = res.fetch_row(how=1)[0]
            return self.query
        else:
            return False
    def ping(self):
        db.ping()
    def parse(self, browser):
        #data = re.findall('<a((([^=>]+)(=(([\'"]([^\'">]*)[\'"])|([^\'"\s\n>]*))*))*)>', page, re.S)
        data = re.findall('href=([\'"][^\'"]+[\'"]|[^\n\s>]*)', browser.page, re.S)
        if data:
            for path in data:
                i = data.index(path)
                if data.count(data[i]) > 1:
                    data[i] = ''
                elif data[i].strip() != '':
                    data[i] = re.sub(r'^[\'"](.*)[\'"]$',r'\1',data[i],re.S).strip()
                    mail = re.search('mailto:(?P<email>[a-zA-Z0-9@_\-\.]*)',data[i].strip(),re.S)
                    if mail:
                        print 'mailto founded' # debugging
                        if mail.group('email'):
                            db.query('INSERT into `emails` (`time`,`url`,`email`) VALUES (UNIX_TIMESTAMP(),"'+db.escape_string(browser.get_url())+'","'+db.escape_string(mail.group('email'))+'")')
                            print 'email inserted' # debugging
                    else:
                        if not re.search('^http://',data[i]):
                            if len(data[i]) > 0 and data[i][0] != '/':
                                data[i] = '/'+data[i]
                            data[i] = 'http://'+browser.host+data[i]
                        if data.count(data[i]) == 1:
                            db.query('SELECT `id` from `queue` WHERE `url`="'+db.escape_string(data[i])+'" AND `created`>UNIX_TIMESTAMP()-1209600')
                            if not db.store_result().num_rows():
                                db.query('INSERT into `queue` (`created`,`url`) VALUES (UNIX_TIMESTAMP(),"'+db.escape_string(data[i])+'")')
                        elif data.count(data[i]) > 1:
                            data.remove(data[i])
    def finished(self):
        db.query('UPDATE `queue` SET `finished`=UNIX_TIMESTAMP() WHERE `id`='+db.escape_string(str(self.query['id'])))
    def aborted(self):
        db.query('UPDATE `queue` SET `finished`=-1 WHERE `id`='+db.escape_string(str(self.query['id'])))
