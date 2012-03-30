
import re
import httplib
import time

class Browser:
    host = ''
    port = ''
    path = ''
    page = ''
    headers = ''
    charset = ''
    validate = 0
    validity = 0
    doctype = ''
    hnd = None
    errors = None
    status = None
    validator = None
    content_type = None
    def __init__(self, host='', port='', path='', url='', validate=''):
        self.validate = validate
        if url:
            if not self.parse_url(url):
                return False
        elif host:
            self.host = host
            if port:
                self.port = port
            else:
                self.port = 80
            self.path = path
            if not self.path:
                self.path = '/'
    def get_url(self):
        url = 'http://'+self.host
        if self.port!=80:
            url = url+':'+self.port
        url = url + self.path
        return url
    def set_url(self, host='', port='', path='', url='', validate=''):
        self.__init__(host, port, path, url, validate)
    def parse_url(self, url):
        import re
        matches = re.match('^(?P<type>[a-zA-Z]\w+)://(?P<server>[^/:]+)(:*)(?P<port>[0-9]*)(?P<path>.*)', url)
        try:
            server_type = matches.group('type')
            if (server_type!='http'):
                return False
            self.host = matches.group('server')
            self.path = matches.group('path')
            if self.path.find('#') != -1:
                self.path = self.path.split('#')[0]
            self.port = matches.group('port')
            if not self.path:
                self.path = '/'
            if not self.port:
                self.port = 80
        except:
            if self.host and self.path:
                self.port = 80
            else:
                return False
        return True
    def connect(self):
        if (self.port==80):
            self.hnd = httplib.HTTP(self.host)
            if self.hnd:
                return True
#        import socket
#        self.hnd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#        self.hnd.connect((self.host, self.port))
    def send_headers(self,recur=0):
        print 'sending headers' # debugging
        try:
            self.hnd.putrequest('GET', self.path)
            self.hnd.putheader('Host', self.host)
            self.hnd.putheader('Connection', 'Keep-alive')
            self.hnd.putheader('Accept', '*/*')
            self.hnd.putheader('From', 'spectrobot(at)spectrox.ru')
            self.hnd.putheader('User-Agent', 'Mozilla/5.0 (compatible; Spectrobot/0.1; +http://spectrox.ru)')
            self.hnd.putheader('Accept-Encoding', 'gzip,deflate')
            self.hnd.endheaders()
            return True
        except:
            self.hnd.close()
            if recur == 0:
                time.sleep(1)
                if self.connect():
                    recur = recur+1
                    return self.send_headers(recur)
            return False
    def read_data(self,recur=0):
        try:
            self.status, returnmsg, self.headers = self.hnd.getreply()
        except:
            self.hnd.close()
            if recur == 0:
                time.sleep(1)
                if self.connect():
                    if self.send_headers():
                        recur = recur+1
                        return self.read_data(recur)
            return False
        self.headers = str(self.headers).replace('\r','')
        if self.status == 200:
            data = re.search('Content-Type: (?P<type>[^;\n]*)', str(self.headers))
            if data and data.group('type'):
                if data.group('type') == 'text/html':
                    self.content_type = 'text/html'
                elif data.group('type') == 'plain/text':
                    self.content_type = 'plain/text'
                    self.validate = False
                elif data.group('type') == 'application/soap+xml':
                    if self.host != 'validator':
                        return False
                else:
                    return False
                try:
                    f = self.hnd.getfile()
                    self.page = f.read()
                    self.hnd.close()
                except:
                    self.hnd.close()
                    if recur == 0:
                        time.sleep(1)
                        if self.connect():
                            if self.send_headers():
                                recur = recur+1
                                return self.read_data(recur)
                    return False
                return True
            else:
                return False
        elif self.status == 301:
            data = re.search('Location: (?P<url>[^\n]*)', str(self.headers))
            if data and recur < 2:
                self.set_url(url=data.group('url'),validate=self.validate)
                if self.connect():
                    if self.send_headers():
                        recur = recur+1
                        if self.read_data(recur):
                            return True
                return False
        else:
            return False
        return True
    def do_validate(self, host='', port='', path=''):
        if port!=80:
            host = host+':'+str(port)
        uri = 'http://validator/check?uri=http://'+host+path+'&output=soap12'
        self.validator = Browser(url=uri)
        self.validator.load()
        if self.validator.page:
            data = re.search('<m:validity>(?P<value>.*?)</m:validity>',
                             self.validator.page)

            if data and data.group('value'):
                self.validator.validity = data.group('value')
                if self.validator.validity=='true':
                    self.validator.validity = 1
                else:
                    self.validator.validity = 0
            else:
                self.validator.validity = 0

            data = re.search('<m:doctype>(?P<value>.*?)</m:doctype>',
                             self.validator.page)
            if data and data.group('value'):
                self.validator.doctype = data.group('value')

            data = re.search('<m:charset>(?P<value>.*?)</m:charset>',
                             self.validator.page)
            if data and data.group('value'):
                self.validator.charset = data.group('value')

            data = re.search('<m:errorlist>(?P<value>.*?)</m:errorlist>',
                             self.validator.page, re.S)
            if data and data.group('value'):
                self.validator.errors = re.findall('<m:messageid>(?P<id>[0-9]+)</m:messageid>', data.group('value'))
            return True
        return False
    def load(self):
        if self.connect():
            if self.send_headers():
                if self.read_data():
                    if self.validate:
                        self.do_validate(self.host, self.port, self.path)
                    return True
                else:
                    return False
