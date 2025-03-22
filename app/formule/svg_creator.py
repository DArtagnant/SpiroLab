

HEAD = """<?xml version="1.0" standalone="yes"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
  "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="{width}" height="{height}" version="1.1" xmlns="http://www.w3.org/2000/svg">"""

END = """</svg>"""

LINE = """<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{line_width}" />"""

def create_svg_for(list_of_points, center_spiro, output_path: str, marges=20):
    csx, csy = center_spiro
    with open(output_path, "w") as file:
        max_x = float('-inf')
        max_y = float('-inf')
        min_x = float('+inf')
        min_y = float('+inf')
        for line in list_of_points:
            min_x = min(min_x, (line.p_from[0] - csx), (line.p_to[0] - csx))
            max_x = max(max_x, (line.p_from[0] - csx), (line.p_to[0] - csx))
            max_y = max(max_y, (line.p_from[1] - csy), (line.p_to[1] - csy))
            min_y = min(min_y, (line.p_from[1] - csy), (line.p_to[1] - csy))
        min_x -= marges
        max_x += marges
        max_y += marges
        min_y -= marges
        file.write(HEAD.format(
            width= max_x - min_x,
            height= max_y - min_y,
        ))
        for line in list_of_points:
            file.write(LINE.format(
                x1= (line.p_from[0] - csx) - min_x,
                y1= -(line.p_from[1] - csy) - min_y,
                x2= (line.p_to[0] - csx) - min_x,
                y2= -(line.p_to[1] - csy) - min_y,
                line_width= line.stroke_width,
                color= line.color,
            ))
        file.write(END)
