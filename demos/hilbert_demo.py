#!/usr/bin/env python
import sys
sys.path.append('../')

from fractals import HilbertCurve
from cli import create_parser, run_fractal_demo

if __name__ == '__main__':
    parser = create_parser('Hilbert Curve', default_level=7, default_cmap='gist_rainbow')
    args = parser.parse_args()

    run_fractal_demo(
        fractal_class=HilbertCurve,
        fractal_name='hilbert',
        args=args,
        init_length=10,
    )
