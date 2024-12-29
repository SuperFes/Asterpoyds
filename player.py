import pygame
from circleshape import CircleShape
from constants import PLAYER_RADIUS, PLAYER_TURN_SPEED, PLAYER_SPEED, SHOT_RADIUS, PLAYER_SHOOT_SPEED, \
    PLAYER_SHOOT_COOLDOWN, SCREEN_WIDTH, SCREEN_HEIGHT
from shot import Shot

class Player(CircleShape):
    containers = []

    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shot_timer = 0

        for container in self.containers:
            container.add(self)

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        pygame.draw.polygon(screen, (255, 255, 255), self.triangle(), 2)

    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] and not keys[pygame.K_d]:
            self.rotation -= PLAYER_TURN_SPEED * dt
        elif keys[pygame.K_d] and not keys[pygame.K_a]:
            self.rotation += PLAYER_TURN_SPEED * dt

        if keys[pygame.K_w] and not keys[pygame.K_s]:
            self.move(dt)
        elif keys[pygame.K_s] and not keys[pygame.K_w]:
            self.move(dt, -1)

        if keys[pygame.K_SPACE]:
            self.shoot(dt)

        self.shot_timer -= dt

    def move(self, dt, direction=1):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += (forward * PLAYER_SPEED * dt) * direction

        if self.position.x < -self.radius:
            self.position.x = SCREEN_WIDTH + self.radius
        elif self.position.x > SCREEN_WIDTH + self.radius:
            self.position.x = -self.radius

        if self.position.y < -self.radius:
            self.position.y = SCREEN_HEIGHT + self.radius
        elif self.position.y > SCREEN_HEIGHT + self.radius:
            self.position.y = -self.radius

    def shoot(self, dt):
        if self.shot_timer > 0:
            return

        shot = Shot(self.position.x, self.position.y, SHOT_RADIUS)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
        self.shot_timer = PLAYER_SHOOT_COOLDOWN
