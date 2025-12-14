import sys
from matplotlib import cm

sys.path.append('../')

from fractals import GosperCurve
from rendering_pygame import draw_fractal

# Create the Gosper Curve (Flowsnake)
gosper = GosperCurve(10)

# Render - hexagonal space-filling curve with 60-degree angles
# Levels 4-6 work well (grows very fast!)
draw_fractal(
    gosper,
    init_pos=(0, 0),
    desired_recursion_level=5,
    window_size=(900, 900),
    edges_per_frame=200,
    cmap=cm.get_cmap('cool'),
    line_width=1,
)
