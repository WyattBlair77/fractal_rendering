import pygame
import numpy as np


def draw_fractal(fractal, init_pos, desired_recursion_level,
                 window_size=(800, 800), line_width=1,
                 edges_per_frame=None, duration=None, cmap=None, fps=60,
                 background_color=(0, 0, 0), line_color=None, auto_scale=True, padding=50):
    """
    Render fractal using Pygame with animated progressive drawing.

    Args:
        fractal: Fractal object with generate() and compute_coordinates() methods
        init_pos: Starting position (used if auto_scale=False)
        desired_recursion_level: Recursion depth for fractal generation
        window_size: (width, height) tuple for the window
        line_width: Thickness of drawn lines
        edges_per_frame: Number of edges to draw per frame (overrides duration)
        duration: Target duration in seconds (used to calculate edges_per_frame)
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

    # Calculate edges_per_frame from duration if specified
    if edges_per_frame is not None:
        # Explicit edges_per_frame takes priority
        pass
    elif duration is not None and duration > 0:
        # Calculate edges_per_frame to achieve target duration
        total_frames = int(duration * fps)
        edges_per_frame = max(1, n // total_frames)
        print(f'--Target duration: {duration}s ({edges_per_frame} edges/frame)--')
    else:
        # Default: draw as fast as possible (all edges per frame)
        edges_per_frame = n

    # Auto-scale to fit window
    if auto_scale:
        coords = scale_to_window(coords, window_size, padding)
    else:
        # Just flip y-axis for screen coordinates (y increases downward)
        coords = coords.copy()
        coords[:, 1] = window_size[1] - coords[:, 1]

    # Pre-compute colors
    if line_color is not None:
        colors = [line_color] * n
    elif cmap is not None:
        colors = [tuple(int(c * 255) for c in cmap(i / n)[:3]) for i in range(n)]
    else:
        colors = [(255, 255, 255)] * n

    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption(f'Fractal - Level {desired_recursion_level} ({n} edges)')
    clock = pygame.time.Clock()

    # View transform state
    zoom = 1.0
    pan_offset = [0.0, 0.0]
    dragging = False
    last_mouse_pos = None
    window_center = (window_size[0] / 2, window_size[1] / 2)

    # Cached surface for fast pan/zoom (rendered at 1x scale)
    # We use a larger surface to allow some zoom without quality loss
    cache_scale = 2.0  # Render at 2x resolution for better zoom quality
    cache_size = (int(window_size[0] * cache_scale), int(window_size[1] * cache_scale))
    fractal_cache = pygame.Surface(cache_size)
    fractal_cache.fill(background_color)
    cache_valid = False

    def render_to_cache():
        """Render the full fractal to the cache surface at high resolution."""
        nonlocal cache_valid
        fractal_cache.fill(background_color)
        # Scale coordinates to cache size
        scale_factor = cache_scale
        for i in range(n):
            start = (int(coords[i][0] * scale_factor), int(coords[i][1] * scale_factor))
            end = (int(coords[i + 1][0] * scale_factor), int(coords[i + 1][1] * scale_factor))
            pygame.draw.line(fractal_cache, colors[i], start, end, max(1, int(line_width * scale_factor)))
        cache_valid = True

    def blit_cached_view():
        """Blit the cached surface to screen with current zoom and pan."""
        screen.fill(background_color)

        # The cached surface is at cache_scale resolution
        # At zoom=1.0, we want it to display at window_size
        scaled_size = (int(window_size[0] * zoom), int(window_size[1] * zoom))

        # Scale the cached surface
        if scaled_size[0] > 0 and scaled_size[1] > 0:
            scaled_surface = pygame.transform.smoothscale(fractal_cache, scaled_size)

            # Position: pan_offset is the top-left corner offset from centered position
            pos_x = int(pan_offset[0])
            pos_y = int(pan_offset[1])

            screen.blit(scaled_surface, (pos_x, pos_y))

        pygame.display.flip()

    def update_caption():
        """Update window title with zoom level."""
        zoom_str = f'{zoom:.1f}x' if zoom != 1.0 else ''
        if zoom_str:
            pygame.display.set_caption(f'Fractal - Level {desired_recursion_level} ({n} edges) - Zoom: {zoom_str}')
        else:
            pygame.display.set_caption(f'Fractal - Level {desired_recursion_level} ({n} edges)')

    # Fill background
    screen.fill(background_color)

    print(f'--Drawing {n} edges--')

    # Progressive drawing loop
    drawn_edges = 0
    running = True
    current_edges_per_frame = edges_per_frame
    needs_redraw = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    # Space to instantly complete
                    current_edges_per_frame = n
                elif event.key == pygame.K_r:
                    # Reset view
                    zoom = 1.0
                    pan_offset = [0.0, 0.0]
                    needs_redraw = True
                    update_caption()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    dragging = True
                    last_mouse_pos = event.pos
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False
                    last_mouse_pos = None
            elif event.type == pygame.MOUSEMOTION:
                if dragging and last_mouse_pos is not None:
                    dx = event.pos[0] - last_mouse_pos[0]
                    dy = event.pos[1] - last_mouse_pos[1]
                    pan_offset[0] += dx
                    pan_offset[1] += dy
                    last_mouse_pos = event.pos
                    needs_redraw = True
            elif event.type == pygame.MOUSEWHEEL:
                # Alternative mousewheel handling for some systems
                mouse_x, mouse_y = pygame.mouse.get_pos()
                old_zoom = zoom
                if event.y > 0:  # Scroll up - zoom in
                    zoom = min(zoom * 1.1, 50.0)
                elif event.y < 0:  # Scroll down - zoom out
                    zoom = max(zoom * 0.9, 0.1)
                # Adjust pan to keep mouse position fixed
                zoom_ratio = zoom / old_zoom
                pan_offset[0] = mouse_x - (mouse_x - pan_offset[0]) * zoom_ratio
                pan_offset[1] = mouse_y - (mouse_y - pan_offset[1]) * zoom_ratio
                needs_redraw = True
                update_caption()

        # Draw batch of edges during initial animation (directly to screen)
        if drawn_edges < n:
            end_idx = min(drawn_edges + current_edges_per_frame, n)
            for i in range(drawn_edges, end_idx):
                start = (int(coords[i][0]), int(coords[i][1]))
                end = (int(coords[i + 1][0]), int(coords[i + 1][1]))
                pygame.draw.line(screen, colors[i], start, end, line_width)

            drawn_edges = end_idx
            pygame.display.flip()

            # When animation completes, render to cache for smooth pan/zoom
            if drawn_edges >= n:
                print('--Caching fractal for smooth navigation--')
                render_to_cache()
        elif needs_redraw and cache_valid:
            blit_cached_view()
            needs_redraw = False

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
                 line_width=1, cmap=None, background_color=(0, 0, 0), line_color=None, padding=50):
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
    try:
        import cv2
    except ImportError:
        print("Error: opencv-python is required for PNG export.")
        print("Install with: pip install opencv-python")
        return

    print('--Making Fractal--')
    edges = fractal.generate(desired_recursion_level=desired_recursion_level)

    print('--Computing Coordinates--')
    coords = fractal.compute_coordinates(edges, start_pos=init_pos)
    n = len(coords) - 1

    # Scale to fit
    coords = scale_to_window(coords, size, padding)

    # Pre-compute colors (BGR for OpenCV)
    if line_color is not None:
        colors = [line_color[::-1]] * n  # Convert RGB to BGR
    elif cmap is not None:
        colors = [tuple(int(c * 255) for c in cmap(i / n)[:3])[::-1] for i in range(n)]
    else:
        colors = [(255, 255, 255)] * n

    # Create image with background
    frame = np.zeros((size[1], size[0], 3), dtype=np.uint8)
    frame[:] = background_color[::-1]  # BGR

    print(f'--Drawing {n} edges--')

    # Draw all edges
    for i in range(n):
        start = (int(coords[i][0]), int(coords[i][1]))
        end = (int(coords[i + 1][0]), int(coords[i + 1][1]))
        cv2.line(frame, start, end, colors[i], line_width)

    # Save to file
    cv2.imwrite(output_file, frame)
    print(f'--Saved to {output_file}--')


def save_fractal_video(fractal, init_pos, desired_recursion_level,
                       output_file='fractal.mp4', size=(900, 900),
                       line_width=1, cmap=None, background_color=(0, 0, 0), line_color=None,
                       padding=50, edges_per_frame=None, duration=None, fps=60):
    """
    Render fractal animation to MP4 video file.

    Args:
        fractal: Fractal object
        init_pos: Starting position
        desired_recursion_level: Recursion depth
        output_file: Output filename (MP4)
        size: (width, height) of output video
        line_width: Thickness of lines
        cmap: Matplotlib colormap
        background_color: RGB tuple for background
        padding: Padding from edges
        edges_per_frame: Edges drawn per frame (overrides duration)
        duration: Target duration in seconds (used to calculate edges_per_frame)
        fps: Frames per second of output video
    """
    try:
        import cv2
    except ImportError:
        print("Error: opencv-python is required for MP4 export.")
        print("Install with: pip install opencv-python")
        return

    print('--Making Fractal--')
    edges = fractal.generate(desired_recursion_level=desired_recursion_level)

    print('--Computing Coordinates--')
    coords = fractal.compute_coordinates(edges, start_pos=init_pos)
    n = len(coords) - 1

    # Calculate edges_per_frame from duration if specified
    if edges_per_frame is not None:
        # Explicit edges_per_frame takes priority
        pass
    elif duration is not None and duration > 0:
        # Calculate edges_per_frame to achieve target duration
        total_frames = int(duration * fps)
        edges_per_frame = max(1, n // total_frames)
        print(f'--Target duration: {duration}s ({edges_per_frame} edges/frame)--')
    else:
        # Default: draw as fast as possible (all edges in ~2 seconds of video)
        edges_per_frame = max(1, n // (fps * 2))

    # Scale to fit
    coords = scale_to_window(coords, size, padding)

    # Pre-compute colors (BGR for OpenCV)
    if line_color is not None:
        colors = [line_color[::-1]] * n  # Convert RGB to BGR
    elif cmap is not None:
        colors = [tuple(int(c * 255) for c in cmap(i / n)[:3])[::-1] for i in range(n)]
    else:
        colors = [(255, 255, 255)] * n

    # Initialize video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_file, fourcc, fps, size)

    # Create initial frame with background
    frame = np.zeros((size[1], size[0], 3), dtype=np.uint8)
    frame[:] = background_color[::-1]  # BGR

    print(f'--Recording {n} edges--')

    # Draw frames progressively
    drawn_edges = 0
    frame_count = 0

    while drawn_edges < n:
        end_idx = min(drawn_edges + edges_per_frame, n)

        for i in range(drawn_edges, end_idx):
            start = (int(coords[i][0]), int(coords[i][1]))
            end = (int(coords[i + 1][0]), int(coords[i + 1][1]))
            cv2.line(frame, start, end, colors[i], line_width)

        out.write(frame)
        drawn_edges = end_idx
        frame_count += 1

    # Hold final frame for 2 seconds
    hold_frames = fps * 2
    for _ in range(hold_frames):
        out.write(frame)

    out.release()
    print(f'--Saved to {output_file} ({frame_count + hold_frames} frames)--')
