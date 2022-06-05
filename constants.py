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
try:
    FULLSCREEN = cparser["SAVED"]["FULLSCREEN"]
except:
    FULLSCREEN = "False"
try:
    MOVEMENT_FLAG = cparser["SAVED"]["MOVEMENT_FLAG"]
except:
    MOVEMENT_FLAG = "True"
try:
    DRAW_VERTICES = cparser["SAVED"]["DRAW_VERTICES"]
except:
    DRAW_VERTICES = "True"


def get_value(key):
    if key == "MOVING_SPEED":
        return MOVING_SPEED_RATE
    if key == "ROTATION_SPEED":
        return ROTATION_SPEED_RATE
    if key == "BACKGROUND_COLOR":
        return BACKGROUND_COLOR
    if key == "FILE":
        return FILE
    if key == "FULLSCREEN":
        return FULLSCREEN
    if key == "MOVEMENT_FLAG":
        return MOVEMENT_FLAG
    if key == "DRAW_VERTICES":
        return DRAW_VERTICES


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
    if key == "FULLSCREEN":
        global FULLSCREEN
        FULLSCREEN = value
    if key == "MOVEMENT_FLAG":
        global MOVEMENT_FLAG
        MOVEMENT_FLAG = value
    if key == "DRAW_VERTICES":
        global DRAW_VERTICES
        DRAW_VERTICES = value
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
        f.write("FULLSCREEN={}\n".format(FULLSCREEN))
        f.write("MOVEMENT_FLAG={}\n".format(MOVEMENT_FLAG))
        f.write("DRAW_VERTICES={}\n".format(DRAW_VERTICES))
        f.close()
    except:
        pass
