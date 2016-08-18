# _*_ coding: utf-8 _*_

"""
this model is aim to unit additional data of apps
"""

import logging
import pymysql
from .united_utils import *

# ----logging config----
logging.basicConfig(level=logging.DEBUG)


def add_catchapps(date):
    """
    unit data
    :param date: getdate of data
    :return: nothing
    """
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PWD, db=DB_DB, charset=DB_CHARSET)
    cur = conn.cursor()
    sql = "SELECT * FROM t_apps_additional WHERE DATE(a_getdate) = %s ORDER BY a_pkgname"
    cur.execute(sql, date)
    conn.commit()

    list_apps = cur.fetchall()
    if not list_apps:
        logging.error("today has no data")
        return

    list_resutl = []
    current_app = init_addi_cur(list_apps[0])

    for item in list_apps[1:]:
        if (current_app[0] == item[0]) or \
                ((samiliar(str(current_app[0]), str(item[0])) > 0.699) and samiliar(str(current_app[2]), str(item[1])) > 0.799):
            # same pkgname
            logging.debug("Pkgname compare: %s and %s is the same one", item[1], current_app[0])
            update_addi_cur(current_app, item)
        else:
            logging.debug("Pkgname compare: %s and %s is very different", item[1], current_app[0])
            list_resutl.append(current_app)
            current_app = init_addi_cur(item)

    for info in list_resutl:
        assert info, "info is null"
        logging.debug("Insert is running: %s", info[0])
        cur.execute("INSERT INTO t_apps_addi_united VALUES (%s, %s, %s, %s, %s, %s, %s, "
                    "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", info)
        conn.commit()
        assert cur, "Cursor happened something"
    return



