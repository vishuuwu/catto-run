import pygame
import random
from config import COIN_DIR, SCREEN_WIDTH, COIN_SCORE_VALUE


class Coin(pygame.sprite.Sprite):
    def __init__(self, y: int):
        super().__init__()
        self.image = pygame.image.load(f"{COIN_DIR}/gold_0.png").convert_alpha()
        self.rect = self.image.get_rect(midleft=(SCREEN_WIDTH + 10, y))
        self.speed = 0

    def update(self, vel: float):
        self.rect.x -= vel
        if self.rect.right < 0:
            self.kill()

    @staticmethod
    def spawn_y():
        return random.choice([552, 652])

    @classmethod
    def spawn(cls):
        return cls(cls.spawn_y())

    @classmethod
    def spawn_group(cls, amount: int):
        return [cls(cls.spawn_y()) for _ in range(amount)]

    def collected(self):
        self.kill()
        return COIN_SCORE_VALUE
