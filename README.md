# fractal_rendering
Helping a friend understand how fractals are closely related to recursion.

# uses two functions:
- curve(current_curve, current_level, desired_level): \n
-- generates a curve, which I define as a list of dictionaries like this: \n
--- [{'length': int, 'angle': int (degrees)}, ...]

- draw_curve(curve, init_pos):
-- draws the curve which it is passed using the turtle library
