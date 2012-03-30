
import sys
sys.path = sys.path + ['/home/develop/python']

import spectrobot.library.main

global is_work
is_work = 1

from spectrobot.model.bot import Bot

b = Bot()
b.loop()
