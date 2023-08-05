"""simple termcolor library
"""

import re

# https://developer.mozilla.org/en-US/docs/Web/CSS/color_value

CSS_COLORS_TO_HEX = {
    "aliceblue": "#f0f8ff",
    "antiquewhite": "#faebd7",
    "aqua": "#00ffff",
    "aquamarine": "#7fffd4",
    "azure": "#f0ffff",
    "beige": "#f5f5dc",
    "bisque": "#ffe4c4",
    "black": "#000000",
    "blanchedalmond": "#ffebcd",
    "blue": "#0000ff",
    "blueviolet": "#8a2be2",
    "brown": "#a52a2a",
    "burlywood": "#deb887",
    "cadetblue": "#5f9ea0",
    "chartreuse": "#7fff00",
    "chocolate": "#d2691e",
    "coral": "#ff7f50",
    "cornflowerblue": "#6495ed",
    "cornsilk": "#fff8dc",
    "crimson": "#dc143c",
    "cyan": "#00ffff",
    "darkblue": "#00008b",
    "darkcyan": "#008b8b",
    "darkgoldenrod": "#b8860b",
    "darkgray": "#a9a9a9",
    "darkgreen": "#006400",
    "darkgrey": "#a9a9a9",
    "darkkhaki": "#bdb76b",
    "darkmagenta": "#8b008b",
    "darkolivegreen": "#556b2f",
    "darkorange": "#ff8c00",
    "darkorchid": "#9932cc",
    "darkred": "#8b0000",
    "darksalmon": "#e9967a",
    "darkseagreen": "#8fbc8f",
    "darkslateblue": "#483d8b",
    "darkslategray": "#2f4f4f",
    "darkslategrey": "#2f4f4f",
    "darkturquoise": "#00ced1",
    "darkviolet": "#9400d3",
    "deeppink": "#ff1493",
    "deepskyblue": "#00bfff",
    "dimgray": "#696969",
    "dimgrey": "#696969",
    "dodgerblue": "#1e90ff",
    "firebrick": "#b22222",
    "floralwhite": "#fffaf0",
    "forestgreen": "#228b22",
    "fuchsia": "#ff00ff",
    "gainsboro": "#dcdcdc",
    "ghostwhite": "#f8f8ff",
    "goldenrod": "#daa520",
    "gold": "#ffd700",
    "gray": "#808080",
    "green": "#008000",
    "greenyellow": "#adff2f",
    "grey": "#808080",
    "honeydew": "#f0fff0",
    "hotpink": "#ff69b4",
    "indianred": "#cd5c5c",
    "indigo": "#4b0082",
    "ivory": "#fffff0",
    "khaki": "#f0e68c",
    "lavenderblush": "#fff0f5",
    "lavender": "#e6e6fa",
    "lawngreen": "#7cfc00",
    "lemonchiffon": "#fffacd",
    "lightblue": "#add8e6",
    "lightcoral": "#f08080",
    "lightcyan": "#e0ffff",
    "lightgoldenrodyellow": "#fafad2",
    "lightgray": "#d3d3d3",
    "lightgreen": "#90ee90",
    "lightgrey": "#d3d3d3",
    "lightpink": "#ffb6c1",
    "lightsalmon": "#ffa07a",
    "lightseagreen": "#20b2aa",
    "lightskyblue": "#87cefa",
    "lightslategray": "#778899",
    "lightslategrey": "#778899",
    "lightsteelblue": "#b0c4de",
    "lightyellow": "#ffffe0",
    "lime": "#00ff00",
    "limegreen": "#32cd32",
    "linen": "#faf0e6",
    "magenta": "#ff00ff",
    "maroon": "#800000",
    "mediumaquamarine": "#66cdaa",
    "mediumblue": "#0000cd",
    "mediumorchid": "#ba55d3",
    "mediumpurple": "#9370db",
    "mediumseagreen": "#3cb371",
    "mediumslateblue": "#7b68ee",
    "mediumspringgreen": "#00fa9a",
    "mediumturquoise": "#48d1cc",
    "mediumvioletred": "#c71585",
    "midnightblue": "#191970",
    "mintcream": "#f5fffa",
    "mistyrose": "#ffe4e1",
    "moccasin": "#ffe4b5",
    "navajowhite": "#ffdead",
    "navy": "#000080",
    "oldlace": "#fdf5e6",
    "olive": "#808000",
    "olivedrab": "#6b8e23",
    "orange": "#ffa500",
    "orangered": "#ff4500",
    "orchid": "#da70d6",
    "palegoldenrod": "#eee8aa",
    "palegreen": "#98fb98",
    "paleturquoise": "#afeeee",
    "palevioletred": "#db7093",
    "papayawhip": "#ffefd5",
    "peachpuff": "#ffdab9",
    "peru": "#cd853f",
    "pink": "#ffc0cb",
    "plum": "#dda0dd",
    "powderblue": "#b0e0e6",
    "purple": "#800080",
    "rebeccapurple": "#663399",
    "red": "#ff0000",
    "rosybrown": "#bc8f8f",
    "royalblue": "#4169e1",
    "saddlebrown": "#8b4513",
    "salmon": "#fa8072",
    "sandybrown": "#f4a460",
    "seagreen": "#2e8b57",
    "seashell": "#fff5ee",
    "sienna": "#a0522d",
    "silver": "#c0c0c0",
    "skyblue": "#87ceeb",
    "slateblue": "#6a5acd",
    "slategray": "#708090",
    "slategrey": "#708090",
    "snow": "#fffafa",
    "springgreen": "#00ff7f",
    "steelblue": "#4682b4",
    "tan": "#d2b48c",
    "teal": "#008080",
    "thistle": "#d8bfd8",
    "tomato": "#ff6347",
    "turquoise": "#40e0d0",
    "violet": "#ee82ee",
    "wheat": "#f5deb3",
    "white": "#ffffff",
    "whitesmoke": "#f5f5f5",
    "yellow": "#ffff00",
    "yellowgreen": "#9acd32",
    "rebeccapurple": "#663399",
}

