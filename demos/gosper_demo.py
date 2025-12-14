#!/usr/bin/env python
import sys
sys.path.append('../')

from fractals import GosperCurve
from cli import create_parser, run_fractal_demo

if __name__ == '__main__':
    parser = create_parser('Gosper Curve (Flowsnake)', default_level=5, default_cmap='gist_rainbow')
    args = parser.parse_args()

    run_fractal_demo(
        fractal_class=GosperCurve,
        fractal_name='gosper',
        args=args,
        init_length=10,
    )
