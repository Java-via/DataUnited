# _*_ coding: utf-8 _*_

"""
this model is aim to unit basic data of apps
"""

import re
# import time
import logging
import Levenshtein
import pymysql


# ----server----
DB_HOST = "101.200.174.172"
DB_DB = "data_apps"
DB_USER = "dba_apps"
DB_PWD = "mimadba_apps"
DB_CHARSET = "utf8"


def basic_catchapps(date):
    """
    unit data
    :param date: getdate of data
    :return: nothing
    """
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PWD, db=DB_DB, charset=DB_CHARSET)
    cur = conn.cursor()
    sql = "SELECT * FROM t_apps_basic WHERE DATE(a_getdate) = %s ORDER BY a_pkgname"
    cur.execute(sql, date)
    conn.commit()

    list_apps = cur.fetchall()
    if len(list_apps) > 0:
        list_resutl = []
        current_app = [i for i in range(19)]

        logging.debug("%s", list_apps[0])
        current_app = init_cur(current_app, list_apps[0])

        for item in list_apps[1:]:

            if (current_app[0] == item[1]) or ((samiliar(str(current_app[0]), str(item[1])) > 0.699) and samiliar(str(current_app[11]), str(item[7])) > 0.799):
                # same pkgname
                logging.debug("Pkgname compare: %s and %s is the same one", item[1], current_app[0])
                current_app = update_cur(current_app, item)
            else:
                logging.debug("Pkgname compare: %s and %s is very different", item[1], current_app[0])
                list_resutl.append(current_app)
                current_app = init_cur(current_app, item)

        cur.execute("DELETE FROM t_apps_basic_united")
        for info in list_resutl:
            assert info, "info is null"
            logging.debug("Insert is running: %s", info[0])
            cur.execute("INSERT INTO t_apps_basic_united VALUES (%s, %s, %s, %s, %s, %s, %s, "
                        "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", info)
            conn.commit()
            assert cur, "Cursor happened something"
        return
    else:
        logging.error("%s has no data", date)
        return


"""
    current_app:
    0:a_pkgname  1:a_pkgname_list  2:a_name  3:a_name_list  4:a_url  5:a_url_list  6:a_picurl  7:a_picurl_list
    8:a_publisher  9:a_publisher_list  10:a_subtitle  11:a_description  12:a_description_list  13:a_classify
    14:a_defaulttags  15:a_softgame  16:a_softgame_list  17:source_list  18:a_getdate
"""
"""
    0:a_id  1:a_pkgname  2:a_name  3:a_url  4:a_picurl  5:a_publisher  6:a_subtitle
    7:a_description  8:a_classify  9:a_defaulttags  10:a_softgame  11:a_source  12:a_getdate
"""


def update_cur(current_app, item):
    """
    update current app
    :param current_app:
    :param item:
    :return:
    """
    current_app[1] = package_str(current_app[1], item[1])
    current_app[3] = package_str(current_app[3], item[2])
    current_app[5] = package_str(current_app[5], item[3])
    current_app[7] = package_str(current_app[7], item[4])
    current_app[9] = package_str(current_app[9], item[5])
    current_app[10] = package_str(current_app[10], item[6])
    current_app[12] = package_str(current_app[12], item[7])
    current_app[13] = package_str(current_app[13], item[8])
    current_app[14] = package_str(current_app[14], item[9])
    current_app[16] = package_str(current_app[16], item[10])
    current_app[17] = package_str(current_app[17], item[11])
    return current_app


def init_cur(current_app, list_apps):
    """
    init current app
    :param current_app:
    :param list_apps:
    :return:
    """
    current_app[0] = list_apps[1]
    current_app[1] = list_apps[1]
    current_app[2] = list_apps[2]
    current_app[3] = list_apps[2]
    current_app[4] = list_apps[3]
    current_app[5] = list_apps[3]
    current_app[6] = list_apps[4]
    current_app[7] = list_apps[4]
    current_app[8] = list_apps[5]
    current_app[9] = list_apps[5]
    current_app[10] = list_apps[6]
    current_app[11] = list_apps[7]
    current_app[12] = list_apps[7]
    current_app[13] = list_apps[8]
    current_app[14] = list_apps[9]
    current_app[15] = list_apps[10]
    current_app[16] = list_apps[10]
    current_app[17] = list_apps[11]
    current_app[18] = list_apps[12]
    return current_app


def samiliar(string1, string2):
    """
    compare two strings
    :param string1:
    :param string2:
    :return: rate
    """
    return Levenshtein.ratio(get_string_strip(string1), get_string_strip(string2))


def package_str(string1, string2):
    """
    package two string with "\n"
    :param string1:
    :param string2:
    :return: join two
    """
    return get_string_strip(string1) + "\n" + get_string_strip(string2)


def get_string_strip(string):
    """
    get string striped \t, \n from a string, also change None to ""
    """
    return re.sub(r"\s+", " ", string).strip() if string else ""

# if __name__ == "__main__":
    # today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    # basic_catchapps(today)
