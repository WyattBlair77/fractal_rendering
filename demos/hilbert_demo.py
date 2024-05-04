import sys

sys.path.append('../')

from fractals import HilbertCurve
from rendering import draw_fractal 

# Set initial conditions:
init_pos = (-100, -100)
desired_final_length_size = 5

for desired_recursion_level in range(12):

    # infer init_length
    init_length = 5
    init_angle = 0

    # create curve
    hilbert_curve = HilbertCurve(init_length)

    # render curve
    draw_fractal(
        hilbert_curve, 
        init_pos=init_pos, 
        desired_recursion_level=desired_recursion_level, 
        speed=0
    )