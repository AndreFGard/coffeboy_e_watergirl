import pygame
from modules.utils import sum_vectors


class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0,0]

    def update(self, movement=(0,0)):
        """moves the player"""
        frame_movement = sum_vectors(movement,self.velocity)
        self.pos[0] += frame_movement[0]
        self.pos[1] += frame_movement[1]

    def render(self, surface: pygame.Surface):
        """renders the entity in the passed surface"""
        surface.blit(self.game.assets['player'], self.pos)

