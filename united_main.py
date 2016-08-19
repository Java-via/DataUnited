# _*_ coding: utf-8 _*_

import logging
import sys
import time
from apps_united.united_for_basic import basic_catchapps
# from apps_united.unitedforadd_v00 import add_catchapps
from apps_united.united_for_addi import addi_catchapps

assert sys.argv[1] in ["basic", "additional"]
if sys.argv[1] == "basic":
    basic_catchapps()
elif sys.argv[1] == "additional":
    today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    addi_catchapps("2016-08-18")
else:
    logging.error("united error: parameters error")
    pass
