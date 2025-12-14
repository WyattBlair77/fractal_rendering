import argparse
from matplotlib import cm


# Color presets
BACKGROUND_PRESETS = {
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'dark-gray': (30, 30, 30),
    'light-gray': (200, 200, 200),
    'navy': (10, 25, 47),
    'charcoal': (40, 44, 52),
}

LINE_COLOR_PRESETS = {
    'white': (255, 255, 255),
    'black': (0, 0, 0),
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'cyan': (0, 255, 255),
    'magenta': (255, 0, 255),
    'yellow': (255, 255, 0),
    'orange': (255, 165, 0),
}


def parse_color(value, presets):
    """Parse color from preset name or hex code (#RRGGBB)."""
    if value in presets:
        return presets[value]
    if value.startswith('#') and len(value) == 7:
        return tuple(int(value[i:i+2], 16) for i in (1, 3, 5))
    raise argparse.ArgumentTypeError(
        f"Invalid color: {value}. Use preset name or #RRGGBB hex code."
    )


def create_parser(fractal_name, default_level=5, default_cmap='gist_rainbow'):
    """
    Create a standard argument parser for fractal demos.

    Args:
        fractal_name: Name of the fractal for help text
        default_level: Default recursion level
        default_cmap: Default colormap name

    Returns:
        Configured argparse.ArgumentParser
    """
    parser = argparse.ArgumentParser(
        description=f'Render the {fractal_name} fractal',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python %(prog)s -l 5                          # Render at level 5
  python %(prog)s -l 3,4,5,6                    # Render levels 3, 4, 5, 6 sequentially
  python %(prog)s -l 7 --export png             # Export to PNG
  python %(prog)s -l 7 --export mp4             # Export to MP4 video
  python %(prog)s -l 7 -d 30                    # Render over 30 seconds
  python %(prog)s -l 7 -d 10 --export mp4       # 10-second MP4 video
  python %(prog)s -l 7 -o my_fractal.png        # Custom output filename

Color options:
  python %(prog)s -l 5 --bg navy                # Navy background
  python %(prog)s -l 5 --bg "#1a1a2e"           # Custom hex background
  python %(prog)s -l 5 --line-color cyan        # Solid cyan lines (no gradient)
  python %(prog)s -l 5 --bg white --cmap viridis  # White bg with gradient
        """
    )

    parser.add_argument(
        '-l', '--level', '--levels',
        type=str,
        default=str(default_level),
        help=f'Recursion level(s). Single value or comma-separated list (default: {default_level})'
    )

    parser.add_argument(
        '--export',
        type=str,
        choices=['png', 'mp4'],
        default=None,
        help='Export format instead of displaying window (png or mp4)'
    )

    parser.add_argument(
        '-o', '--output',
        type=str,
        default=None,
        help='Output filename (default: {fractal}_level{N}.{ext})'
    )

    parser.add_argument(
        '--size',
        type=int,
        default=900,
        help='Window/image size in pixels (default: 900)'
    )

    parser.add_argument(
        '--line-width',
        type=int,
        default=1,
        help='Line thickness (default: 1)'
    )

    parser.add_argument(
        '--cmap',
        type=str,
        default=default_cmap,
        help=f'Matplotlib colormap name (default: {default_cmap})'
    )

    parser.add_argument(
        '--bg', '--background',
        type=str,
        default='black',
        dest='background',
        help='Background color. Presets: black, white, dark-gray, light-gray, navy, charcoal. Or hex: #RRGGBB'
    )

    parser.add_argument(
        '--line-color',
        type=str,
        default=None,
        help='Solid line color (disables gradient). Presets: white, black, red, green, blue, cyan, magenta, yellow, orange. Or hex: #RRGGBB'
    )

    parser.add_argument(
        '--edges-per-frame',
        type=int,
        default=None,
        help='Edges drawn per frame (overrides --duration if set)'
    )

    parser.add_argument(
        '-d', '--duration',
        type=float,
        default=None,
        help='Target duration in seconds for the animation (e.g., --duration 30)'
    )

    parser.add_argument(
        '--fps',
        type=int,
        default=60,
        help='Frames per second for display/video (default: 60)'
    )

    return parser


def parse_levels(level_str):
    """Parse level string into list of integers."""
    levels = []
    for part in level_str.split(','):
        part = part.strip()
        if part:
            levels.append(int(part))
    return levels


def get_colormap(cmap_name):
    """Get matplotlib colormap by name."""
    return cm.get_cmap(cmap_name)


def run_fractal_demo(fractal_class, fractal_name, args, init_length=10, **fractal_kwargs):
    """
    Run the fractal demo with parsed arguments.

    Args:
        fractal_class: The fractal class to instantiate
        fractal_name: Name for output files
        args: Parsed argparse namespace
        init_length: Initial length for fractal
        **fractal_kwargs: Additional kwargs for fractal constructor
    """
    from rendering_pygame import draw_fractal, save_fractal, save_fractal_video, save_multilevel_video

    levels = parse_levels(args.level)
    cmap = get_colormap(args.cmap)
    window_size = (args.size, args.size)
    background_color = parse_color(args.background, BACKGROUND_PRESETS)
    line_color = parse_color(args.line_color, LINE_COLOR_PRESETS) if args.line_color else None

    if args.export == 'mp4' and len(levels) > 1:
        # Multiple levels -> single stitched video
        if args.output:
            output_file = args.output
        else:
            level_str = '_'.join(str(l) for l in levels)
            output_file = f"{fractal_name}_levels_{level_str}.mp4"

        save_multilevel_video(
            fractal_class=fractal_class,
            levels=levels,
            init_length=init_length,
            fractal_kwargs=fractal_kwargs,
            output_file=output_file,
            size=window_size,
            line_width=args.line_width,
            cmap=cmap,
            background_color=background_color,
            line_color=line_color,
            edges_per_frame=args.edges_per_frame,
            duration=args.duration,
            fps=args.fps,
        )
        print(f"Saved: {output_file}")
        return

    for level in levels:
        # Create fresh fractal instance for each level
        fractal = fractal_class(init_length, **fractal_kwargs)

        if args.export == 'png':
            # Export to PNG (separate file per level)
            if args.output:
                output_file = args.output if len(levels) == 1 else f"{args.output.rsplit('.', 1)[0]}_level{level}.png"
            else:
                output_file = f"{fractal_name}_level{level}.png"

            save_fractal(
                fractal,
                init_pos=(0, 0),
                desired_recursion_level=level,
                output_file=output_file,
                size=window_size,
                line_width=args.line_width,
                cmap=cmap,
                background_color=background_color,
                line_color=line_color,
            )
            print(f"Saved: {output_file}")

        elif args.export == 'mp4':
            # Single level MP4
            if args.output:
                output_file = args.output
            else:
                output_file = f"{fractal_name}_level{level}.mp4"

            save_fractal_video(
                fractal,
                init_pos=(0, 0),
                desired_recursion_level=level,
                output_file=output_file,
                size=window_size,
                line_width=args.line_width,
                cmap=cmap,
                background_color=background_color,
                line_color=line_color,
                edges_per_frame=args.edges_per_frame,
                duration=args.duration,
                fps=args.fps,
            )
            print(f"Saved: {output_file}")

        else:
            # Display in window
            draw_fractal(
                fractal,
                init_pos=(0, 0),
                desired_recursion_level=level,
                window_size=window_size,
                line_width=args.line_width,
                cmap=cmap,
                background_color=background_color,
                line_color=line_color,
                edges_per_frame=args.edges_per_frame,
                duration=args.duration,
                fps=args.fps,
            )
