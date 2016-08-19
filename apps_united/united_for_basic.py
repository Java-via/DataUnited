# _*_ coding: utf-8 _*_

"""
this model is aim to unit basic data of apps
"""

import logging
import pymysql
from .united_utils import *

# ----logging config----
logging.basicConfig(level=logging.DEBUG)


def basic_catchapps():
    """
    unit data
    :param date: getdate of data
    :return: nothing
    """
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PWD, db=DB_DB, charset=DB_CHARSET)
    cur = conn.cursor()
    sql = "SELECT * FROM t_apps_basic ORDER BY a_pkgname;"
    sql_basic_united = "SELECT a_pkgname FROM t_apps_basic_united;"
    logging.debug("Select from basic begin")
    cur.execute(sql)
    logging.debug("Select from basic end")
    list_apps = cur.fetchall()

    logging.debug("Select from basic_united begin")
    cur.execute(sql_basic_united)
    logging.debug("Select from basic_united end")
    pkg_bu_set = set(cur.fetchall())

    if not list_apps:
        logging.error("today has no data")
        return

    list_resutl = []
    current_app = init_basic_cur(list_apps[0])

    for item in list_apps[1:]:
        if (current_app[0] == item[1]) or (
                    (samiliar(str(current_app[0]), str(item[1])) > 0.699) and (
                            (samiliar(str(current_app[2]), str(item[2])) == 1) or (
                                    samiliar(str(current_app[11]), str(item[7])) > 0.799))):
            # same pkgname
            logging.debug("Pkgname compare: %s and %s is the same one", item[1], current_app[0])
            update_basic_cur(current_app, item)
        else:
            logging.debug("Pkgname compare: %s and %s is very different", item[1], current_app[0])
            list_resutl.append(current_app)
            current_app = init_basic_cur(item)

    cur.execute("DELETE FROM t_apps_basic_united")
    sql_insert = "INSERT INTO t_apps_basic_united (a_pkgname = %s, a_pkgname_list = %s, a_name = %s, " \
                 "a_name_list = %s, a_url = %s, a_url_list = %s, a_picurl = %s, a_picurl_list = %s, " \
                 "a_publisher = %s, a_publisher_list = %s, a_subtitle = %s, a_description = %s, " \
                 "a_description_list = %s, a_classify = %s, a_defaulttags = %s, a_softgame = %s, " \
                 "a_softgame_list = %s, a_source_list = %s, a_getdate = %s) " \
                 "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    sql_update = "UPDATE t_apps_basic_united SET a_pkgname_list = %s, a_name = %s, a_name_list = %s, " \
                 "a_url = %s, a_url_list = %s, a_picurl = %s, a_picurl_list = %s, a_publisher = %s, " \
                 "a_publisher_list = %s, a_subtitle = %s, a_description = %s, a_description_list = %s, " \
                 "a_classify = %s, a_defaulttags = %s, a_softgame = %s, a_softgame_list = %s, " \
                 "a_source_list = %s, a_getdate = %s WHERE a_pkgname = %s"
    for info in list_resutl:
        assert info, "info is null"
        logging.debug("Insert is running: %s", info[0])
        if info[0] in pkg_bu_set:
            logging.debug("Basic already exist : %s update", info[0])
            update_item = update_basic_items(info)
            cur.execute(sql_update, update_item)
        else:
            logging.debug("Basic not exist : %s insert", info[0])
            current_app = init_basic_cur(info)
            cur.execute(sql_insert, current_app)
            pkg_bu_set.add(info[0])
        conn.commit()
        assert cur, "Cursor happened something"
    return
