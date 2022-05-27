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

from object_3d import *
from camera import *
from projection import *
from constants import *

import pygame as pg
import pygame_gui as pgg

from os import path
from configparser import ConfigParser
from pygame_gui.core.utility import create_resource_path
from screeninfo import get_monitors


class SoftwareRender:
    def __init__(self):
        pg.init()
        pg.display.set_caption("3D Engine")

        monitors = get_monitors()
        for index in range(0, len(monitors)):
            monitor = monitors[index]
            if monitor.is_primary:
                self.RESOLUTION = self.WIDTH, self.HEIGHT = (
                    monitor.width - 200), (monitor.height - 200)

        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2
        self.FPS = 120
        self.file_dialog = None
        self.show_options = False
        self.is_running = True
        self.fonts = []

        self.screen = pg.display.set_mode(self.RESOLUTION, pg.RESIZABLE)
        self.manager = pgg.UIManager(self.RESOLUTION, "resources/theme.json")
        self.clock = pg.time.Clock()

        self.create_objects()
        self.create_layout()

    def create_fonts(self, font_sizes):
        for size in font_sizes:
            try:
                self.fonts.append(pg.font.Font(
                    "resources/IBMPlexMono-Regular.ttf", size))
            except:
                self.fonts.append(pg.font.SysFont("Arial", size))

        return self.fonts

    def render(self, font, text, color, pos):
        text_to_show = font.render(text, 0, pg.Color(color))
        self.screen.blit(text_to_show, pos)

    def display_fps(self):
        self.render(self.fonts[1], text=str(
            int(self.clock.get_fps())) + " FPS", color="red", pos=(5, 0))

    def create_objects(self):
        self.camera = Camera(self, [-5, 5, -50])
        self.projection = Projection(self)
        self.object = self.get_object_from_file(str(get_value("FILE")))

    def get_object_from_file(self, filename):
        try:
            vertice, faces = [], []
            with open(filename) as f:
                for line in f:
                    if line.startswith("v "):
                        vertice.append([float(i)
                                       for i in line.split()[1:]] + [1])
                    elif line.startswith("f"):
                        faces_ = line.split()[1:]
                        faces.append(
                            [int(face_.split("/")[0]) - 1 for face_ in faces_])

            return Object3D(self, vertice, faces)
        except:
            print("error")

    def create_layout(self):
        w, h = pg.display.get_surface().get_size()

        self.options = pgg.elements.UIButton(relative_rect=pg.Rect(
            (w - 100, 0), (100, 30)), text="Options", manager=self.manager)

        self.panel = pgg.elements.UIPanel(
            relative_rect=pg.Rect((w - 250, 0), (250, h)),
            manager=self.manager,
            starting_layer_height=0,
            visible=0,
        )

        self.moving_speed_label = pgg.elements.UILabel(pg.Rect(
            (w - 293, 35), (200, 25)), text="Moving Speed", manager=self.manager, visible=0)
        self.moving_speed_entry = pgg.elements.UITextEntryLine(pg.Rect(
            (w - 245, 55), (240, -1)), manager=self.manager, visible=0)
        self.moving_speed_entry.set_text(
            str(get_value("MOVING_SPEED")))
        self.rotation_speed_label = pgg.elements.UILabel(pg.Rect(
            (w - 287, 95), (200, 25)), text="Rotation Speed", manager=self.manager, visible=0)
        self.rotation_speed_entry = pgg.elements.UITextEntryLine(pg.Rect(
            (w - 245, 115), (240, -1)), manager=self.manager, visible=0)
        self.rotation_speed_entry.set_text(
            str(get_value("ROTATION_SPEED")))

        self.load_button = pgg.elements.UIButton(relative_rect=pg.Rect(
            (w - 250, h - 30), (250, 30)), text="Load 3D File", manager=self.manager, visible=0)

    def applyOptions(self):
        set_value("MOVING_SPEED", self.moving_speed_entry.get_text())
        set_value("ROTATION_SPEED", self.rotation_speed_entry.get_text())

    def toggle_options(self):
        if self.show_options:
            self.panel.show()
            self.moving_speed_label.show()
            self.moving_speed_entry.show()
            self.rotation_speed_label.show()
            self.rotation_speed_entry.show()
            self.load_button.show()
        else:
            self.applyOptions()
            self.panel.hide()
            self.moving_speed_label.hide()
            self.moving_speed_entry.hide()
            self.rotation_speed_label.hide()
            self.rotation_speed_entry.hide()
            self.load_button.hide()

    def draw(self):
        self.screen.fill(pg.Color(get_value("BACKGROUND_COLOR")))
        self.object.draw()
        self.manager.draw_ui(self.screen)

    def run(self):
        while self.is_running:
            self.delta = self.clock.tick(self.FPS)/1000.0
            self.fonts = self.create_fonts([32, 20, 16, 8])

            self.draw()
            self.camera.control()
            self.display_fps()

            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    self.is_running = False
                    exit()

                if event.type == pg.VIDEORESIZE:
                    self.manager = pgg.UIManager(
                        (event.w, event.h), "resources/theme.json")
                    self.show_options = False
                    self.file_dialog = None
                    self.create_layout()

                if event.type == pgg.UI_BUTTON_PRESSED:
                    if event.ui_element == self.options:
                        self.show_options = not self.show_options
                        self.toggle_options()

                if event.type == pg.KEYUP:
                    if event.key == pg.K_o:
                        self.show_options = not self.show_options
                        self.toggle_options()

                if event.type == pgg.UI_BUTTON_PRESSED:
                    if event.ui_element == self.load_button:
                        self.file_dialog = pgg.windows.UIFileDialog(pg.Rect(
                            160, 50, 440, 500), self.manager, window_title="Load 3D Object (.obj)",
                            initial_file_path="./resources/", allow_existing_files_only=True)
                        self.load_button.disable()

                if event.type == pgg.UI_FILE_DIALOG_PATH_PICKED:
                    f_path = create_resource_path(event.text)
                    set_value("FILE", f_path)
                    self.object = self.get_object_from_file(
                        str(get_value("FILE")))

                if event.type == pgg.UI_WINDOW_CLOSE:
                    if event.ui_element == self.file_dialog:
                        self.load_button.enable()
                        self.file_dialog = None

                self.manager.process_events(event)

            self.manager.update(self.delta)
            self.clock.tick(self.FPS)

            pg.display.flip()


app = SoftwareRender()
app.run()
