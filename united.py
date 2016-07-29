# _*_ coding: utf-8 _*_

import Levenshtein
import re
import pymysql

DB_HOST = "127.0.0.1"
DB_DB = "app_db"
DB_USER = "root"
DB_PWD = "123"
DB_CHARSET = "utf8"


def catchapps():
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PWD, db=DB_DB, charset=DB_CHARSET)
    cur = conn.cursor()
    sql = "SELECT * FROM t_apps_basic WHERE DATE(a_getdate) = '2016-7-28' ORDER BY a_pkgname"
    cur.execute(sql)
    conn.commit()

    list_apps = cur.fetchall()
    list_resutl = []
    list_info = []

    current_app = list_apps[0]

    for item in list_apps[1: -1]:
        item = list(item)
        if current_app[0] == item[0]:
            """
            0:pkgname 1:name 2:url 3:subtitle 4:description 5:classify 6:defaulttags 7:softgame 8:source 9:getdate
            """
            list_info[0] = item[0]
            list_info[1] = item[1]
            list_info[2] = item[2]
            list_info[3] = samiliar(current_app[3], item[3])
            list_info[4] = samiliar(current_app[4], item[4])
            list_info[5] = samiliar(current_app[5], item[5])
            list_info[6] = samiliar(current_app[6], item[6])
            list_info[7] = samiliar(current_app[7], item[7])
            current_app = item

        else:
            if (current_app[0] != item[0]) & (len(current_app[0].split(".")) < 4):
                list_info = current_app
                current_app = item
            elif (len(current_app[0].split(".")) < len(item[0].split("."))) & (current_app[0] not in item[0]):
                list_info = current_app
                current_app = item
            elif len(current_app[0].split(".")) > len(item[0].split(".")):
                list_info = current_app
                current_app = item
            elif (len(current_app[0].split(".")) == len(item[0].split("."))) & (current_app[0][:-1] not in item[0]):
                list_info = current_app
                current_app = item
            else:
                list_info[0] = item[0]
                list_info[1] = item[1]
                list_info[2] = item[2]
                list_info[3] = samiliar(current_app[3], item[3])
                list_info[4] = samiliar(current_app[4], item[4])
                list_info[5] = samiliar(current_app[5], item[5])
                list_info[6] = samiliar(current_app[6], item[6])
                list_info[7] = samiliar(current_app[7], item[7])
                current_app = item

        list_resutl.append(list_info)

    for info in list_resutl:
        cur.execute("INSERT INTO t_apps_basic_united (a_pkgname, a_name, a_url, a_subtitle, a_description, "
                    "a_classify, a_defaulttags, a_softgame) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (info[0], info[1], info[2], info[3], info[4], info[5], info[6], info[7]))
        conn.commit()
    print(list_resutl[-1])


def samiliar(string1, string2):
    return string1 if Levenshtein.ratio(string1, string2) > 0.7 else string1 + string2


def get_string_strip(string):
    """
    get string striped \t, \n from a string, also change None to ""
    """
    return re.sub(r"\s+", " ", string).strip() if string else ""

if __name__ == "__main__":
    catchapps()
