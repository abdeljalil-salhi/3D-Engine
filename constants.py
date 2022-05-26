# !/usr/bin/env python3
# -*- coding: utf-8 -*-
#  ,_     _
#  |\\_,-~/
#  / _  _ |    ,--.
# (  @  @ )   / ,-'       ___    __        __     __
#  \  _T_/-._( (         /   |  / /_  ____/ /__  / /
#  /         `. \       / /| | / __ \/ __  / _ \/ /
# |         _  \ |     / ___ |/ /_/ / /_/ /  __/ /
#  \ \ ,  /      |    /_/  |_/_.___/\__,_/\___/_/
#   || |-_\__   /                         © 2022
#  ((_/`(____,-'
#  3D ENGINE @v0.0.1

from configparser import ConfigParser
from os import path, mkdir

try:
    cparser = ConfigParser()
    cparser.read(path.join("./resources/", "config.ini"))
    MOVING_SPEED_RATE = float(cparser["SAVED"]["MOVING_SPEED"])
    ROTATION_SPEED_RATE = float(cparser["SAVED"]["ROTATION_SPEED"])
    BACKGROUND_COLOR = str(cparser["SAVED"]["BACKGROUND_COLOR"])
except:
    MOVING_SPEED_RATE = 0.5
    ROTATION_SPEED_RATE = 0.015
    BACKGROUND_COLOR = "#013636"


def getValue(key):
    if key == "MOVING_SPEED":
        return MOVING_SPEED_RATE
    if key == "ROTATION_SPEED":
        return ROTATION_SPEED_RATE
    if key == "BACKGROUND_COLOR":
        return BACKGROUND_COLOR


def setValue(key, value):
    if key == "MOVING_SPEED":
        global MOVING_SPEED_RATE
        MOVING_SPEED_RATE = float(value)
    if key == "ROTATION_SPEED":
        global ROTATION_SPEED_RATE
        ROTATION_SPEED_RATE = float(value)
    if key == "BACKGROUND_COLOR":
        global BACKGROUND_COLOR
        BACKGROUND_COLOR = str(value)
    try:
        f_path = path.join("./resources/", "config.ini")
        if not path.isdir("./resources/"):
            mkdir("./resources/")
        f = open(f_path, "w+")
        f.write("[SAVED]\n")
        f.write("MOVING_SPEED={}\n".format(MOVING_SPEED_RATE))
        f.write("ROTATION_SPEED={}\n".format(ROTATION_SPEED_RATE))
        f.write("BACKGROUND_COLOR={}\n".format(BACKGROUND_COLOR))
        f.close()
    except:
        pass
