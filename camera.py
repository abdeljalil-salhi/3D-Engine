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

from matrix import *
from constants import *
import pygame as pg


class Camera:
    def __init__(self, render, pos):
        self.render = render
        self.pos = np.array([*pos, 1.0])
        self.forward = np.array([0, 0, 1, 1])
        self.up = np.array([0, 1, 0, 1])
        self.right = np.array([1, 0, 0, 1])
        self.h_fov = math.pi / 3
        self.v_fov = self.h_fov * (render.HEIGHT / render.WIDTH)
        self.near_plane = 0.1
        self.far_plane = 100
        self.moving_speed = getValue("MOVING_SPEED")
        self.rotation_speed = getValue("ROTATION_SPEED")

    def control(self):
        self.moving_speed = getValue("MOVING_SPEED")
        self.rotation_speed = getValue("ROTATION_SPEED")
        key = pg.key.get_pressed()
        if key[pg.K_r]:
            self.pos = [-5, 5, -50, 1]
            self.forward = np.array([0, 0, 1, 1])
            self.up = np.array([0, 1, 0, 1])
            self.right = np.array([1, 0, 0, 1])
        if key[pg.K_q]:
            self.pos -= self.right * self.moving_speed
        if key[pg.K_d]:
            self.pos += self.right * self.moving_speed
        if key[pg.K_z]:
            self.pos += self.forward * self.moving_speed
        if key[pg.K_s]:
            self.pos -= self.forward * self.moving_speed
        if key[pg.K_a]:
            self.pos += self.up * self.moving_speed
        if key[pg.K_w]:
            self.pos -= self.up * self.moving_speed

        if key[pg.K_LEFT]:
            self.camera_yaw(-self.rotation_speed)
        if key[pg.K_RIGHT]:
            self.camera_yaw(self.rotation_speed)
        if key[pg.K_UP]:
            self.camera_pitch(-self.rotation_speed)
        if key[pg.K_DOWN]:
            self.camera_pitch(self.rotation_speed)

    def camera_yaw(self, angle):
        rotate = rotate_Y(angle)
        self.forward = self.forward @ rotate
        self.right = self.right @ rotate
        self.up = self.up @ rotate

    def camera_pitch(self, angle):
        rotate = rotate_X(angle)
        self.forward = self.forward @ rotate
        self.right = self.right @ rotate
        self.up = self.up @ rotate

    def translate_matrix(self):
        x, y, z, w = self.pos
        return np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [-x, -y, -z, 1]
        ])

    def rotate_matrix(self):
        rx, ry, rz, w = self.right
        fx, fy, fz, w = self.forward
        ux, uy, uz, w = self.up
        return np.array([
            [rx, ux, fx, 0],
            [ry, uy, fy, 0],
            [rz, uz, fz, 0],
            [0, 0, 0, 1]
        ])

    def camera_matrix(self):
        return self.translate_matrix() @ self.rotate_matrix()
