# _*_ coding: utf-8 _*_

import Levenshtein
import time
import re
import pymysql
import logging

logging.basicConfig(level=logging.DEBUG)

# ----server----
DB_HOST = "101.200.174.172"
DB_DB = "data_apps"
DB_USER = "dba_apps"
DB_PWD = "mimadba_apps"
DB_CHARSET = "utf8"

# ----local----
# DB_HOST = "127.0.0.1"
# DB_DB = "app_db"
# DB_USER = "root"
# DB_PWD = "123"
# DB_CHARSET = "utf8"

"""
0:pkgname 1:name 2:url 3:publisher 4:picurl 5:bytes 6:updatedate 7:version
8:install 9:like 10:comment 11:score 12:softgame 13:source 14:getdate
0:a_pkgname 1:a_name 2:a_url 3:publisher 4:picurl 5:bytes 6:updatedate 7:version
8:install 9:like 10:comment 11:score 12:softgame 13:getdate
"""


def add_catchapps(date):
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PWD, db=DB_DB, charset=DB_CHARSET)
    cur = conn.cursor()
    sql = "SELECT * FROM t_apps_additional WHERE DATE(a_getdate) = %s ORDER BY a_pkgname"
    cur.execute(sql, date)
    conn.commit()

    list_apps = cur.fetchall()
    if len(list_apps) > 0:
        logging.debug("it's time to start")

        list_resutl = []
        current_app = list_apps[0]

        for item in list_apps[1: -1]:
            item = list(item)
            if current_app[0] == item[0]:
                logging.debug("Pkgname compare: %s and %s is the same one", item[0], current_app[0])
                item[0] = current_app[0]
                item[1] = current_app[1]
                item[2] = current_app[2]
                item[3] = samiliar(str(current_app[3]), str(item[3]))
                item[4] = str(current_app[4]) if "http://pp.myapp.com/" in str(current_app[4]) else item[4]
                item[5] = current_app[5]
                item[6] = current_app[6]
                item[7] = current_app[7]
                item[8] = int(current_app[8]) + int(item[8])
                item[9] = current_app[9] if current_app[9] != 0 else item[9]
                item[10] = current_app[10] if current_app[10] != 0 else item[10]
                item[11] = current_app[11] if current_app[11] != 0 else item[11]
                item[12] = current_app[12]
                item[14] = current_app[14]
                current_app = item
            elif (Levenshtein.ratio(str(current_app[0]), str(item[0])) > 0.799) & \
                    (Levenshtein.ratio(get_string_strip(str(current_app[1])), get_string_strip(str(item[1]))) > 0.799):
                logging.debug("Pkaname compare: the matching degree of %s and %s is very high", item[0], current_app[0])
                item[0] = current_app[0]
                item[1] = current_app[1]
                item[2] = current_app[2]
                item[3] = samiliar(str(current_app[3]), str(item[3]))
                item[4] = str(current_app[4]) if "http://pp.myapp.com/" in str(current_app[4]) else item[4]
                item[5] = current_app[5]
                item[6] = current_app[6]
                item[7] = current_app[7]
                item[8] = int(current_app[8]) + int(item[8])
                item[9] = current_app[9] if current_app[9] != 0 else item[9]
                item[10] = current_app[10] if current_app[10] != 0 else item[10]
                item[11] = current_app[11] if current_app[11] != 0 else item[11]
                item[12] = current_app[12]
                item[14] = current_app[14]
                current_app = item
            else:
                logging.debug("Pkgname compare: %s and %s is very different", item[0], current_app[0])
                list_resutl.append(current_app)
                current_app = item

        for info in list_resutl:
            assert info, "info is null"
            cur.execute("INSERT INTO t_apps_additional_united (a_pkgname, a_name, a_url, "
                        "a_publisher, a_picurl, a_bytes, a_updatedate, a_version, a_install, "
                        "a_like, a_comment, a_score, a_softgame, a_getdate)"
                        " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                        (info[0], info[1], info[2], info[3], info[4], info[5], info[6], info[7],
                         info[8], info[9], info[10], info[11], info[12], info[14]))
            conn.commit()
            assert cur, "Cursor happened something"
        logging.debug("done")
        return
    else:
        logging.debug("%s today has no data", date)
        return


def samiliar(string1, string2):
    return string1 if Levenshtein.ratio(string1, string2) > 0.7 else (string1 + "//" + string2)


def get_string_strip(string):
    """
    get string striped \t, \n from a string, also change None to ""
    """
    return re.sub(r"\s+", " ", string).strip() if string else ""

if __name__ == "__main__":
    today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    add_catchapps(today)
