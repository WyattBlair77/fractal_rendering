#!/usr/bin/env python
import sys
sys.path.append('../')

from fractals import SierpinskiArrowhead
from cli import create_parser, run_fractal_demo

if __name__ == '__main__':
    parser = create_parser('Sierpinski Arrowhead', default_level=10, default_cmap='magma')
    args = parser.parse_args()

    run_fractal_demo(
        fractal_class=SierpinskiArrowhead,
        fractal_name='sierpinski',
        args=args,
        init_length=500,
    )
