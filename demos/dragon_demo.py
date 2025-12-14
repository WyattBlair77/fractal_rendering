import sys
from matplotlib import cm

sys.path.append('../')

from fractals import DragonCurve
from rendering_pygame import draw_fractal

# Create the Dragon Curve
dragon = DragonCurve(10)

# Render - the dragon curve looks best at levels 12-16
# Press SPACE to instantly complete, ESC to exit
draw_fractal(
    dragon,
    init_pos=(0, 0),
    desired_recursion_level=14,
    window_size=(900, 900),
    edges_per_frame=500,
    cmap=cm.get_cmap('plasma'),
    line_width=1,
)
