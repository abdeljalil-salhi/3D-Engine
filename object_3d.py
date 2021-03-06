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

from numba import njit


@njit(fastmath=True)
def any_func(arr, a, b):
    return np.any((arr == a) | (arr == b))


class Object3D:

    def __init__(self, render, vertices, faces):

        self.render = render
        self.vertices = np.array([np.array(v) for v in vertices])
        self.faces = np.array([np.array(face) for face in faces], dtype=object)
        self.translate([0.0001, 0.0001, 0.0001])

        self.font = pg.font.Font(
            "resources/IBMPlexMono-Regular.ttf", 30, bold=True)
        self.color_faces = [(pg.Color("orange"), face) for face in self.faces]

        self.label = ""

    def draw(self):

        self.screen_projection()
        self.movement()

    def movement(self):

        if get_value("MOVEMENT_FLAG") == "True":
            self.rotate_Y(-(pg.time.get_ticks() % 0.005))

    def screen_projection(self):

        vertices = self.vertices @ self.render.camera.camera_matrix()
        vertices = vertices @ self.render.projection.projection_matrix
        vertices /= vertices[:, -1].reshape(-1, 1)
        vertices[(vertices > 2) | (vertices < -2)] = 0
        vertices = vertices @ self.render.projection.to_screen_matrix
        vertices = vertices[:, :2]

        for index, color_face in enumerate(self.color_faces):
            color, face = color_face

            try:
                polygon = vertices[face]

                if not any_func(polygon, self.render.H_WIDTH, self.render.H_HEIGHT):
                    pg.draw.polygon(self.render.screen, color, polygon, 1)

                    if self.label:
                        text = self.font.render(
                            self.label[index], True, pg.Color('white'))
                        self.render.screen.blit(text, polygon[-1])
            except:
                pass

        if get_value("DRAW_VERTICES") == "True":

            for vertex in vertices:
                if not any_func(vertex, self.render.H_WIDTH, self.render.H_HEIGHT):
                    pg.draw.circle(self.render.screen,
                                   pg.Color('white'), vertex, 2)

    def translate(self, pos):

        self.vertices = self.vertices @ translate(pos)

    def scale(self, scale_to):

        self.vertices = self.vertices @ scale(scale_to)

    def rotate_X(self, angle):

        self.vertices = self.vertices @ rotate_X(angle)

    def rotate_Y(self, angle):

        self.vertices = self.vertices @ rotate_Y(angle)

    def rotate_Z(self, angle):

        self.vertices = self.vertices @ rotate_Z(angle)


class Axes(Object3D):

    def __init__(self, render):

        super().__init__(render)

        self.vertices = np.array([
            (0, 0, 0, 1), (1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1)
        ])

        self.faces = np.array([(0, 1), (0, 2), (0, 3)])

        self.colors = [pg.Color("red"), pg.Color("green"), pg.Color("blue")]

        self.color_faces = [(color, face)
                            for color, face in zip(self.colors, self.faces)]

        set_value("DRAW_VERTICES", "False")
        self.label = "XYZ"