HEX_COLOR_PATTERN = re.compile(r"#(?:[0-9a-fA-F]{3}){1,2}")

BACKGROUND_CSS_COLORS_TO_HEX = {
    "bg_" + k: v
    for k, v in CSS_COLORS_TO_HEX.items()
}

OTHER_FMTS = {
    "bold": 1,
    "underline": 4,
    "deleted": 9,
    'grey': 30,
    'red': 31,
    'green': 32,
    'yellow': 33,
    'blue': 34,
    'magenta': 35,
    'cyan': 36,
    'white': 37,
}


def hex_to_rgb(hex_value):
    hex_value = hex_value.lstrip('#')
    hlen = len(hex_value)
    return tuple(
        int(hex_value[i:i + hlen // 3], 16) for i in range(0, hlen, hlen // 3))


def _hex_to_rgb_tuple(table):
    res = {}
    for k, v in table.items():
        res[k] = hex_to_rgb(v)
    return res


CSS_COLORS_TO_RGB = _hex_to_rgb_tuple(CSS_COLORS_TO_HEX)
BACKGROUND_CSS_COLORS_TO_RGB = _hex_to_rgb_tuple(BACKGROUND_CSS_COLORS_TO_HEX)


def _simple_code(index):
    return "\u001b[{}m".format(index)


def _color(r, g, b):
    return "\u001b[38;2;{};{};{}m".format(r, g, b)


def color_code(fmt):
    return _color(*CSS_COLORS_TO_RGB[fmt])


def end_code():
    return "\u001b[0m"


def _bg_color(r, g, b):
    return "\u001b[48;2;{};{};{}m".format(r, g, b)


def _fmt_dispatch(fmt):
    if fmt in OTHER_FMTS:
        return _simple_code(OTHER_FMTS[fmt])
    elif fmt in CSS_COLORS_TO_RGB:
        return _color(*CSS_COLORS_TO_RGB[fmt])
    elif fmt in BACKGROUND_CSS_COLORS_TO_RGB:
        return _bg_color(*BACKGROUND_CSS_COLORS_TO_RGB[fmt])
    elif HEX_COLOR_PATTERN.match(fmt):
        return _color(*hex_to_rgb(fmt))
    else:
        raise ValueError("unknown terminal fmt: {}".format(fmt))


def colored(text, *fmts):
    res = ""
    for fmt in fmts:
        if fmt is None:
            continue
        res += _fmt_dispatch(fmt)
    res += text + "\u001b[0m"
    return res


def red(text, *fmts):
    return colored(text, "red", *fmts)


def green(text, *fmts):
    return colored(text, "green", *fmts)


def blue(text, *fmts):
    return colored(text, "blue", *fmts)


def dodgerblue(text, *fmts):
    return colored(text, "dodgerblue", *fmts)


def lightskyblue(text, *fmts):
    return colored(text, "lightskyblue", *fmts)


def yellow(text, *fmts):
    return colored(text, "yellow", *fmts)


def orchid(text, *fmts):
    return colored(text, "orchid", *fmts)
