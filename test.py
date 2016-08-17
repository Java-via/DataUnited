# _*_ coding: utf-8 _*_

import pymysql
import logging

logging.basicConfig(level=logging.DEBUG)

pkgset = set()
pkg_name_soft = {}
pkg_name_game = {}
dataset = set()
num = 0

# ----server----
DB_HOST = "101.200.174.172"
DB_DB = "data_apps"
DB_USER = "dba_apps"
DB_PWD = "mimadba_apps"
DB_CHARSET = "utf8"

conn = pymysql.connect(host=DB_HOST, db=DB_DB, user=DB_USER, passwd=DB_PWD, charset=DB_CHARSET)
cur = conn.cursor()
cur.execute("SELECT a_pkgname, a_name, a_softgame FROM t_apps_basic")
for app in cur.fetchall():
    if "soft" in app[2]:
        pkg_name_soft[app[0]] = app[1]
    else:
        pkg_name_game[app[0]] = app[1]
    pkgset.add(app[0])

f = open("G:/data", "r", encoding="utf-8")
softout = open("G:/softlist", "a", encoding="utf-8")
gameout = open("G:/gamelist", "a", encoding="utf-8")
for line in f.readlines():
    data = line.split("|")
    dataset.add(data[2])
    logging.debug("pkgname = %s", data[2])
f.close()

for pkg in dataset:
    if pkg in pkgset:
        if pkg in pkg_name_soft.keys():
            softout.write(pkg_name_soft.get(pkg) + "\n")
        else:
            gameout.write(pkg_name_game.get(pkg) + "\n")
softout.close()
gameout.close()
