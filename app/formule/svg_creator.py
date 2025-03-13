

HEAD = """<?xml version="1.0" standalone="yes"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
  "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="{width}" height="{height}" version="1.1" xmlns="http://www.w3.org/2000/svg">"""

END = """</svg>"""

LINE = """<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{line_width}" />"""

def create_svg_for(list_of_points, output_path: str, height: int, width: int, line_width: int):
    with open(output_path, "w") as file:
        file.write(HEAD.format(
            height= height,
            width= width,
        ))
        for line in list_of_points:
            file.write(LINE.format(
                x1= line.x1,
                x2= line.x2,
                y1= line.y1,
                y2= line.y2,
                line_width= line_width,
                color= line.paint.color,
            ))
        file.write(END)
