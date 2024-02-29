import pygame
from modules.utils import sum_vectors, k_vector
from modules.tilemap import Tilemap

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0,0]

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def update(self, tilemap:Tilemap, movement=(0,0)):
        """moves the player"""
        self.collisions = {'up': False, 'down': False, 'left': False, 'right': False}
        frame_movement = sum_vectors(movement,self.velocity)


        #-------------------------------------------------------#
        # colisao
        self.pos[0] += frame_movement[0]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    #a entidade se mexe pra direita
                    #entao vamos fazer com que a borda direita dela seja empurrada
                    #pra borda esquerda do rect com que colidiu
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                
                self.pos[0] = entity_rect.x

        self.pos[1] += frame_movement[1]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):

                if frame_movement[1] > 0:
                    self.collisions['up'] = True
                    entity_rect.bottom = rect.top
                if frame_movement[1] < 0:
                    self.collisions['down'] = True
                    entity_rect.top = rect.bottom
                
                self.pos[1] = entity_rect.y

        #isso lida com a gravidade
        self.velocity[1] = min(5, self.velocity[1] + 0.1)

        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0

    def render(self, surface: pygame.Surface, offset):
        """renders the entity in the passed surface"""
        pygame.draw.rect(surface, (0,0,100), pygame.Rect(self.pos[0] -offset[0], self.pos[1] -offset[1], self.size[0], self.size[1]) )
        surface.blit(self.game.assets['player'], 
                     sum_vectors(k_vector(-1, offset), self.pos))
        
class ItemColecionavel(PhysicsEntity):
    def __init__(self, game, tipo, posicao, tamanho, pontuacao=10):
        super().__init__(game, tipo, posicao, tamanho)
        self.pontuacao = pontuacao
        self.coletado = False

    def update(self, tilemap: Tilemap, movement=(0, 0)):
        """Move o item colecionável"""
        super().update(tilemap, movement)

        # Lógica adicional de atualização específica para itens colecionáveis pode ser adicionada aqui

    def render(self, superficie: pygame.Surface, deslocamento):
        """Renderiza o item colecionável"""
        pygame.draw.rect(superficie, (0, 0, 0), pygame.Rect(self.pos[0] - deslocamento[0], self.pos[1] - deslocamento[1], self.size[0], self.size[1]))
        # Você pode personalizar a renderização do item colecionável conforme necessário