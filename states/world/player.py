import random

import pygame, os
from states.state import State
import numpy as np


class Player:
    def __init__(self, game):
        self.game = game
        self.__load_sprites__()
        self.position = pygame.math.Vector2(200, 200)
        self.current_frame, self.last_frame_update = 0, 0
        # Stats
        self.health = 100
        self.mana = 100
        self.inventory_slots = 36  # max 36 maybe
        self.speed = 2

        self.inventory = np.full(self.inventory_slots, np._NoValue)

        # only temporary to generate items
        for i in range(random.randrange(0, self.inventory_slots)):  # item count
            # random index of item
            self.inventory[random.randrange(0, self.inventory_slots)] = \
                pygame.image.load(os.path.join(self.game.gui_dir, "broken_sword.png"))

        # Sort inventory
        self.inventory = self.sort(self.inventory)

        self.quickbar_slots = 6
        self.quickbar = [None] * self.quickbar_slots
        self.quickbar[3] = pygame.image.load(os.path.join(self.game.gui_dir, "broken_sword.png"))

    def __load_sprites__(self):
        # Get the diretory with the player sprites
        self.sprite_dir = os.path.join(self.game.sprite_dir, "player")
        self.front_sprites, self.back_sprites, self.right_sprites, self.left_sprites = [], [], [], []
        # Load in the frames for each direction
        for i in range(1, 5):
            self.front_sprites.append(pygame.image.load(os.path.join(self.sprite_dir, "player_front" + str(i) + ".png")))
            self.back_sprites.append(pygame.image.load(os.path.join(self.sprite_dir, "player_back" + str(i) + ".png")))
            self.right_sprites.append(pygame.image.load(os.path.join(self.sprite_dir, "player_right" + str(i) + ".png")))
            self.left_sprites.append(pygame.image.load(os.path.join(self.sprite_dir, "player_left" + str(i) + ".png")))
        # Set the default frames to facing front
        self.current_image = self.front_sprites[0]
        self.curr_anim_list = self.front_sprites

    def sort(self, lst):
        new_lst = []
        for i in lst:
            if i is not None:
                new_lst.append(i)
        for i in range(len(lst) - len(new_lst)):
            new_lst.append(None)
        return new_lst

    def update(self, delta_time, actions):
        if self.game.actions['shift']:
            self.speed = 4
        else:
            self.speed = 2
        # Get the direction from inputs
        direction = pygame.math.Vector2()
        direction.x = actions["right"] - actions["left"]
        direction.y = actions["down"] - actions["up"]
        # Update the position
        if direction.magnitude() != 0:  # normalize the vector
            direction = direction.normalize()
        self.position.x += 100 * delta_time * direction.x * self.speed
        self.position.y += 100 * delta_time * direction.y * self.speed
        # Animate the sprite
        self.animate(delta_time, direction)

    def render(self, display):
        scaled_image = pygame.transform.scale(
            self.current_image,
            (self.current_image.get_width() * self.game.game_resolution[0] / 540,
             self.current_image.get_height() * self.game.game_resolution[1] / 400))
        display.blit(scaled_image, self.position)

    def animate(self, delta_time, direction):
        # Compute how much time has passed since the frame last updated
        self.last_frame_update += delta_time
        # If no direction is pressed, set image to idle and return
        if not direction:
            self.current_image = self.curr_anim_list[0]
            return
        # key was pressed
        if direction.x:
            if direction.x > 0: self.curr_anim_list = self.right_sprites
            else: self.curr_anim_list = self.left_sprites
        if direction.y:
            if direction.y > 0: self.curr_anim_list = self.front_sprites
            else: self.curr_anim_list = self.back_sprites

        # Advance the animation if enough time has elapsed
        if self.last_frame_update > .15:
            self.last_frame_update = 0
            self.current_frame = (self.current_frame + 1) % len(self.curr_anim_list)
            self.current_image = self.curr_anim_list[self.current_frame]
