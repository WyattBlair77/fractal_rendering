# fractal_rendering
Helping a friend understand how fractals are closely related to recursion. Run one of the demos to see it in action. 

# First define the fractal as an extension of the `Fractal` class
The only thing the class needs is an update function. This function takes a list of edges in and returns the new list of edges based on the rule set that that the specific fractal uses on each iteration.

# Then render the fractal
Then simply pass the curve and the desired recursion limit into the `draw_fractal` function.