
from spectrobot.library.main import db

class Parser:
    host = None
    page = None
    cache = None
    visit = None
    errors = None
    browser = None
    def set_host(self):
        from spectrobot.model.host import Host
        self.host = Host(host=self.browser.host)
        if not self.host.id:
            self.host.save()
    def set_page(self):
        if self.host.id:
            from spectrobot.model.page import Page
            self.page = Page(host_id=self.host.id, path=self.browser.path)
            if not self.page.id:
                self.page.save()
    def set_queue(self):
        from spectrobot.model.queue import Queue
        q = Queue()
        q.parse(self.browser)
    def set_visit(self):
        if self.page.id:
            from spectrobot.model.visit import Visit
            self.visit = Visit(page_id=self.page.id, status=self.browser.status)
            if not self.visit.id:
                self.visit.save()
    def set_errors(self):
        if self.visit.id:
            from spectrobot.model.errors import Errors
            self.errors = Errors(visit_id=self.visit.id, errors=self.browser.validator.errors)
            self.errors.save()
    def set_cache(self):
        if self.visit.id:
            from spectrobot.model.cache import Cache
            self.cache = Cache(visit_id=self.visit.id, page_id=self.page.id, browser=self.browser)
            if not self.cache.id:
                self.cache.save()
    def set_from_browser(self, b):
        self.browser = b
        self.set_host()
        self.set_page()
        self.set_queue()
        self.set_visit()
        if self.browser.validate:
            self.set_errors()
        self.set_cache()
        return True
