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

from .constants import *


class Layout:
    def __init__(self):
        self.clear()

    def clear(self):
        self.elements = []

    def prop(self, family, idname):
        self.elements.append(("PROP", family, idname))

    def operator(self, idname):
        self.elements.append(("OPERATOR", idname))

    def label(self, text):
        self.elements.append(("LABEL", text))


class Properties:
    type = "PROPERTIES"


class Operator:
    type = "OPERATOR"


class PropUI:
    type = "PROPUI"
    layout = Layout()

    row_size = 20
    padding = 10

    bg_col = GRAY
    border = 2
    border_col = WHITE