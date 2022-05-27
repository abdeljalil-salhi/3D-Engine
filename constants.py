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

cparser = ConfigParser()
cparser.read(path.join("./resources/", "config.ini"))

try:
    MOVING_SPEED_RATE = float(cparser["SAVED"]["MOVING_SPEED"])
except:
    MOVING_SPEED_RATE = 0.5
try:
    ROTATION_SPEED_RATE = float(cparser["SAVED"]["ROTATION_SPEED"])
except:
    ROTATION_SPEED_RATE = 0.015
try:
    BACKGROUND_COLOR = str(cparser["SAVED"]["BACKGROUND_COLOR"])
except:
    BACKGROUND_COLOR = "#000000"
try:
    FILE = str(cparser["SAVED"]["FILE"])
except:
    FILE = "resources/Tank.obj"


def get_value(key):
    if key == "MOVING_SPEED":
        return MOVING_SPEED_RATE
    if key == "ROTATION_SPEED":
        return ROTATION_SPEED_RATE
    if key == "BACKGROUND_COLOR":
        return BACKGROUND_COLOR
    if key == "FILE":
        return FILE


def set_value(key, value):
    if key == "MOVING_SPEED":
        global MOVING_SPEED_RATE
        MOVING_SPEED_RATE = float(value)
    if key == "ROTATION_SPEED":
        global ROTATION_SPEED_RATE
        ROTATION_SPEED_RATE = float(value)
    if key == "BACKGROUND_COLOR":
        global BACKGROUND_COLOR
        BACKGROUND_COLOR = str(value)
    if key == "FILE":
        global FILE
        FILE = str(value)
    try:
        f_path = path.join("./resources/", "config.ini")
        if not path.isdir("./resources/"):
            mkdir("./resources/")
        f = open(f_path, "w+")
        f.write("[SAVED]\n")
        f.write("MOVING_SPEED={}\n".format(MOVING_SPEED_RATE))
        f.write("ROTATION_SPEED={}\n".format(ROTATION_SPEED_RATE))
        f.write("BACKGROUND_COLOR={}\n".format(BACKGROUND_COLOR))
        f.write("FILE={}\n".format(FILE))
        f.close()
    except:
        pass
