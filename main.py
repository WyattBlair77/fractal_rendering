import turtle

# Set initial conditions:
init_pos = (-250, 0)
desired_level = 12
desired_final_length_size = 5


# Generate the curve function
def curve(current_curve, current_level, desired_level):
    print('Current Level:', current_level)

    if desired_level == current_level:
        return current_curve
    else:
        new_curve = []
        for edge in current_curve:
            new_curve.append({'length': edge['length']/2, 'angle': edge['angle'] + 45})
            new_curve.append({'length': edge['length']/2, 'angle': edge['angle'] - 45})
        return curve(new_curve, current_level+1, desired_level)


# Draw the curve function
def draw_curve(curve, init_pos):
    print('--Drawing--')
    t = turtle.Turtle()
    t.penup()
    t.setposition(init_pos)
    t.pendown()
    t.speed(0)

    for edge in curve:
        t.setheading(0)
        t.left(edge['angle'])
        t.forward(edge['length'])

    print('--Finshed drawing--')
    turtle.done()


# Determine scale
init_length = desired_final_length_size * 2**desired_level
init_koch = [{'length': init_length, 'angle': 0}]

# Run functions
koch_curve = curve(init_koch, 0, desired_level)
draw_curve(koch_curve, init_pos)
