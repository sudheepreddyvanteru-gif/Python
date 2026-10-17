# Simple Pong game in Python 3 for beginners
# By V.Sudheep Reddy
# Part 4 : Moving the ball

import turtle

wn = turtle.Screen()
wn.title('Pong by @SudheepNSaharsh')
wn.bgcolor('black')
wn.setup(width=800, height=600)
wn.tracer(0)

# Paddle A
paddle_a = turtle.Turtle()
paddle_a.speed(0)
paddle_a.shape('square')
paddle_a.color('white')
paddle_a.shapesize(stretch_wid= 5, stretch_len = 1)
paddle_a.penup()
paddle_a.goto(350, 0)

# Paddle B
paddle_b = turtle.Turtle()
paddle_b.speed(0)
paddle_b.shape('square')
paddle_b.color('white')
paddle_b.shapesize(stretch_wid= 5, stretch_len = 1)
paddle_b.penup()
paddle_b.goto(-350, 0)

# Ball
ball = turtle.Turtle()
ball.speed(0)
ball.shape('square')
ball.color('white')
ball.penup()
ball.goto(0, 0)
ball.dx = 2.5
ball.dy = -2.5

# Scoreboard
score_a = 0
score_b = 0

scoreboard = turtle.Turtle()
scoreboard.speed(0)
scoreboard.color('white')
scoreboard.penup()
scoreboard.hideturtle()
scoreboard.goto(0, 260)
scoreboard.write(
    'Player A: 0  Player B: 0',
    align='center',
    font=('Courier', 24, 'normal')
)

# Functions
def paddle_a_up():
    y = paddle_a.ycor()
    y += 20
    paddle_a.sety(y)

def paddle_a_down():
    y = paddle_a.ycor()
    y -= 20
    paddle_a.sety(y)

def paddle_b_up():
    y = paddle_b.ycor()
    y += 20
    paddle_b.sety(y)

def paddle_b_down():
    y = paddle_b.ycor()
    y -= 20
    paddle_b.sety(y)

# Keyboard binding
wn.listen()
wn.onkeypress(paddle_a_up, 'a')
wn.onkeypress(paddle_a_down, 'c')
wn.onkeypress(paddle_b_up, 'Up')
wn.onkeypress(paddle_b_down, 'Down')

# Main game loop
def game_loop():
    global score_a, score_b

    wn.update()

    # Move the ball
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # Border checking
    if ball.ycor() > 290:
        ball.sety(290)
        ball.dy *= -1

    if ball.ycor() < -290:
            ball.sety(-290)
            ball.dy *= -1

    if ball.xcor() > 390:
        score_b += 1
        scoreboard.clear()
        scoreboard.write(
            f'Player A: {score_a}  Player B: {score_b}',
            align='center',
            font=('Courier', 24, 'normal')
        )
        ball.goto(0, 0)
        ball.dx *= -1

    if ball.xcor() < -390:
        score_a += 1
        scoreboard.clear()
        scoreboard.write(
            f'Player A: {score_a}  Player B: {score_b}',
            align='center',
            font=('Courier', 24, 'normal')
        )
        ball.goto(0, 0)
        ball.dx *= -1

    # Paddle collisions also adjust the vertical direction by impact point.
    if ball.dx > 0 and 330 <= ball.xcor() <= 360:
            offset = (ball.ycor() - paddle_a.ycor()) / 60
            if abs(offset) <= 1:
                ball.setx(330)
                ball.dx *= -1
                ball.dy = offset * 0.5 or (0.15 if ball.dy >= 0 else -0.15)

    if ball.dx < 0 and -360 <= ball.xcor() <= -330:
            offset = (ball.ycor() - paddle_b.ycor()) / 60
            if abs(offset) <= 1:
                ball.setx(-330)
                ball.dx *= -1
                ball.dy = offset * 0.5 or (0.15 if ball.dy >= 0 else -0.15)

    wn.ontimer(game_loop, 15)


game_loop()
turtle.done()