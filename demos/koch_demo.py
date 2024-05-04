import sys

sys.path.append('../')

from fractals import KochCurve
from rendering import draw_fractal 

# Set initial conditions:
init_pos = (-100, 0)
desired_final_length_size = 5

for desired_recursion_level in range(12):

    # infer init_length
    init_length = desired_final_length_size * 2**desired_recursion_level
    init_angle = 0

    # create curve
    koch_curve = KochCurve(init_length, init_angle)

    # render curve
    draw_fractal(
        koch_curve, 
        init_pos=init_pos, 
        desired_recursion_level=desired_recursion_level, 
        speed=0
    )