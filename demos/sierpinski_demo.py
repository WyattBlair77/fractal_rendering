#!/usr/bin/env python
import sys
sys.path.append('../')

from fractals import SierpinskiArrowhead
from cli import create_parser, run_fractal_demo, parse_levels

if __name__ == '__main__':
    parser = create_parser('Sierpinski Arrowhead', default_level=6, default_cmap='gist_rainbow')
    args = parser.parse_args()

    # Scale init_length based on max level to keep edges visible
    # Each level halves the edge length, so we need init_length = 2^level * min_edge_length
    # Using min_edge_length of 2 pixels for visibility
    levels = parse_levels(args.level)
    max_level = max(levels)
    init_length = (2 ** max_level) * 2  # Ensures ~2 pixel edges at highest level

    run_fractal_demo(
        fractal_class=SierpinskiArrowhead,
        fractal_name='sierpinski',
        args=args,
        init_length=init_length,
    )
