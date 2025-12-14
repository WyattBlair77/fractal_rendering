import sys
from matplotlib import cm

sys.path.append('../')

from fractals import LevyCCurve
from rendering_pygame import draw_fractal

# Create the Levy C Curve
levy = LevyCCurve(400)

# Render - creates beautiful symmetric tree-like patterns
# Levels 12-16 show the fractal nature well
draw_fractal(
    levy,
    init_pos=(0, 0),
    desired_recursion_level=14,
    window_size=(900, 900),
    edges_per_frame=500,
    cmap=cm.get_cmap('viridis'),
    line_width=1,
)
