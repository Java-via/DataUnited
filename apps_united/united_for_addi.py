# _*_ coding: utf-8 _*_

import pymysql
import logging
from .united_utils import *


def addi_catchapps(date):

    conn = pymysql.connect(host=DB_HOST, db=DB_DB, user=DB_USER, passwd=DB_PWD, charset=DB_CHARSET)
    cur = conn.cursor()
    sql = "SELECT a_pkgname, a_pkgname_list FROM t_apps_basic_united ORDER BY a_pkgname;"
    sql_addi = "SELECT * FROM t_apps_additional WHERE DATE(a_getdate) = %s AND a_pkgname in %s;"
    logging.debug("BASIC: start to select from basic_united")
    cur.execute(sql)
    logging.debug("BASIC: select from basic_united over, start to add to basic_pkg_list")
    basic_pkg_list = cur.fetchall()
    logging.debug("BASIC: basic_pkg_list has all data")
    for pkg_list in basic_pkg_list:
        logging.debug("ADDI: start to modify pkgname_list")
        pkg_name = get_string_split(pkg_list[1], (" ", "\n"), is_remove_empty=True)
        in_pkg = set(pkg_name)
        logging.debug("ADDI: in_pkg get all, start to insert select from additional")
        cur.execute(sql_addi, (date, in_pkg))
        for app in cur.fetchall():
            logging.debug("ENDING: get result")
            addi_app = init_addi_cur(app)
            logging.debug("ENDING: inserting to addi_united")
            sql_insert = "INSERT INTO t_apps_addi_united VALUES (%s, %s, %s, %s, %s, %s, %s, " \
                         "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
            cur.execute(sql_insert, addi_app)

    logging.debug("done")



