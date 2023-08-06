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


class BoolProp:
    type = "BOOL"

    def __init__(self, name="", description="", default=False):
        """
        :param name: Name of prop.
        :param description: Description of prop.
        :param default: Default value of prop.
        """
        self.name = name
        self.description = description
        self.value = default


class IntProp:
    type = "INT"

    def __init__(self, name="", description="", default=0, min=-100, max=100, step=1):
        """
        :param name: Name of prop.
        :param description: Description of prop.
        :param default: Default value of prop.
        :param min: Minimum value of prop.
        :param max: Maximum value of prop.
        :param step: Step of prop.
        """
        self.name = name
        self.description = description
        self.value = default
        self.min = min
        self.max = max
        self.step = step


class FloatProp:
    type = "FLOAT"

    def __init__(self, name="", description="", default=0, min=-100, max=100):
        """
        :param name: Name of prop.
        :param description: Description of prop.
        :param default: Default value of prop.
        :param min: Minimum value of prop.
        :param max: Maximum value of prop.
        """
        self.name = name
        self.description = description
        self.value = default
        self.min = min
        self.max = max


class StringProp:
    type = "STRING"

    def __init__(self, name="", description="", default="", max_len="", password=False):
        """
        :param name: Name of prop.
        :param description: Description of prop.
        :param default: Default value of prop.
        :param max_len: Maximum length of string.
        :param password: Show as asterisks?
        """
        self.name = name
        self.description = description
        self.value = default
        self.max_len = max_len
        self.password = password