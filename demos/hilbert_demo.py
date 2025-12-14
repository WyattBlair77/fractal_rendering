import sys
from matplotlib import cm

sys.path.append('../')

from fractals import HilbertCurve
from rendering_pygame import draw_fractal

# Set initial conditions
init_pos = (0, 0)

# Create curve
hilbert_curve = HilbertCurve(10)

# Render curve with Pygame (MUCH faster than turtle!)
# - edges_per_frame controls animation speed (higher = faster)
# - Press SPACE to instantly complete the drawing
# - Press ESC or close window to exit
draw_fractal(
    hilbert_curve,
    init_pos=init_pos,
    desired_recursion_level=7,
    window_size=(800, 800),
    edges_per_frame=200,
    cmap=cm.get_cmap('gist_rainbow'),
    line_width=1,
)