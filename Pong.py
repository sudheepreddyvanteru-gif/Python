# Simple Pong game in Python for beginners
# By V.Sudheep Reddy
# Part 4 : Moving the ball

import turtle
import random

wn = turtle.Screen()
wn.title('Pong by @SudheepNSaharsh')
wn.bgcolor('black')
wn.setup(width=1.0, height=1.0)
wn.getcanvas().winfo_toplevel().state('zoomed')
wn.tracer(0)

court_half_width = wn.window_width() / 2
court_half_height = wn.window_height() / 2

# Paddle A
paddle_a = turtle.Turtle()
paddle_a.speed(0)
paddle_a.shape('square')
paddle_a.color('white')
paddle_a.shapesize(stretch_wid= 5, stretch_len = 1)
paddle_a.penup()
paddle_a.goto(-court_half_width + 50, 0)

# Paddle B
paddle_b = turtle.Turtle()
paddle_b.speed(0)
paddle_b.shape('square')
paddle_b.color('white')
paddle_b.shapesize(stretch_wid= 5, stretch_len = 1)
paddle_b.penup()
paddle_b.goto(court_half_width - 50, 0)

# Ball trail
trail = turtle.Turtle()
trail.speed(0)
trail.hideturtle()
trail.penup()
trail.pensize(6)
trail_points = []
trail_length = 24

# Ball
ball = turtle.Turtle()
ball.speed(0)
ball.shape('circle')
ball.color('white')
ball.penup()
ball.goto(0, 0)
ball.clear()
ball_speed = 8
ball.dx = random.choice((-ball_speed, ball_speed))
ball.dy = random.choice((-ball_speed, ball_speed))

# Scoreboard
score_a = 0
score_b = 0

scoreboard = turtle.Turtle()
scoreboard.speed(0)
scoreboard.color('white')
scoreboard.penup()
scoreboard.hideturtle()
scoreboard.goto(0, court_half_height - 100)
scoreboard.write(
    'Player A: 0  Player B: 0',
    align='center',
    font=('Courier', 24, 'normal')
)

# Paddle movement speeds
paddle_a_dy = 0
paddle_b_dy = 0
paddle_speed = 12

# Functions
def paddle_a_up():
    global paddle_a_dy
    paddle_a_dy = paddle_speed

def paddle_a_down():
    global paddle_a_dy
    paddle_a_dy = -paddle_speed

def paddle_b_up():
    global paddle_b_dy
    paddle_b_dy = paddle_speed

def paddle_b_down():
    global paddle_b_dy
    paddle_b_dy = -paddle_speed

def stop_paddle_a():
    global paddle_a_dy
    paddle_a_dy = 0

def stop_paddle_b():
    global paddle_b_dy
    paddle_b_dy = 0

def draw_ball_trail():
    trail_points.append((ball.xcor(), ball.ycor()))
    if len(trail_points) > trail_length:
        trail_points.pop(0)

    trail.clear()
    segment_count = len(trail_points) - 1
    for index in range(segment_count):
        shade = 40 + int(180 * (index + 1) / segment_count)
        trail.color(f'#{shade:02x}{shade:02x}{shade:02x}')
        trail.penup()
        trail.goto(trail_points[index])
        trail.pendown()
        trail.goto(trail_points[index + 1])
    trail.penup()

def reset_ball():
    ball.penup()
    ball.goto(0, 0)
    trail_points.clear()
    ball.dx = random.choice((-ball_speed, ball_speed))
    ball.dy = random.choice((-ball_speed, ball_speed))

# Keyboard binding
wn.listen()
wn.onkeypress(paddle_a_up, 'Up')
wn.onkeypress(paddle_a_down, 'Down')
wn.onkeypress(paddle_b_up, 'x')
wn.onkeypress(paddle_b_down, 'y')
wn.onkeyrelease(stop_paddle_a, 'Up')
wn.onkeyrelease(stop_paddle_a, 'Down')
wn.onkeyrelease(stop_paddle_b, 'x')
wn.onkeyrelease(stop_paddle_b, 'y')

# Main game loop
def game_loop():
    global score_a, score_b

    wn.update()

    paddle_a.sety(max(-court_half_height + 50, min(
        court_half_height - 50, paddle_a.ycor() + paddle_a_dy
    )))
    paddle_b.sety(max(-court_half_height + 50, min(
        court_half_height - 50, paddle_b.ycor() + paddle_b_dy
    )))

    # Move the ball
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # Border checking
    if ball.ycor() > court_half_height - 10:
        ball.sety(court_half_height - 10)
        ball.dy *= -1

    if ball.ycor() < -court_half_height + 10:
        ball.sety(-court_half_height + 10)
        ball.dy *= -1

    if ball.xcor() > court_half_width - 10:
        score_a += 1
        scoreboard.clear()
        scoreboard.write(
            f'Player A: {score_a}  Player B: {score_b}',
            align='center',
            font=('Courier', 24, 'normal')
        )
        reset_ball()

    if ball.xcor() < -court_half_width + 10:
        score_b += 1
        scoreboard.clear()
        scoreboard.write(
            f'Player A: {score_a}  Player B: {score_b}',
            align='center',
            font=('Courier', 24, 'normal')
        )
        reset_ball()

    # Paddle collisions also adjust the vertical direction by impact point.
    if ball.dx < 0 and paddle_a.xcor() - 10 <= ball.xcor() <= paddle_a.xcor() + 20:
            offset = (ball.ycor() - paddle_a.ycor()) / 60
            if abs(offset) <= 1:
                ball.setx(paddle_a.xcor() + 20)
                ball.dx *= -1
                ball.dy = offset * ball_speed or (ball_speed * 0.25 if ball.dy >= 0 else -ball_speed * 0.25)

    if ball.dx > 0 and paddle_b.xcor() - 20 <= ball.xcor() <= paddle_b.xcor() + 10:
            offset = (ball.ycor() - paddle_b.ycor()) / 60
            if abs(offset) <= 1:
                ball.setx(paddle_b.xcor() - 20)
                ball.dx *= -1
                ball.dy = offset * ball_speed or (ball_speed * 0.25 if ball.dy >= 0 else -ball_speed * 0.25)

    draw_ball_trail()
    wn.ontimer(game_loop, 15)


game_loop()
turtle.done()
