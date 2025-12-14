import pygame
import numpy as np


def draw_fractal(fractal, init_pos, desired_recursion_level,
                 window_size=(800, 800), line_width=1,
                 edges_per_frame=100, cmap=None, fps=60,
                 background_color=(0, 0, 0), auto_scale=True, padding=50):
    """
    Render fractal using Pygame with animated progressive drawing.

    Args:
        fractal: Fractal object with generate() and compute_coordinates() methods
        init_pos: Starting position (used if auto_scale=False)
        desired_recursion_level: Recursion depth for fractal generation
        window_size: (width, height) tuple for the window
        line_width: Thickness of drawn lines
        edges_per_frame: Number of edges to draw per frame (controls animation speed)
        cmap: Matplotlib colormap for coloring (e.g., cm.get_cmap('gist_rainbow'))
        fps: Target frames per second
        background_color: RGB tuple for background
        auto_scale: If True, automatically scale and center the fractal to fit window
        padding: Padding from window edges when auto_scale=True
    """
    print('--Making Fractal--')
    edges = fractal.generate(desired_recursion_level=desired_recursion_level)

    print('--Computing Coordinates--')
    coords = fractal.compute_coordinates(edges, start_pos=init_pos)
    n = len(coords) - 1

    # Auto-scale to fit window
    if auto_scale:
        coords = scale_to_window(coords, window_size, padding)
    else:
        # Just flip y-axis for screen coordinates (y increases downward)
        coords = coords.copy()
        coords[:, 1] = window_size[1] - coords[:, 1]

    # Pre-compute colors
    if cmap is not None:
        colors = [tuple(int(c * 255) for c in cmap(i / n)[:3]) for i in range(n)]
    else:
        colors = [(255, 255, 255)] * n

    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption(f'Fractal - Level {desired_recursion_level} ({n} edges)')
    clock = pygame.time.Clock()

    # Fill background
    screen.fill(background_color)

    print(f'--Drawing {n} edges--')

    # Progressive drawing loop
    drawn_edges = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    # Space to instantly complete
                    edges_per_frame = n

        # Draw batch of edges
        if drawn_edges < n:
            end_idx = min(drawn_edges + edges_per_frame, n)
            for i in range(drawn_edges, end_idx):
                start = (int(coords[i][0]), int(coords[i][1]))
                end = (int(coords[i + 1][0]), int(coords[i + 1][1]))
                pygame.draw.line(screen, colors[i], start, end, line_width)

            drawn_edges = end_idx
            pygame.display.flip()

        clock.tick(fps)

    print('--Finished drawing--')
    pygame.quit()


def scale_to_window(coords, window_size, padding=50):
    """Scale and center coordinates to fit within window with padding."""
    coords = coords.copy()

    # Find bounds
    min_x, min_y = coords.min(axis=0)
    max_x, max_y = coords.max(axis=0)

    # Calculate scale to fit in window with padding
    width = max_x - min_x
    height = max_y - min_y

    available_width = window_size[0] - 2 * padding
    available_height = window_size[1] - 2 * padding

    scale = min(available_width / width, available_height / height) if width > 0 and height > 0 else 1

    # Center the fractal
    center_x = (min_x + max_x) / 2
    center_y = (min_y + max_y) / 2

    # Transform: center at origin, scale, then translate to window center
    coords[:, 0] = (coords[:, 0] - center_x) * scale + window_size[0] / 2
    coords[:, 1] = (coords[:, 1] - center_y) * scale + window_size[1] / 2

    # Flip y-axis for screen coordinates
    coords[:, 1] = window_size[1] - coords[:, 1]

    return coords


def save_fractal(fractal, init_pos, desired_recursion_level,
                 output_file='fractal.png', size=(2000, 2000),
                 line_width=1, cmap=None, background_color=(0, 0, 0), padding=50):
    """
    Render fractal to an image file (no animation).

    Args:
        fractal: Fractal object
        init_pos: Starting position
        desired_recursion_level: Recursion depth
        output_file: Output filename (PNG)
        size: (width, height) of output image
        line_width: Thickness of lines
        cmap: Matplotlib colormap
        background_color: RGB tuple for background
        padding: Padding from edges
    """
    print('--Making Fractal--')
    edges = fractal.generate(desired_recursion_level=desired_recursion_level)

    print('--Computing Coordinates--')
    coords = fractal.compute_coordinates(edges, start_pos=init_pos)
    n = len(coords) - 1

    # Scale to fit
    coords = scale_to_window(coords, size, padding)

    # Pre-compute colors
    if cmap is not None:
        colors = [tuple(int(c * 255) for c in cmap(i / n)[:3]) for i in range(n)]
    else:
        colors = [(255, 255, 255)] * n

    # Initialize Pygame in headless mode
    pygame.init()
    surface = pygame.Surface(size)
    surface.fill(background_color)

    print(f'--Drawing {n} edges--')

    # Draw all edges
    for i in range(n):
        start = (int(coords[i][0]), int(coords[i][1]))
        end = (int(coords[i + 1][0]), int(coords[i + 1][1]))
        pygame.draw.line(surface, colors[i], start, end, line_width)

    # Save to file
    pygame.image.save(surface, output_file)
    print(f'--Saved to {output_file}--')

    pygame.quit()
