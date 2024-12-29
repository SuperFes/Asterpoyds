import pygame

from circleshape import CircleShape
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class Shot(CircleShape):
    containers = []

    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

        for container in self.containers:
            container.add(self)

    def update(self, dt):
        self.position += self.velocity * dt

        if self.position.x < -self.radius:
            self.kill()
        elif self.position.x > SCREEN_WIDTH + self.radius:
            self.kill()
        elif self.position.y < -self.radius:
            self.kill()
        elif self.position.y > SCREEN_HEIGHT + self.radius:
            self.kill()

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), self.position, self.radius, 2)
