import pygame
from pygame.constants import K_SPACE, K_UP, K_w

from config import PLAYER_START_X, PLAYER_START_Y, PLAYER_GRAVITY, PLAYER_JUMP_STRENGTH, SPRITE_DIR


class Player(pygame.sprite.Sprite):
    """Main controllable character."""

    def __init__(self):
        super().__init__()

        # Load animations
        self.animations = {
            "walk": [pygame.image.load(f"{SPRITE_DIR}/walk_{i}.png").convert_alpha() for i in range(8)],
            "idle": [pygame.image.load(f"{SPRITE_DIR}/idleUp_{i}.png").convert_alpha() for i in range(8)],
        }
        self.state = "idle"
        self.anim_index: float = 0.0
        self.image = self.animations[self.state][0]
        self.rect = self.image.get_rect(topleft=(PLAYER_START_X, PLAYER_START_Y))

        # Jumping
        self._is_jump = False
        self._jump_count = PLAYER_JUMP_STRENGTH

    # ---------------------------- API ---------------------------- #

    def update(self, keys, dt: float):
        """Update animation frame & vertical movement."""
        self._handle_jump(keys)
        self._update_animation(dt)

    # ---------------------------- Internals ---------------------------- #

    def set_state(self, state: str):
        if state != self.state:
            self.state = state
            self.anim_index = 0

    def _update_animation(self, dt: float):
        frames = self.animations[self.state]
        speed = 10  # frames per second
        self.anim_index += speed * dt
        if self.anim_index >= len(frames):
            self.anim_index = 0
        self.image = frames[int(self.anim_index)]

    def _handle_jump(self, keys):
        # Initiate jump
        if not self._is_jump and (keys[K_SPACE] or keys[K_UP] or keys[K_w]):
            self._is_jump = True

        if self._is_jump:
            if self._jump_count >= -PLAYER_JUMP_STRENGTH:
                neg = 1 if self._jump_count >= 0 else -1
                self.rect.y -= (self._jump_count ** 2) * PLAYER_GRAVITY * neg
                self._jump_count -= 1
            else:
                self._is_jump = False
                self._jump_count = PLAYER_JUMP_STRENGTH
