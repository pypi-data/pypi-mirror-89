#  ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# ##### END GPL LICENSE BLOCK #####

import pygame
from .intern import Ops, Props
from .constants import *
pygame.init()


class App:
    """App variable"""

    def __init__(self):
        """
        Initializes app.
        """
        self.prop_uis = []
        self.ops = Ops()
        self.props = Props()

    def draw(self, events, size):
        """
        Starts app window.
        :param label: Window label.
        """
        self.window = pygame.Surface(size)
        for ui in self.prop_uis:
            self.draw_ui(ui)
        return self.window

    def draw_ui(self, ui):
        ui.layout.clear()
        ui.draw()
        font = ui.font
        row_size = ui.row_size

        surface = pygame.Surface(ui.size)
        surface.fill(ui.bg_col)
        if hasattr(ui, "border") and ui.border > 0:
            pygame.draw.rect(surface, ui.border_col, (0, 0)+ui.size, ui.border)

        curr_y = ui.padding
        for element in ui.layout.elements:
            if element[0] == "LABEL":
                text = font.render(element[1], 1, WHITE)
                surface.blit(text, (ui.padding, curr_y))
            curr_y += row_size

        self.window.blit(surface, ui.location)

    def register(self, obj):
        """
        Registers obj.
        :param obj: Object to register.
        """
        obj = obj()
        if obj.type == "PROPUI":
            self.prop_uis.append(obj)

        elif obj.type == "OPERATOR":
            if hasattr(self.ops, obj.idname):
                raise NameError(f"idname {obj.idname} already exists.")
            setattr(self.ops, obj.idname, obj)

        elif obj.type == "PROPERTIES":
            if hasattr(self.props, obj.idname):
                raise NameError(f"idname {obj.idname} already exists.")
            setattr(self.props, obj.idname, obj)