from math import sin, cos

HEAD = """<?xml version="1.0" standalone="yes"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
  "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="{width}" height="{height}" version="1.1" xmlns="http://www.w3.org/2000/svg">"""

END = """</svg>"""

LINE = """<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{line_width}" />"""

def create_svg_for(list_of_points, center_spiro, output_path: str, marges=20, angle=None):
    csx, csy = center_spiro
    with open(output_path, "w") as file:
        max_x = float('-inf')
        max_y = float('-inf')
        min_x = float('+inf')
        min_y = float('+inf')
        for line in list_of_points:
            x1 = line.p_from[0] - csx
            x2 = line.p_to[0] - csx
            y1 = line.p_from[1] - csy
            y2 = line.p_to[1] - csy
            if angle is not None:
                x1p = (x1 * cos(angle) - y1 * sin(angle))
                y1p = (x1 * sin(angle) + y1 * cos(angle))
                x2p = (x2 * cos(angle) - y2 * sin(angle))
                y2p = (x2 * sin(angle) + y2 * cos(angle))
                x1, y1, x2, y2 = x1p, y1p, x2p, y2p

            min_x = min(min_x, x1, x2)
            max_x = max(max_x, x1, x2)
            max_y = max(max_y, y1, y2)
            min_y = min(min_y, y1, y2)
        min_x -= marges
        max_x += marges
        max_y += marges
        min_y -= marges
        file.write(HEAD.format(
            width= max_x - min_x,
            height= max_y - min_y,
        ))
        for line in list_of_points:
            x1 = line.p_from[0] - csx
            x2 = line.p_to[0] - csx
            y1 = line.p_from[1] - csy
            y2 = line.p_to[1] - csy
            if angle is not None:
                x1p = (x1 * cos(angle) - y1 * sin(angle))
                y1p = (x1 * sin(angle) + y1 * cos(angle))
                x2p = (x2 * cos(angle) - y2 * sin(angle))
                y2p = (x2 * sin(angle) + y2 * cos(angle))
                x1, y1, x2, y2 = x1p, y1p, x2p, y2p
            file.write(LINE.format(
                x1= x1 - min_x,
                y1= (max_y - min_y) - (y1 - min_y),
                x2= x2 - min_x,
                y2= (max_y - min_y) - (y2 - min_y),
                line_width= line.stroke_width,
                color= line.color,
            ))
        file.write(END)
