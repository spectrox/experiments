
from spectrobot.library import mysql

config = {
          'db_host': 'localhost',
	  'db_name': 'spectrobot',
          'db_user': 'spectrobot',
          'db_passwd': ''
          }

#class Main:
def init():
    database()
def database():
    global db, config
    db = mysql.MySQL()
    db.connect(db_host=config['db_host'], db_user=config['db_user'],
               db_passwd=config['db_passwd'], db_name=config['db_name'])

init()
