import turtle as t
import numpy as np

# Draw the curve function
def draw_fractal(fractal, init_pos, desired_recursion_level, speed=0, cmap=None):
    
    t.TurtleScreen._RUNNING = True

    print('--Making Fractal--')
    fractal_lines = fractal.generate(desired_recursion_level=desired_recursion_level)

    print('--Drawing--')
    screen = t.Screen()
    screen.colormode(1)

    t.penup()
    t.setposition(init_pos)
    t.pendown()
    t.speed(speed)

    for i, edge in enumerate(fractal_lines):

        if cmap is not None:
            
            color = cmap(i/len(fractal_lines))
            r, g, b = color[0], color[1], color[2]
            
            t.pencolor(r, g, b)

        t.setheading(0)
        t.left(edge['angle'])
        t.forward(edge['length'])

    print('--Finshed drawing--')

    screen.exitonclick()