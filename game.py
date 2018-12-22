from collections import namedtuple
from time import sleep
from random import randint
import random
import pyxel

def clip(x, lower, upper):
    if(x>upper):
        return upper
    elif(x<lower):
        return lower
    else:
        return x
def sign(x):
    if(x==0):
        return 0
    if(x>0):
        return 1
    if(x<0):
        return -1

BMP_COOKIE = 1
BMP_HAT = 0

class Point:
    def __init__(self, x, y, wrap=False, width=None, height=None):
        self.x = x
        self.y = y
        self.wrap = wrap
        if(wrap):
            self.wrap = wrap
            self.width = width
            self.height = height
    def add(self, a, b):
        if(self.wrap):
            self.x = (self.x + a)%self.width
            self.y = (self.y + b)%self.height
        else:
            self.x += a
            self.y += b

    def tup(self):
        return (self.x, self.y)
    def x(self):
        return self.x
    def y(self):
        return self.y
class Game:
    def reset(self):
        self.gravity = 3
        self.spawn_prob = 0.02
        self.cookies = []
        self.time = 0
        self.score = 0
        self.hat = Point(100, self.HEIGHT-20)
        self.sound_speed = 30
        self.acceleration = 0
        self.speed = 0
        self.friction = -0.4

    def __init__(self):
        self.WIDTH = 200
        self.HEIGHT = 200
        self.reset()
        pyxel.init(self.WIDTH, self.HEIGHT, caption='MyGame', scale = 10)
        pyxel.sound(0).speed = int(self.sound_speed)
        pyxel.load('./res.pyxel')
        pyxel.play(0, 0, loop=True)
        pyxel.run(self.update, self.draw)

    def update(self):
        self.time += 1
        self.move_hat()
        print('Time:'+str(self.time))
        pyxel.sound(0).speed  = int(self.sound_speed)

        #handle keystrokes  
        self.handle_keys()

        #Spawn cookies with probability=spawn_prob 
        if random.uniform(0,1)<=self.spawn_prob:
            self.spawn_cookie()
        self.spawn_prob *= 1.02

        #Let each cookie fall and check if its caught by the hat
        new_cookies = []
        for c in self.cookies:
            c.add(0, self.gravity)
            if(self.caught(c)):
                self.score += 1
                self.sound_speed *=  0.97
                pyxel.play(1, 2, loop=False)
                continue
            if(c.y < self.HEIGHT):
                new_cookies.append(c)
            else:
                print('Game Over')
                pyxel.play(0, 1, loop=False)
                sleep(3)
                exit()
        self.cookies = new_cookies

    def draw(self):
        pyxel.cls(col=0)
        
        #Draw each cookie
        for c in self.cookies:
            pyxel.blt(c.x, c.y, BMP_COOKIE, 4, 4, 8, 8, 0)
            pyxel.pix(c.x, c.y, 11)

        #Draw number of cookies
        txt = "Score: " + str(self.score)
        pyxel.text(1, 1, txt, 3)

        #Draw santas hat
        pyxel.blt(self.hat.x, self.hat.y, BMP_HAT, 0, 7, 14, 11, 0)
        pyxel.pix(self.hat.x, self.hat.y, 11)
    def move_hat(self):
        MAX_SPEED = 5
        MIN_SPEED = -5
        FRICTION = self.friction
        self.speed += self.acceleration
        self.speed += FRICTION*sign(self.speed)
        self.speed = clip(self.speed, MIN_SPEED, MAX_SPEED)
        self.hat.x += int(self.speed)

    def caught(self, cookie):
        hat_w = 13
        cookie_w = 8
        hat = self.hat
        if cookie.x in range(hat.x - hat_w + cookie_w, hat.x + hat_w) and cookie.y in range(hat.y - 3, hat.y + 3):
            print("DING")
            return True
        return False
        
    def spawn_cookie(self):
        print('Spawning cookie')
        x = randint(0, self.WIDTH)
        p = Point(x, 0)
        self.cookies.append(p)
        self.spawn_prob*= 0.1

    def hat_speed(self):
        speed = self.speed + self.acceleration
        max_speed = 5
        min_speed = -5
        return clip(speed, min_speed, max_speed)

    def handle_keys(self):
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.acceleration = 1
        elif pyxel.btn(pyxel.KEY_LEFT):
            self.acceleration = -1
        else:
            self.acceleration = 0

Game()
