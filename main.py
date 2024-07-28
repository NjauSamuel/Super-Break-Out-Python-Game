from turtle import Turtle, mainloop, listen, onkeypress, onkeyrelease, tracer, ontimer, Screen, bye
from random import choice

class Target(Turtle):
    colors = ['green', 'orange', 'yellow', 'pink', 'purple', 'gold', 'gray', 'brown', 'white']

    def __init__(self, x, y):
        super().__init__()
        self.white = False
        self.shapesize(1, 2.5)
        self.color(choice(self.colors))
        self.shape('square')
        self.penup()
        self.goto(x, y)

class Player(Turtle):
    def __init__(self):
        super().__init__()
        self.shapesize(1, 5)
        self.color('blue')
        self.shape('square')
        self.penup()
        self.goto(0, -250)
        self.speed = 20  # Added speed attribute
        self.moving_left = False  # Added moving_left attribute
        self.moving_right = False  # Added moving_right attribute

    def goleft(self):
        self.moving_left = True  # Set moving_left to True
        self.move_left()  # Start moving left

    def goright(self):
        self.moving_right = True  # Set moving_right to True
        self.move_right()  # Start moving right

    def move_left(self):
        if self.moving_left:
            if self.xcor() >= -240:
                self.setx(self.xcor() - self.speed)  # Move left by speed
            ontimer(self.move_left, 20)  # Repeat after 20 milliseconds

    def move_right(self):
        if self.moving_right:
            if self.xcor() <= 240:
                self.setx(self.xcor() + self.speed)  # Move right by speed
            ontimer(self.move_right, 20)  # Repeat after 20 milliseconds

    def stop_left(self):
        self.moving_left = False  # Stop moving left

    def stop_right(self):
        self.moving_right = False  # Stop moving right

class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.shapesize(1)
        self.color('red')
        self.shape('circle')
        self.penup()
        self.goto(0, 0)  # Initial position of the ball

class Game:
    tx, ty = -250, 200  # Adjusted starting y-coordinate for targets
    dy = 2  # Increased ball speed
    dx = choice([-.5, .5])
    targets = []

    def __init__(self):
        tracer(0)
        self.pl = Player()
        self.ball = Ball()
        for _ in range(5):
            for _ in range(10):
                target = Target(self.tx, self.ty)
                self.targets.append(target)
                self.tx += 55
            self.ty -= 25
            self.tx = -250
        tracer(1)

    def update(self):
        if self.ball.ycor() < -300:
            self.game_over()  # Call game_over when ball goes off screen
            return

        if self.ball.ycor() > 300:
            self.dy *= -1

        if self.ball.ycor() >= 80:
            for target in self.targets:
                if not target.white:
                    if self.ball.ycor() >= target.ycor() - 25:
                        if self.ball.xcor() >= target.xcor() - 25:
                            if self.ball.xcor() <= target.xcor() + 25:
                                self.dy *= -1
                                target.color('black')
                                target.white = True
                                break

        if self.ball.xcor() <= -270 or self.ball.xcor() >= 260:
            self.dx *= -1
        if self.ball.ycor() <= self.pl.ycor() + 25:
            if self.ball.xcor() >= self.pl.xcor() - 50:
                if self.ball.xcor() <= self.pl.xcor() + 50:
                    self.dy *= -1
        self.ball.setpos(self.ball.xcor() + self.dx * 6, self.ball.ycor() - self.dy * 6)  # Increased ball speed
        ontimer(self.update, 20)  # Schedule the next update in 20 milliseconds

    def game_over(self):
        self.ball.hideturtle()
        game_over_message = Turtle()
        game_over_message.hideturtle()
        game_over_message.color("white")
        game_over_message.penup()
        game_over_message.goto(0, 0)
        game_over_message.write("Game Over", align="center", font=("Arial", 24, "normal"))
        ontimer(bye, 3000)  # Exit the game gracefully after 3 seconds

def enable_keys(pl):
    onkeypress(pl.goleft, "Left")
    onkeypress(pl.goright, "Right")
    onkeyrelease(pl.stop_left, "Left")  # Stop moving left when key is released
    onkeyrelease(pl.stop_right, "Right")  # Stop moving right when key is released

def start():
    screen = Screen()
    screen.setup(width=600, height=600)  # Set the screen dimensions
    screen.bgcolor(0, 0, 0)
    game = Game()
    enable_keys(game.pl)
    listen()
    game.update()  # Start the game updates

if __name__ == '__main__':
    start()
    mainloop()
