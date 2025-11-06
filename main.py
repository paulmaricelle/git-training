import pygame as py

def Car():
    def __init__(self, x, y):
        self.vx, self.vy = 0, 0
        self.x, self.y = x, y
        self.angle = 0


    def update(self, dt):
        self.x += self.vx*dt
        self.y += self.vy*dt
        #Add realistic phsyics
        self.vx *= 0.98
        self.vy *= 0.98
        #Add Drifting when steering is too sharp
        #Loss of control is discontinous






def initialize():
    car =Car(100, 100)
    #Utilize pygame and create a window
    py.init()
    screen = py.display.set_mode((1200, 1000))
    #Background color
    #While x is not pressed, keep running the loop
    bg_color = (0, 0, 0)
    while True:
        dt = 0.1
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                return
        car.update(dt)
        screen.fill(bg_color)
        #Plot the car according to the angle
        py.draw.polygon(screen, (255, 0, 0), [(car.x + 20 * py.math.cos(py.math.radians(car.angle)), car.y + 20 * py.math.sin(py.math.radians(car.angle))),                                              (car.x - 10 * py.math.cos(py.math.radians(car.angle - 90)), car.y - 10 * py.math.sin(py.math.radians(car.angle - 90))),                                              (car.x - 10 * py.math.cos(py.math.radians(car.angle + 90)), car.y - 10 * py.math.sin(py.math.radians(car.angle + 90)))])

        #Update the display
        py.display.flip()


def position(self):
    return (self.x, self.y)

