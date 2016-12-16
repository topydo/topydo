# Topydo - A todo.txt client written in Python.
# Copyright (C) 2016 Bram Schoenmakers <bram@topydo.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

""" This module provides a class that represents a color. """


class AbstractColor:
    NEUTRAL = 0
    PROJECT = 1
    CONTEXT = 2
    META = 3
    LINK = 4


class Color:
    color_names_dict = {
        'black': 0,
        'red': 1,
        'green': 2,
        'yellow': 3,
        'blue': 4,
        'magenta': 5,
        'cyan': 6,
        'gray': 7,
        'darkgray': 8,
        'light-red': 9,
        'light-green': 10,
        'light-yellow': 11,
        'light-blue': 12,
        'light-magenta': 13,
        'light-cyan': 14,
        'white': 15,
    }

    # Source: https://gist.github.com/jasonm23/2868981
    html_color_dict = {
          0: "#000000",   1: "#800000",   2: "#008000",   3: "#808000",   4: "#000080",
          5: "#800080",   6: "#008080",   7: "#c0c0c0",   8: "#808080",   9: "#ff0000",
         10: "#00ff00",  11: "#ffff00",  12: "#0000ff",  13: "#ff00ff",  14: "#00ffff",
         15: "#ffffff",  16: "#000000",  17: "#00005f",  18: "#000087",  19: "#0000af",
         20: "#0000d7",  21: "#0000ff",  22: "#005f00",  23: "#005f5f",  24: "#005f87",
         25: "#005faf",  26: "#005fd7",  27: "#005fff",  28: "#008700",  29: "#00875f",
         30: "#008787",  31: "#0087af",  32: "#0087d7",  33: "#0087ff",  34: "#00af00",
         35: "#00af5f",  36: "#00af87",  37: "#00afaf",  38: "#00afd7",  39: "#00afff",
         40: "#00d700",  41: "#00d75f",  42: "#00d787",  43: "#00d7af",  44: "#00d7d7",
         45: "#00d7ff",  46: "#00ff00",  47: "#00ff5f",  48: "#00ff87",  49: "#00ffaf",
         50: "#00ffd7",  51: "#00ffff",  52: "#5f0000",  53: "#5f005f",  54: "#5f0087",
         55: "#5f00af",  56: "#5f00d7",  57: "#5f00ff",  58: "#5f5f00",  59: "#5f5f5f",
         60: "#5f5f87",  61: "#5f5faf",  62: "#5f5fd7",  63: "#5f5fff",  64: "#5f8700",
         65: "#5f875f",  66: "#5f8787",  67: "#5f87af",  68: "#5f87d7",  69: "#5f87ff",
         70: "#5faf00",  71: "#5faf5f",  72: "#5faf87",  73: "#5fafaf",  74: "#5fafd7",
         75: "#5fafff",  76: "#5fd700",  77: "#5fd75f",  78: "#5fd787",  79: "#5fd7af",
         80: "#5fd7d7",  81: "#5fd7ff",  82: "#5fff00",  83: "#5fff5f",  84: "#5fff87",
         85: "#5fffaf",  86: "#5fffd7",  87: "#5fffff",  88: "#870000",  89: "#87005f",
         90: "#870087",  91: "#8700af",  92: "#8700d7",  93: "#8700ff",  94: "#875f00",
         95: "#875f5f",  96: "#875f87",  97: "#875faf",  98: "#875fd7",  99: "#875fff",
        100: "#878700", 101: "#87875f", 102: "#878787", 103: "#8787af", 104: "#8787d7",
        105: "#8787ff", 106: "#87af00", 107: "#87af5f", 108: "#87af87", 109: "#87afaf",
        110: "#87afd7", 111: "#87afff", 112: "#87d700", 113: "#87d75f", 114: "#87d787",
        115: "#87d7af", 116: "#87d7d7", 117: "#87d7ff", 118: "#87ff00", 119: "#87ff5f",
        120: "#87ff87", 121: "#87ffaf", 122: "#87ffd7", 123: "#87ffff", 124: "#af0000",
        125: "#af005f", 126: "#af0087", 127: "#af00af", 128: "#af00d7", 129: "#af00ff",
        130: "#af5f00", 131: "#af5f5f", 132: "#af5f87", 133: "#af5faf", 134: "#af5fd7",
        135: "#af5fff", 136: "#af8700", 137: "#af875f", 138: "#af8787", 139: "#af87af",
        140: "#af87d7", 141: "#af87ff", 142: "#afaf00", 143: "#afaf5f", 144: "#afaf87",
        145: "#afafaf", 146: "#afafd7", 147: "#afafff", 148: "#afd700", 149: "#afd75f",
        150: "#afd787", 151: "#afd7af", 152: "#afd7d7", 153: "#afd7ff", 154: "#afff00",
        155: "#afff5f", 156: "#afff87", 157: "#afffaf", 158: "#afffd7", 159: "#afffff",
        160: "#d70000", 161: "#d7005f", 162: "#d70087", 163: "#d700af", 164: "#d700d7",
        165: "#d700ff", 166: "#d75f00", 167: "#d75f5f", 168: "#d75f87", 169: "#d75faf",
        170: "#d75fd7", 171: "#d75fff", 172: "#d78700", 173: "#d7875f", 174: "#d78787",
        175: "#d787af", 176: "#d787d7", 177: "#d787ff", 178: "#dfaf00", 179: "#dfaf5f",
        180: "#dfaf87", 181: "#dfafaf", 182: "#dfafdf", 183: "#dfafff", 184: "#dfdf00",
        185: "#dfdf5f", 186: "#dfdf87", 187: "#dfdfaf", 188: "#dfdfdf", 189: "#dfdfff",
        190: "#dfff00", 191: "#dfff5f", 192: "#dfff87", 193: "#dfffaf", 194: "#dfffdf",
        195: "#dfffff", 196: "#ff0000", 197: "#ff005f", 198: "#ff0087", 199: "#ff00af",
        200: "#ff00df", 201: "#ff00ff", 202: "#ff5f00", 203: "#ff5f5f", 204: "#ff5f87",
        205: "#ff5faf", 206: "#ff5fdf", 207: "#ff5fff", 208: "#ff8700", 209: "#ff875f",
        210: "#ff8787", 211: "#ff87af", 212: "#ff87df", 213: "#ff87ff", 214: "#ffaf00",
        215: "#ffaf5f", 216: "#ffaf87", 217: "#ffafaf", 218: "#ffafdf", 219: "#ffafff",
        220: "#ffdf00", 221: "#ffdf5f", 222: "#ffdf87", 223: "#ffdfaf", 224: "#ffdfdf",
        225: "#ffdfff", 226: "#ffff00", 227: "#ffff5f", 228: "#ffff87", 229: "#ffffaf",
        230: "#ffffdf", 231: "#ffffff", 232: "#080808", 233: "#121212", 234: "#1c1c1c",
        235: "#262626", 236: "#303030", 237: "#3a3a3a", 238: "#444444", 239: "#4e4e4e",
        240: "#585858", 241: "#626262", 242: "#6c6c6c", 243: "#767676", 244: "#808080",
        245: "#8a8a8a", 246: "#949494", 247: "#9e9e9e", 248: "#a8a8a8", 249: "#b2b2b2",
        250: "#bcbcbc", 251: "#c6c6c6", 252: "#d0d0d0", 253: "#dadada", 254: "#e4e4e4",
        255: "#eeeeee",
    }

    def __init__(self, p_value=None):
        """ p_value is user input, be it a word color or an xterm code """
        self._value = None
        self.color = p_value

    @property
    def color(self):
        return self._value

    @color.setter
    def color(self, p_value):
        try:
            if not p_value:
                self._value = None
            elif p_value in Color.color_names_dict:
                self._value = Color.color_names_dict[p_value]
            else:
                self._value = int(p_value)

                # values not in the 256 range are normalized to be neutral
                if not 0 <= self._value < 256:
                    raise ValueError
        except ValueError:
            # garbage was entered, make it neutral, so at least some
            # highlighting may take place
            self._value = -1

    def is_neutral(self):
        """
        A neutral color is the default color on the shell, setting this color
        will reset all other attributes (background, foreground, decoration).
        """
        return self._value == -1

    def is_valid(self):
        """
        Whether the color is a valid color.
        """
        return self._value is not None

    def as_ansi(self, p_decoration='normal', p_background=False):
        if not self.is_valid():
            return ''
        elif self.is_neutral():
            return '\033[0m'

        is_high_color = 8 <= self._value < 16
        is_256 = 16 <= self._value < 255

        decoration_dict = {
            'normal': '0',
            'bold': '1',
            'faint': '2',
            'italic': '3',
            'underline': '4',
        }
        decoration = decoration_dict[p_decoration]

        base = 40 if p_background else 30
        if is_high_color:
            color = '1;{}'.format(base + self._value - 8)
        elif is_256:
            color = '{};5;{}'.format(base + 8, self._value)
        else:
            # it's a low color
            color = str(base + self._value)

        return '\033[{};{}m'.format(
            decoration,
            color
        )

    def as_html(self):
        try:
            return Color.html_color_dict[self.color]
        except KeyError:
            return '#ffffff'

    def as_rgb(self):
        """
        Returns a tuple (r, g, b) of the color.
        """

        html = self.as_html()

        return (
            int(html[1:3], 16),
            int(html[3:5], 16),
            int(html[5:7], 16)
        )
