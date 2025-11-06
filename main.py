import pygame as py
import random
import math


class Car:
    def __init__(self, x, y):
        # physical state
        self.pos = py.math.Vector2(x, y)
        self.vel = py.math.Vector2(0.0, 0.0)     # world-space velocity vector (px/s)
        self.angle = 0.0                         # heading in degrees
        self.angular_velocity = 0.0              # deg/s

        # tuning parameters
        self.length = 30
        self.max_speed = 800.0                   # px/s
        self.max_accel = 600.0                   # px/s^2
        self.brake_accel = 800.0
        self.steer_strength = 180.0              # deg/s^2 at low speed
        self.steer_falloff = 0.008               # how steering effectiveness drops with speed
        self.base_lateral_friction = 0.9         # how quickly sideways velocity is damped
        self.slip_speed = 300.0                  # px/s threshold to start losing traction
        self.slip_steer_threshold = 60.0         # deg/s angular rate threshold for slip
        self.slip_max = 1.0                      # max slip factor
        self.angular_damping = 4.0               # damps angular velocity

    def handle_input(self, keys, dt):
        # acceleration / braking
        accel = 0.0
        if keys[py.K_UP]:
            accel += self.max_accel
        if keys[py.K_DOWN]:
            accel -= self.brake_accel

        # apply forward/backward acceleration along heading
        forward = py.math.Vector2(math.cos(math.radians(self.angle)), math.sin(math.radians(self.angle)))
        self.vel += forward * (accel * dt)

        # steering input
        steer_input = 0.0
        if keys[py.K_LEFT]:
            steer_input += 1.0
        if keys[py.K_RIGHT]:
            steer_input -= 1.0

        # steering effectiveness falls off with speed
        speed = self.vel.length()
        steer_effectiveness = max(0.15, 1.0 - speed * self.steer_falloff)
        # increase angular velocity from steering
        self.angular_velocity += steer_input * self.steer_strength * steer_effectiveness * dt

    def update(self, dt):
        # decompose velocity into forward and lateral components
        forward = py.math.Vector2(math.cos(math.radians(self.angle)), math.sin(math.radians(self.angle)))
        right = forward.rotate(90)
        forward_vel = forward.dot(self.vel)
        lateral_vel = right.dot(self.vel)
        speed = self.vel.length()

        # basic longitudinal friction / drag
        forward_vel *= 0.999

        # baseline lateral damping (grip)
        lateral_vel *= self.base_lateral_friction

        # Loss-of-control / slip mechanic:
        # When at high speed and steering sharply, reduce traction and increase lateral slide,
        # add random yaw perturbations and reduce steering authority.
        slip = 0.0
        if speed > self.slip_speed and abs(self.angular_velocity) > self.slip_steer_threshold:
            # slip factor grows with how much over the threshold we are (clamped)
            slip = min(self.slip_max, (speed - self.slip_speed) / (self.slip_speed))
            # traction reduction: forward acceleration less effective and lateral friction reduced
            forward_vel *= (1.0 - 0.25 * slip)         # lose some forward traction
            lateral_vel *= (1.0 + 0.6 * slip)          # lateral sliding increases
            # random yaw perturbation to mimic sudden loss of control
            self.angular_velocity += random.uniform(-40.0, 40.0) * slip
            # small random lateral kick
            lateral_vel += random.uniform(-40.0, 40.0) * slip

        # rebuild velocity vector from components
        self.vel = forward * forward_vel + right * lateral_vel

        # clamp max speed
        if self.vel.length() > self.max_speed:
            self.vel.scale_to_length(self.max_speed)

        # update position and angle
        self.pos += self.vel * dt
        self.angle += self.angular_velocity * dt

        # angular damping (reduce angular_velocity over time)
        self.angular_velocity *= max(0.0, 1.0 - self.angular_damping * dt)

    def draw(self, surface):
        # simple triangle car oriented by angle
        rad = math.radians(self.angle)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)

        front = self.pos + py.math.Vector2(cos_a, sin_a) * (self.length * 0.8)
        right = py.math.Vector2(cos_a, sin_a).rotate(90)
        rear_right = self.pos - py.math.Vector2(cos_a, sin_a) * (self.length * 0.4) + right * (self.length * 0.33)
        rear_left = self.pos - py.math.Vector2(cos_a, sin_a) * (self.length * 0.4) - right * (self.length * 0.33)

        py.draw.polygon(surface, (255, 0, 0), [(front.x, front.y), (rear_right.x, rear_right.y), (rear_left.x, rear_left.y)])

    def position(self):
        return (self.pos.x, self.pos.y)


def initialize():
    car = Car(100, 100)
    #Utilize pygame and create a window
    py.init()
    screen = py.display.set_mode((1200, 1000))
    clock = py.time.Clock()
    #Background color
    bg_color = (0, 0, 0)
    while True:
        dt = clock.tick(60) / 1000.0
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                return
        keys = py.key.get_pressed()
        car.handle_input(keys, dt)
        car.update(dt)

        screen.fill(bg_color)
        car.draw(screen)

        #Update the display
        py.display.flip()

if __name__ == "__main__":
    initialize()