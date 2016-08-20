# _*_ coding: utf-8 _*

import re
import Levenshtein
import functools
import operator

# ----server----
DB_HOST = "101.200.174.172"
DB_DB = "data_apps"
DB_USER = "dba_apps"
DB_PWD = "mimadba_apps"
DB_CHARSET = "utf8"

"""
    basic_current_app:
    0:a_pkgname  1:a_pkgname_list  2:a_name  3:a_name_list  4:a_url  5:a_url_list  6:a_picurl  7:a_picurl_list
    8:a_publisher  9:a_publisher_list  10:a_subtitle  11:a_description  12:a_description_list  13:a_classify
    14:a_defaulttags  15:a_softgame  16:a_softgame_list  17:source_list  18:a_getdate
"""
"""
    basic_item:
    0:a_id  1:a_pkgname  2:a_name  3:a_url  4:a_picurl  5:a_publisher  6:a_subtitle
    7:a_description  8:a_classify  9:a_defaulttags  10:a_softgame  11:a_source  12:a_getdate
"""


def init_basic_cur(list_apps):
    """
    init current app
    :param list_apps:
    :return:
    """

    return [list_apps[1], list_apps[1], list_apps[2], list_apps[2],
            list_apps[3], list_apps[3], list_apps[4], list_apps[4],
            list_apps[5], list_apps[5], get_string_strip(list_apps[6]),
            get_string_strip(list_apps[7]), get_string_strip(list_apps[7]),
            get_string_strip(list_apps[8]), get_string_strip(list_apps[9]),
            list_apps[10], list_apps[10], list_apps[11], list_apps[12]]


def update_basic_cur(current_app, item):
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
    return


"""
    additional:
    0:a_pkgname   1:a_name          2:a_url        3:a_picurl
    4:a_bytes     5:a_updatedate    6:a_version    7:a_install
    8:a_like      9:a_comment       10:a_score     11:a_softgame    12:a_source    13:a_getdate
"""
"""
    additional_united:
    0:a_pkgname  0    1:a_pkgname_list 0 2:a_name  1         3:a_name_list  1
    4:a_url 2         5:a_url_list  2    6:a_picurl 3        7:a_picurl_list 3 8:a_bytes 4
    9:a_updatedate 5  10:a_version  6    11:a_version_list 6 12:a_install_sum7 13:a_install_list 7 14:a_like 8
    15:a_comment_sum9 16:a_comment_list9 17:a_score 10        18:a_softgame 11 19:a_softgame_list 11
    20:a_source_list12 21:a_getdate 13
"""


def init_addi_cur(list_apps):
    """
    init current app
    :param current_app:
    :param list_apps:
    :return:
    """
    return [list_apps[0], list_apps[0], list_apps[1], list_apps[1], list_apps[2],
            list_apps[2], list_apps[3], list_apps[3], list_apps[4], list_apps[5],
            list_apps[6], list_apps[6], list_apps[7], list_apps[7], list_apps[8],
            list_apps[9], list_apps[9], list_apps[10], list_apps[11], list_apps[11],
            list_apps[12], list_apps[13]]


def update_addi_cur(current_app, item):
    """
    update current app
    :param current_app:
    :param item:
    :return:
    """
    current_app[1] = package_str(current_app[1], item[0])
    current_app[3] = package_str(current_app[3], item[1])
    current_app[5] = package_str(current_app[5], item[2])
    current_app[7] = package_str(current_app[7], item[3])
    current_app[11] = package_str(current_app[11], item[6])
    current_app[12] = get_sum(current_app[12], item[7])
    current_app[13] = package_str(current_app[13], str(item[7]))
    current_app[15] = get_sum(current_app[15], int(item[9]))
    current_app[16] = package_str(current_app[16], str(item[9]))
    current_app[19] = package_str(current_app[19], item[11])
    current_app[20] = package_str(current_app[20], item[12])
    return


def update_addi_items(current_app):
    return [current_app[1], current_app[2], current_app[3], current_app[4],
            current_app[5], current_app[6], current_app[7], current_app[8],
            current_app[9], current_app[10], current_app[11], current_app[12],
            current_app[13], current_app[14], current_app[15], current_app[16],
            current_app[17], current_app[18], current_app[19], current_app[20],
            current_app[21], current_app[0]]


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
    return str(string1) + "\n" + get_string_strip(str(string2))


def get_string_strip(string):
    """
    get string striped \t, \n from a string, also change None to ""
    """
    return re.sub(r"\s+", " ", string).strip() if string else ""


def get_sum(num1, num2):
    return num1 + num2


def get_string_split(string, split_chars=(" ", "\t", ","), is_remove_empty=False):
    """
    get string list by splitting string from split_chars
    """
    assert len(split_chars) >= 2, "get_string_split: len(split_chars) must >= 2"
    string_list = []
    for char in split_chars:
        if string_list:
            string_list = functools.reduce(operator.add, [item.split(char) for item in string_list], [])
        else:
            string_list = string.split(char)
    return string_list if not is_remove_empty else [item.strip() for item in string_list if item.strip()]
