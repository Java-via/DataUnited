# _*_ coding: utf-8 _*_

import pymysql
import logging

logging.basicConfig(level=logging.DEBUG)

# ----server----
DB_HOST = "101.200.174.172"
DB_DB = "data_apps"
DB_USER = "dba_apps"
DB_PWD = "mimadba_apps"
DB_CHARSET = "utf8"


conn = pymysql.connect(host=DB_HOST, db=DB_DB, user=DB_USER, password=DB_PWD, charset=DB_CHARSET)
cur = conn.cursor()
sql = "SELECT a_pkgname, a_source, a_picurl FROM t_apps_additional WHERE DATE(a_getdate) = %s;"
logging.debug("start to select additional")
cur.execute(sql, "2016-08-15")
logging.debug("2016-08-15 data get")
app_add = cur.fetchall()
sql_up = "UPDATE t_apps_basic SET a_picurl = %s WHERE a_pkgname = %s AND a_source = %s;"
for app in app_add:
    logging.debug("update %s", app[0])
    cur.execute(sql_up, (app[2], app[0], app[1]))
conn.commit()
logging.debug("done")
