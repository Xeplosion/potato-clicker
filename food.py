# Foster Cavender
# CS1400 online 7 week
import math
from random import randint


class Potato:
    def __init__(self, screen, type, image):
        # screen values
        self.screen = screen
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()

        # set the draw values
        self.image = image
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.radius = self.width / 2 - 1
        self.center_x = self.screen_width // 2
        self.center_y = self.screen_height // 2
        self.draw_x = self.center_x - self.width / 2
        self.draw_y = self.center_y - self.height / 2

        self.poisonous = type

        # move values
        self.speed = randint(1, 15)
        self.dir = randint(0, 360)
        self.move = [self.speed, self.dir, self.dir * (math.pi / 180)]

    def draw(self):
        # set the draw pos based off player asset dimensions
        self.draw_x = int(self.center_x - self.width / 2)
        self.draw_y = int(self.center_y - self.height / 2)

        # draw the sprite to the screen
        self.screen.blit(self.image, (self.draw_x, self.draw_y))


    def check_bounce(self):
        # check if in the screen bounds
        # if outside then we return True with a bounce value in degrees
        if self.draw_x < 0:
            return [True, 0]
        if self.draw_y < 0:
            return [True, 180]
        if self.draw_x > self.screen_width - self.width:
            return [True, 0]
        if self.draw_y > self.screen_height - self.height:
            return [True, 180]
        else:
            return [False, 0]

    def move_potato(self):
        # move enemy, then bounce if offscreen
        self.center_x += math.sin(self.move[2]) * self.move[0]
        self.center_y += math.cos(self.move[2]) * self.move[0]
        bounce = False

        # handle bounces
        if self.check_bounce()[0]:
            self.center_x -= math.sin(self.move[2]) * self.move[0]
            self.center_y -= math.cos(self.move[2]) * self.move[0]
            self.move[1] += self.check_bounce()[1] - self.move[1] * 2
            self.move[2] = self.move[1] * (math.pi / 180)
            self.center_x += math.sin(self.move[2]) * self.move[0]
            self.center_y += math.cos(self.move[2]) * self.move[0]

    def did_get(self, location):
        # check for collisions
        # adjusting for increased mouse icon size, + 32 (not a specific point but makes sense for my game)
        if abs(location[0] - self.center_x) < self.radius + 32:
            if abs(location[1] - self.center_y) < self.radius + 32:
                return True

        return False
