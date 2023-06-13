"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao.

This program is a classic brick breaker game "Breakout". A ball moves around the window, bouncing off the paddle and
the bricks. The player loses a life if the ball hits the bottom of the window. The objective of the game is to
break all the bricks without running out of lives.
"""

from campy.gui.events.timer import pause
from breakoutgraphics import BreakoutGraphics
from campy.graphics.gobjects import GLabel

FRAME_RATE = 10         # 100 frames per second
NUM_LIVES = 3			# Number of attempts


def main():
    graphics = BreakoutGraphics()
    x_speed = 0
    y_speed = 0

    # Add the animation loop here!
    while True:
        x_speed = graphics.get_dx()
        y_speed = graphics.get_dy()
        brick_num = graphics.brick_num
        lives = NUM_LIVES - graphics.death_time
        death_condition = graphics.death_or_not
        graphics.ball.move(x_speed, y_speed)
        graphics.bounce()

        if death_condition:
            graphics.restart()
        if brick_num == 0:
            graphics.win()
            break
        if lives == 0:
            graphics.lose()
            break
        pause(FRAME_RATE)


if __name__ == '__main__':
    main()
