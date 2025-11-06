import pygame as py

def Car():
    def __init__(self, x, y):
        self.vx, self.vy = 0, 0
        self.x, self.y = x, y

    def update(self, dt):
        self.x += self.vx*dt
        self.y += self.vy*dt
    def position(self):
        return (self.x, self.y)

