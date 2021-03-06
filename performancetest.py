"""
A rocket animation performance test

Copyright by Irmen de Jong (irmen@razorvine.net).
Open source software license: MIT.
"""
from __future__ import print_function, division
import random
import time
from vectors import Vector2D
from tkanimation import AnimationWindow, tkinter
from rocketsimulator import Rocket


class PerformanceTestWindow(AnimationWindow):
    def setup(self):
        self.cwidth, self.cheight = int(self.canvas["width"]), int(self.canvas["height"])
        self.set_frame_rate(60)
        self.rockets = []
        self.framecounter = 0
        self.start_time = time.time()
        for _ in range(10):
            self.add_rocket()

    def draw(self):
        self.update()
        self.canvas.delete(tkinter.ALL)
        for rocket in self.rockets:
            rocket.draw(self.canvas)
        # framecounter
        if time.time()-self.start_time:
            fps = round(self.framecounter / (time.time() - self.start_time))
        else:
            fps = 0
        self.canvas.create_text(self.cwidth, 0, text="#ROCKETS: {0:d}  FPS: {1:d} ".format(len(self.rockets), fps), fill="yellow", anchor=tkinter.NE)
        self.canvas.create_text(self.cwidth, 30, text="press SPACE to add 10 more ", fill="yellow", anchor=tkinter.NE)

    def add_rocket(self):
        rocket = Rocket(self.cwidth, self.cheight)
        rocket.rotation_speed = random.uniform(-.3,.3)
        rocket.engine_throttle = 1
        rocket.position = Vector2D((random.randint(-self.cwidth/2,self.cwidth/2), random.randint(0,self.cheight)))
        rocket.velocity = Vector2D((random.uniform(-10,10), random.uniform(-4,4)))
        self.rockets.append(rocket)

    def keypress(self, char, mouseposition):
        if char == ' ':
            for _ in range(10):
                self.add_rocket()
            self.start_time = time.time()
            self.framecounter = 0

    def update(self):
        self.framecounter += 1
        for rocket in self.rockets:
            rocket.update()
            if not(-self.cwidth/2 < rocket.position.x < self.cwidth/2):
                rocket.velocity.flipx()
            if not(0<rocket.position.y<self.cheight):
                rocket.velocity.flipy()


if __name__ == "__main__":
    window = PerformanceTestWindow(1000, 600, "Rocket animation performance test")
    window.mainloop()
