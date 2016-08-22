# _*_ coding: utf-8 _*_

import pymysql
import logging
from .united_utils import *


def addi_catchapps(date):
    conn = pymysql.connect(host=DB_HOST, db=DB_DB, user=DB_USER, passwd=DB_PWD, charset=DB_CHARSET)
    cur = conn.cursor()
    sql = "SELECT a_pkgname, a_pkgname_list FROM t_apps_basic_united ORDER BY a_pkgname;"
    sql_addi = "SELECT * FROM t_apps_additional WHERE DATE(a_getdate) = %s AND a_pkgname IN %s ORDER BY a_pkgname;"
    sql_addi_pkg = "SELECT a_pkgname FROM t_apps_addi_united WHERE DATE (a_getdate) = %s;"
    logging.debug("BASIC: start to select from basic_united")
    cur.execute(sql)
    logging.debug("BASIC: select from basic_united over, start to add to basic_pkg_list")
    basic_pkg_list = cur.fetchall()
    logging.debug("ADDI-UNITED: start to select from addi_united")
    cur.execute(sql_addi_pkg, date)
    logging.debug("ADDI-UNITED: select from addi_united is over, start to add to addi_pkg_set")
    addi_pkg_set = set(item[0] for item in cur.fetchall())
    logging.debug("Addi already has : %s", addi_pkg_set)
    logging.debug("BASIC: basic_pkg_list has all data")
    for pkg_list in basic_pkg_list:
        logging.debug("ADDI: start to modify pkgname_list")
        pkg_name = get_string_split(pkg_list[1], (" ", "\n"), is_remove_empty=True)
        logging.debug("ADDI: in_pkg get all, start to insert select from additional")
        logging.debug("PKGNAME is got: %s", pkg_name)
        cur.execute(sql_addi, (date, pkg_name))
        apps = cur.fetchall()
        if len(apps) == 0:
            logging.warning("Not exist : %s", pkg_name)
        else:
            addi_app = init_addi_cur(apps[0])
            logging.debug("ENDING: get result")
            if len(apps) > 1:
                for app in apps[1:]:
                    update_addi_cur(addi_app, app)
            logging.debug("ENDING: inserting to addi_united")
            sql_insert = "INSERT INTO t_apps_addi_united VALUES (%s, %s, %s, %s, %s, %s, %s, " \
                         "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
            sql_update = "UPDATE t_apps_addi_united SET a_pkgname_list = %s, a_name = %s, a_name_list = %s," \
                         " a_url = %s, a_url_list = %s, a_picurl = %s, a_picurl_list = %s, a_bytes = %s, " \
                         "a_updatedate = %s, a_version = %s, a_version_list = %s, a_install_sum = %s, " \
                         "a_install_list = %s, a_like = %s, a_comment_sum = %s, a_comment_list = %s, a_score = %s, " \
                         "a_softgame = %s, a_softgame_list = %s, a_source_list = %s, a_getdate = %s " \
                         "WHERE a_pkgname = %s"
            if addi_app[0] in addi_pkg_set:
                logging.debug("Addi already exist : %s, update", addi_app[0])
                cur.execute(sql_update, update_addi_items(addi_app))
            else:
                logging.debug("Addi not exist : %s, insert", addi_app[0])
                cur.execute(sql_insert, addi_app)
                addi_pkg_set.add(addi_app[0])
            conn.commit()

    logging.debug("done")
    return
