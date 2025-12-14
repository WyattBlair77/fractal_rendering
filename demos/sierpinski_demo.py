import sys
from matplotlib import cm

sys.path.append('../')

from fractals import SierpinskiArrowhead
from rendering_pygame import draw_fractal

# Create the Sierpinski Arrowhead Curve
sierpinski = SierpinskiArrowhead(500)

# Render - draws the Sierpinski triangle as a single continuous line
# Levels 8-12 work well
draw_fractal(
    sierpinski,
    init_pos=(0, 0),
    desired_recursion_level=10,
    window_size=(900, 900),
    edges_per_frame=300,
    cmap=cm.get_cmap('magma'),
    line_width=1,
)
