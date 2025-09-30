import math
import random
from typing import List

import pygame

from config import (
    ACCELERATION,
    COIN_SPAWN_DELAY_MS,
    FPS,
    LAYER_DIR,
    LAYER_SCROLL_VELOCITIES,
    MAX_SCROLL_SPEED,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
from coin import Coin
from player import Player


class Layer:
    """Single parallax scrolling layer."""

    def __init__(self, image_path: str, speed_modifier: float):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.speed_modifier = speed_modifier
        self.scroll = 0
        self.bg_width = self.image.get_width()

    def draw(self, surf: pygame.Surface, velocity: float):
        tiles = math.ceil(SCREEN_WIDTH / self.bg_width) + 1
        for i in range(tiles):
            surf.blit(self.image, (self.bg_width * i + self.scroll, 0))
        self.scroll -= velocity * self.speed_modifier
        if abs(self.scroll) >= self.bg_width:
            self.scroll = 0


class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Catto-Run")
        self.font = pygame.font.SysFont("arial", 24)

        # Entities
        self.player = Player()
        self.all_sprites = pygame.sprite.Group(self.player)
        self.coins = pygame.sprite.Group()

        self.layers: List[Layer] = [
            Layer(f"{LAYER_DIR}/L-{i}.png", LAYER_SCROLL_VELOCITIES[i]) for i in range(12)
        ]

        # Gameplay state
        self.scroll_vel = 1.0
        self.score = 0
        self.last_coin_spawn = pygame.time.get_ticks()
        self.running = True

    # ---------------------------- Main Loop ---------------------------- #

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0  # seconds per frame
            self._handle_events()
            self._update(dt)
            self._draw()
        pygame.quit()

    # ---------------------------- Internal ---------------------------- #

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def _update(self, dt: float):
        keys = pygame.key.get_pressed()
        # Speed control
        if keys[pygame.K_RIGHT]:
            self.scroll_vel = min(MAX_SCROLL_SPEED, _lerp(self.scroll_vel, MAX_SCROLL_SPEED, ACCELERATION))
            self.player.set_state("walk")
        else:
            self.scroll_vel = max(0, _lerp(self.scroll_vel, 0, ACCELERATION))
            self.player.set_state("idle")

        # Update sprites
        self.player.update(keys, dt)
        for coin in self.coins.sprites():
            coin.update(self.scroll_vel)
        # Remove off screen handled in coin.update

        # Collision
        collided = pygame.sprite.spritecollide(self.player, self.coins, dokill=True)
        self.score += sum(c.collected() for c in collided)

        # Spawn coins
        current_time = pygame.time.get_ticks()
        if current_time - self.last_coin_spawn > COIN_SPAWN_DELAY_MS + random.randint(0, 1000):
            coin = Coin(Coin.spawn_y())
            self.coins.add(coin)
            self.last_coin_spawn = current_time

    def _draw(self):
        # Background layers
        for layer in self.layers:
            layer.draw(self.display, self.scroll_vel)

        # Sprites
        self.all_sprites.draw(self.display)
        self.coins.draw(self.display)

        # UI
        score_surf = self.font.render(f"Score: {self.score}", True, (0, 0, 0))
        self.display.blit(score_surf, (10, 10))

        pygame.display.update()


# ---------------------------------------------------------------------- #


def _lerp(a: float, b: float, t: float) -> float:
    return a + t * (b - a)


if __name__ == "__main__":
    Game().run()
