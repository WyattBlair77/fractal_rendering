#!/usr/bin/env python
import sys
sys.path.append('../')

from fractals import MooreCurve
from cli import create_parser, run_fractal_demo

if __name__ == '__main__':
    parser = create_parser('Moore Curve', default_level=6, default_cmap='gist_rainbow')
    args = parser.parse_args()

    run_fractal_demo(
        fractal_class=MooreCurve,
        fractal_name='moore',
        args=args,
        init_length=10,
    )
