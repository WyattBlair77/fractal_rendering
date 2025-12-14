import sys
from matplotlib import cm

sys.path.append('../')

from fractals import MooreCurve
from rendering_pygame import draw_fractal

# Create the Moore Curve (closed-loop Hilbert variant)
moore = MooreCurve(10)

# Render - forms a complete closed loop, unlike Hilbert
# Levels 5-7 work well
draw_fractal(
    moore,
    init_pos=(0, 0),
    desired_recursion_level=6,
    window_size=(900, 900),
    edges_per_frame=200,
    cmap=cm.get_cmap('gist_rainbow'),
    line_width=1,
)
