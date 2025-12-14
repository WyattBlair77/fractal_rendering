#!/usr/bin/env python
import sys
sys.path.append('../')

from fractals import DragonCurve
from cli import create_parser, run_fractal_demo

if __name__ == '__main__':
    parser = create_parser('Dragon Curve', default_level=14, default_cmap='gist_rainbow')
    args = parser.parse_args()

    run_fractal_demo(
        fractal_class=DragonCurve,
        fractal_name='dragon',
        args=args,
        init_length=10,
    )
