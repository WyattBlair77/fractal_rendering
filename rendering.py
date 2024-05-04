import turtle as t

# Draw the curve function
def draw_fractal(fractal, init_pos, desired_recursion_level, speed=0):
    
    t.TurtleScreen._RUNNING = True

    print('--Making Fractal--')
    fractal_lines = fractal.generate(desired_recursion_level=desired_recursion_level)

    print('--Drawing--')

    t.penup()
    t.setposition(init_pos)
    t.pendown()
    t.speed(speed)

    for edge in fractal_lines:
        t.setheading(0)
        t.left(edge['angle'])
        t.forward(edge['length'])

    print('--Finshed drawing--')

    screen = t.Screen()
    screen.exitonclick()