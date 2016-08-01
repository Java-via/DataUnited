# _*_ coding: utf-8 _*_

import Levenshtein
import re
import pymysql

DB_HOST = "127.0.0.1"
DB_DB = "app_db"
DB_USER = "root"
DB_PWD = "123"
DB_CHARSET = "utf8"

"""
0:pkgname 1:name 2:url 3:subtitle 4:description 5:classify 6:defaulttags 7:softgame 8:source 9:getdate
0:a_pkgname 1:a_name 2:a_url 3:a_subtitle 4:a_description 5:a_classify 6:a_defaulttags 7:a_softgame
"""


def catchapps():
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PWD, db=DB_DB, charset=DB_CHARSET)
    cur = conn.cursor()
    sql = "SELECT * FROM t_apps_basic WHERE DATE(a_getdate) = '2016-7-28' ORDER BY a_pkgname"
    cur.execute(sql)
    conn.commit()

    list_apps = cur.fetchall()
    list_resutl = []

    current_app = list_apps[0]

    for item in list_apps[1: -1]:
        item = list(item)
        if current_app[0] == item[0]:
            item[0] = current_app[0]
            item[1] = current_app[1]
            item[2] = current_app[2]
            item[3] = samiliar(str(current_app[3]), str(item[3]))
            item[4] = samiliar(str(current_app[4]), str(item[4]))
            item[5] = samiliar(str(current_app[5]), str(item[5]))
            item[6] = samiliar(str(current_app[6]), str(item[6]))
            item[7] = samiliar(str(current_app[7]), str(item[7]))
            item[9] = current_app[9]
            current_app = item
        elif (Levenshtein.ratio(str(current_app[0]), str(item[0])) > 0.799) &\
                (Levenshtein.ratio(get_string_strip(str(current_app[4])), get_string_strip(str(item[4]))) > 0.799):
            item[0] = current_app[0]
            item[1] = current_app[1]
            item[2] = current_app[2]
            item[3] = samiliar(str(current_app[3]), str(item[3]))
            item[4] = samiliar(str(current_app[4]), str(item[4]))
            item[5] = samiliar(str(current_app[5]), str(item[5]))
            item[6] = samiliar(str(current_app[6]), str(item[6]))
            item[7] = samiliar(str(current_app[7]), str(item[7]))
            item[9] = current_app[9]
            current_app = item
        else:
            list_resutl.append(current_app)
            current_app = item

    for info in list_resutl:
        assert info, "info is null"
        cur.execute("INSERT INTO t_apps_basic_united (a_pkgname, a_name, a_url, a_subtitle, a_description, "
                    "a_classify, a_defaulttags, a_softgame) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %S)",
                    (info[0], info[1], info[2], info[3], info[4], info[5], info[6], info[7], info[9]))
        conn.commit()
        assert cur, "Cursor happened something"
    print(list_resutl[-1])


def samiliar(string1, string2):
    return string1 if Levenshtein.ratio(string1, string2) > 0.7 else (string1 + "//" + string2)


def get_string_strip(string):
    """
    get string striped \t, \n from a string, also change None to ""
    """
    return re.sub(r"\s+", " ", string).strip() if string else ""

if __name__ == "__main__":
    catchapps()
