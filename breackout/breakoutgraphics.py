"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman, 
and Jerry Liao.

This program is a game which is named "Breakout". The objective of the game is to use a paddle to bounce a ball into
a wall of bricks, removing bricks when the ball hits them, with the ultimate goal of removing all the bricks to
win the game.

Classes:
BreakoutGraphics: This class initializes the game environment, controls the paddle and ball dynamics, and manages the
game state.

Methods:

__init__: This method initializes the game, creating the window, the paddle, the ball, the bricks, and the labels for
remaining bricks and life of game. It also sets up mouse listeners for player interaction.

reset_position: This method moves the paddle based on the user's mouse movements.

start: This method sets the initial ball velocity and starts the game when the user clicks the mouse.

win and lose: These methods display a winning or losing message when the game ends, depending on whether the player
has won or lost.

bounce: This method controls the movement of the ball, how it bounces off walls, the paddle, and bricks,
and how it removes bricks upon collision.

restart: This method resets the game state to its initial state.
"""
from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel
from campy.gui.events.mouse import onmouseclicked, onmousemoved
from campy.gui.events.timer import pause
import random

BRICK_SPACING = 5      # Space between bricks (in pixels). This space is used for horizontal and vertical spacing
BRICK_WIDTH = 40       # Width of a brick (in pixels)
BRICK_HEIGHT = 15      # Height of a brick (in pixels)
BRICK_ROWS = 10        # Number of rows of bricks
BRICK_COLS = 10        # Number of columns of bricks
BRICK_OFFSET = 50      # Vertical offset of the topmost brick from the window top (in pixels)
BALL_RADIUS = 10       # Radius of the ball (in pixels)
PADDLE_WIDTH = 75      # Width of the paddle (in pixels)
PADDLE_HEIGHT = 15     # Height of the paddle (in pixels)
PADDLE_OFFSET = 50     # Vertical offset of the paddle from the window bottom (in pixels)
INITIAL_Y_SPEED = 7    # Initial vertical speed for the ball
MAX_X_SPEED = 5        # Maximum initial horizontal speed for the ball
DELAY = 10


class BreakoutGraphics:

    def __init__(self, ball_radius=BALL_RADIUS, paddle_width=PADDLE_WIDTH, paddle_height=PADDLE_HEIGHT,
                 paddle_offset=PADDLE_OFFSET, brick_rows=BRICK_ROWS, brick_cols=BRICK_COLS, brick_width=BRICK_WIDTH,
                 brick_height=BRICK_HEIGHT, brick_offset=BRICK_OFFSET, brick_spacing=BRICK_SPACING, title='Breakout'):

        # Create a graphical window, with some extra space
        self.window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        self.window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)
        self.window = GWindow(width=self.window_width, height=self.window_height, title=title)

        # Create a paddle
        self.paddle_offset = paddle_offset
        self.paddle = GRect(paddle_width, paddle_height)
        self.paddle.filled = True
        self.window.add(self.paddle, x=(self.window_width-paddle_width)/2, y=self.window_height-self.paddle_offset)

        # Center a filled ball in the graphical window
        self.ball = GOval(BALL_RADIUS*2, BALL_RADIUS*2)
        self.ball.filled = True
        self.window.add(self.ball, (self.window_width-BALL_RADIUS)/2, (self.window_height-BALL_RADIUS)/2)

        # Default initial velocity for the ball
        self.__dx = 0
        self.__dy = 0

        # Initialize our mouse listeners
        self.is_first_click = True
        onmouseclicked(self.start)
        onmousemoved(self.reset_position)

        # Draw bricks
        color_index = 0
        for x in range(brick_cols):
            for y in range(brick_rows):
                self.bricks = GRect(brick_width, brick_height)
                self.bricks.filled = True
                color_index = (y // 2) % 5  # Change color every two rows
                if color_index == 0:
                    self.bricks.fill_color = 'red'
                elif color_index == 1:
                    self.bricks.fill_color = 'orange'
                elif color_index == 2:
                    self.bricks.fill_color = 'yellow'
                elif color_index == 3:
                    self.bricks.fill_color = 'green'
                else:
                    self.bricks.fill_color = 'blue'
                self.window.add(self.bricks, x=(brick_width + brick_spacing) * x, y=brick_offset + (brick_height +
                                                                                                    brick_spacing) * y)
        # Initialize the death times and status
        self.death_time = 0
        self.death_or_not = False

        # Create a label to display the remaining number of bricks
        self.brick_num = BRICK_COLS * BRICK_ROWS
        self.label = GLabel(str(self.brick_num), x=0, y=self.window_height)
        self.window.add(self.label)

        # Create a label to display the remaining life of game
        self.challenge_times = GLabel(str(self.death_time))
        self.window.add(self.challenge_times, x=self.window_width-self.challenge_times.width, y=self.window_height)

        # Create the screen of end of the game
        self.end_background = GRect(self.window_width, self.window_height)
        self.end_background.filled = True
        self.end_background.fill_color = 'yellow'
        self.win_text = GLabel('YOU WIN!!')
        self.win_text.font = '-50'
        self.lose_text = GLabel('YOU LOSE!!')
        self.lose_text.font = '-50'

    # Method to update the paddle's position based on the mouse movement.
    def reset_position(self, event):
        if event.x < self.paddle.width/2:
            self.paddle.x = 0
        elif event.x > self.window_width-self.paddle.width/2:
            self.paddle.x = self.window_width - self.paddle.width
        else:
            self.paddle.x = event.x-self.paddle.width / 2
            self.paddle.y = self.window_height - self.paddle_offset

    # Method to start the game and set the velocity of the ball when the mouse is clicked.
    def start(self, event):
        if self.is_first_click is True:
            self.__dy = INITIAL_Y_SPEED
            self.__dx = random.randint(1, MAX_X_SPEED)
            if random.random() > 0.5:
                self.__dx = -self.__dx
            self.is_first_click = False
            return self.is_first_click

    # Method to get the current velocity of the ball in the x-direction for the user.
    def get_dx(self):
        return self.__dx

    # Method to get the current velocity of the ball in the y-direction for the user.
    def get_dy(self):
        return self.__dy

    # Method to display a winning message when the game ends with the player winning.
    def win(self):
        self.window.add(self.end_background)
        self.window.add(self.win_text, x=(self.window.width-self.win_text.width)/2, y=(self.window.height +
                                                                                       self.win_text.height)/2)

    # Method to display a losing message when the game ends with the player losing.
    def lose(self):
        self.window.add(self.end_background)
        self.window.add(self.lose_text, x=(self.window.width-self.lose_text.width)/2, y=(self.window.height +
                                                                                         self.lose_text.height)/2)

    def bounce(self):
        # Reverse the x-direction of the ball's motion when it hits the left or right side of the window
        if self.ball.x < 0 or self.ball.x > self.window_width - self.ball.width:
            self.__dx = -self.__dx

        # Reverse the y-direction of the ball's motion when it hits the top of the window
        if self.ball.y < 0:
            self.__dy = -self.__dy

        # When the player fails to catch the ball and it hits the bottom of the window
        if self.ball.y > self.window_height - self.ball.height:
            self.death_time += 1
            self.challenge_times.text = str(self.death_time)
            self.restart()

        # Detect if the ball hits the paddle, reverse y-direction if true
        maybe_paddle1 = self.window.get_object_at(self.ball.x, self.ball.y+BALL_RADIUS*2+1)
        maybe_paddle2 = self.window.get_object_at(self.ball.x+BALL_RADIUS*2, self.ball.y+BALL_RADIUS*2+1)
        if maybe_paddle1 is not None or maybe_paddle2 is not None:
            if maybe_paddle1 is self.paddle or maybe_paddle2 is self.paddle:
                self.ball.y = self.paddle.y - self.paddle.height
                self.__dy = -self.__dy

        # Detect if the ball hits a brick. If so, reverse the y-direction, remove the brick from the window
        maybe_brick1 = self.window.get_object_at(self.ball.x, self.ball.y)
        maybe_brick2 = self.window.get_object_at(self.ball.x+BALL_RADIUS*2, self.ball.y)
        maybe_brick3 = self.window.get_object_at(self.ball.x, self.ball.y+BALL_RADIUS*2)
        maybe_brick4 = self.window.get_object_at(self.ball.x+BALL_RADIUS*2, self.ball.y+BALL_RADIUS*2)

        if self.ball.y < self.window_height/2:
            if maybe_brick1 is not None:
                self.__dy = -self.__dy
                self.window.remove(maybe_brick1)
                self.brick_num -= 1
                self.label.text = str(self.brick_num)
            elif maybe_brick2 is not None:
                self.__dy = -self.__dy
                self.window.remove(maybe_brick2)
                self.brick_num -= 1
                self.label.text = str(self.brick_num)
            elif maybe_brick3 is not None:
                self.__dy = -self.__dy
                self.window.remove(maybe_brick3)
                self.brick_num -= 1
                self.label.text = str(self.brick_num)
            elif maybe_brick4 is not None:
                self.__dy = -self.__dy
                self.window.remove(maybe_brick4)
                self.brick_num -= 1
                self.label.text = str(self.brick_num)
        return self.brick_num

    # Method to reset the state of the game to its initial state
    def restart(self):
        self.window.add(self.ball, (self.window_width-BALL_RADIUS)/2, (self.window_height-BALL_RADIUS)/2)
        self.__dx = 0
        self.__dy = 0
        self.is_first_click = True
        self.death_or_not = False

