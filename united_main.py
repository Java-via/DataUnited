# _*_ coding: utf-8 _*_

import logging
import sys
import time
from apps_united.unitedbasic_v01 import basic_catchapps
from apps_united.unitedforadd_v00 import add_catchapps

assert sys.argv[1] in ["basic", "additional"]
if sys.argv[1] == "basic":
    today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    basic_catchapps("2016-07-30")
elif sys.argv[1] == "additional":
    today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    add_catchapps(today)
else:
    logging.error("united error: parameters error")
    pass
