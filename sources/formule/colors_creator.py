from colorsys import hsv_to_rgb
from random import randint

def hex_to_rgb(hex_color):
    """Convert a hex color (e.g. "#ACDDDE") to an (R, G, B) tuple."""
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    """Convert an (R, G, B) tuple to a hex color string."""
    return "#{:02X}{:02X}{:02X}".format(*rgb)

def interpolate_colors(color1, color2, t):
    """
    Interpolate between two RGB colors.
    t should be between 0 (color1) and 1 (color2).
    """
    return (
        int(color1[0] + (color2[0] - color1[0]) * t),
        int(color1[1] + (color2[1] - color1[1]) * t),
        int(color1[2] + (color2[2] - color1[2]) * t),
    )

def smooth_color_generator(colors, steps, easing=None):
    """
    Create a generator that yields colors as hex strings.
    
    Parameters:
      colors: iterable of hex color strings.
      steps: the number of intermediate colors between each pair.
      
    The generator smoothly interpolates between colors and finally connects 
    the last color back to the first.
    """

    if easing is None:
        easing = lambda t: t

    rgb_colors = [hex_to_rgb(c) for c in colors]
    n = len(rgb_colors)
    
    i = 0
    while True:
        start = rgb_colors[i]
        end = rgb_colors[(i+1) % n]
        for step in range(steps):
            t = step / steps
            rgb_interp = interpolate_colors(start, end, easing(t))
            yield rgb_to_hex(rgb_interp)
        i  = (i+1)%n


def progressive_color_arc_en_ciel(nb_points):
    hue = 0.0
    pas = 3 / nb_points # 2 = nombre de cycles
    while True:
        yield "#{}{}{}".format(*map(lambda n:hex(int(255*n))[2:].zfill(2), hsv_to_rgb(hue, 1, 1)))
        hue = (hue + pas)%1.0





def gen_random_color_scheme(i=None):

    intervals = [
        None,
        ("#957DAD", "#FFDFD3"),
        ("#8B52CB", "#F7D903"), # Woman in a glass room
        ("#AA0815", "#3D9BE1"), # Pile of winterwears
        ("#360258", "#AF1D61"), # Sunset festival
        ("#FFCE08", "#1259B8"), # Always shining
        ("#E37324", "#1F1FD1"), # Creative gradient
        ("#41BBF4", "#EC4087"), # Vivid and spring
        ("#88d8b0", "#f96e5a"), # Colorful beach
        ("#f56600", "#e026a3"), # Old Nyc subway colors
        ("#00ff41", "#003b00"), # Matrix code green
        ("#772A53", "#E87C5D"), # Dull illustration
    ]

    if i is None:
        interval = intervals[randint(0, len(intervals) - 1)]
    else:
        interval = intervals[i % (len(intervals) - 1)]

    if interval == None:
        return progressive_color_arc_en_ciel

    else:
        return lambda nb_points : smooth_color_generator(interval, nb_points)