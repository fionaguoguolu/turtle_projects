import turtle
import math

mandala = True
# Create a turtle (pen)
pen = turtle.Turtle()
pen.speed(0)  # Fastest speed
pen.penup()  # Start with the pen up
pen.shape("square")
pen.hideturtle()
# Set up turtle screen
screen = turtle.Screen()
pen_down = False

def left_click(x, y):
    global pen_down
    pen_down = not pen_down

# Bind mouse events
screen.onscreenclick(left_click, 1)  # Left-click to start drawing

def get_turtlexy():
    canvas = screen.getcanvas()
    x, y = canvas.winfo_pointerxy()
    
    # Get actual turtle window size
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    # Get turtle window position on the screen
    canvas_x = canvas.winfo_rootx()
    canvas_y = canvas.winfo_rooty()
    
    # Convert screen coordinates to turtle coordinates
    turtle_x = x - canvas_x - (canvas_width // 2)
    turtle_y = (canvas_height // 2) - (y - canvas_y)
    return turtle_x, turtle_y

# Function to print mouse coordinates continuously
# Function to track mouse position and stamp continuously
def track_mouse():
    global pen_down
    if not pen_down:
        screen.ontimer(track_mouse, 2)
        return
    x, y = get_turtlexy()
    pen.goto(x, y)
    pen.stamp()
    if mandala:
        pen.setheading(math.degrees(math.atan2(y, x)) + 90)
        radius = math.sqrt(x ** 2 + y ** 2)
        for _ in range(7):
            pen.circle(radius, 45)
            pen.stamp()
    # Keep updating every 100ms
    screen.ontimer(track_mouse, 2)
    
screen.tracer(0)
# Start tracking mouse position
screen.ontimer(track_mouse, 2)  # Start tracking after 2ms

def set_yellow():
    pen.color("yellow")
    
def set_red():
    pen.color("red")

def set_blue():
    pen.color("blue")

def set_turquoise():
    pen.color("turquoise")

def set_orange():
    pen.color("orange")

def set_pink():
    pen.color("pink")

def set_green():
    pen.color("green")

screen.onkey(set_yellow, "y")
screen.onkey(set_red, "r")
screen.onkey(set_blue, "b")
screen.onkey(set_turquoise, "t")
screen.onkey(set_orange, "o")
screen.onkey(set_pink, "p")
screen.onkey(set_green, "g")
screen.listen()
turtle.done()
# Keep the window open
screen.mainloop()
