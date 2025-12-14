#!/usr/bin/env python
import sys
sys.path.append('../')

from fractals import KochCurve
from cli import create_parser, run_fractal_demo

# KochCurve needs init_angle as well, so we use a wrapper
class KochCurveWrapper:
    def __init__(self, init_length):
        self._curve = KochCurve(init_length, init_angle=0)

    def generate(self, desired_recursion_level):
        return self._curve.generate(desired_recursion_level)

    def compute_coordinates(self, edges, start_pos=(0, 0)):
        return self._curve.compute_coordinates(edges, start_pos)

if __name__ == '__main__':
    parser = create_parser('Koch Curve', default_level=12, default_cmap='gist_rainbow')
    args = parser.parse_args()

    run_fractal_demo(
        fractal_class=KochCurveWrapper,
        fractal_name='koch',
        args=args,
        init_length=500,
    )
