
from spectrobot.library.main import db
from spectrobot.model.browser import Browser
from spectrobot.model.parser import Parser
from spectrobot.model.queue import Queue
from spectrobot.init import is_work

import time

class Bot:
    def parse(self, query):
        if query['url']:
            print query['url'] # debugging
            b = Browser(url=query['url'], validate=1)
            if b.load():
                print b.status # debugging
                if b.status == 200:
                    p = Parser()
                    if p.set_from_browser(b):
                        return True
                    else:
                        return False
    def loop(self):
        q = Queue()
        while is_work == 1:
            q.ping()
            query = q.next()
            if query:
                if self.parse(query):
                    q.finished()
                else:
                    q.aborted()
            else:
                time.sleep(1)