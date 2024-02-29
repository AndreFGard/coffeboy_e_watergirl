import pygame
from modules.utils import sum_vectors, subtract_vectors
from modules.tilemap import Tilemap

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0,0]

        self.action = ''

        #esse offset tira o padding que as imagens das animacoes tem como margem
        # pra representar seus movimentos
        self.anim_offset = (-3, -3)
        
        #pra caso ele esteja virado pro outro lado
        self.flip = False
        self.set_action('idle')


    def set_action(self, action):
        if action != self.action:
            self.action = action
            #criamos uma nova instanccia da animacao a cada vez que precisarmos dela
            #é aqui onde o caminho praas animacoes é definido.
            self.animation = self.game.assets[self.type + "/" + self.action].copy()

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
                    self.collisions['down'] = True
                    entity_rect.bottom = rect.top
                if frame_movement[1] < 0:
                    self.collisions['up'] = True
                    entity_rect.top = rect.bottom
                
                self.pos[1] = entity_rect.y


        if movement[0] >= 0:
            self.flip = False
        else:
            #fazer a imagem/animacao olhar pra esquerda
            self.flip = True

        #isso lida com a gravidade
        self.velocity[1] = min(5, self.velocity[1] + 0.1)

        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0


        self.animation.update()

    def render(self, surface: pygame.Surface, offset):
        """renders the entity in the passed surface"""
        surface.blit(pygame.transform.flip(self.animation.img(), self.flip, False),
                     sum_vectors(subtract_vectors(self.pos, offset),
                                 self.anim_offset))

        # pygame.draw.rect(surface, (0,0,150), pygame.Rect(self.pos[0] -offset[0], self.pos[1] -offset[1], self.size[0], self.size[1]) )
        # surface.blit(self.game.assets['player'], 
        #              subtract_vectors(self.pos, offset))

class Player(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'player', pos, size)

        #tempo que passou no ar
        self.air_time = 0

    def update(self, tilemap, movement=(0,0)):
        super().update(tilemap, movement=movement)

        self.air_time += 1
        if self.collisions['down']:
            self.air_time = 0

        if self.air_time > 4:
            self.set_action('jump')
        elif movement[0] != 0:
            self.set_action('run')
        else:
            self.set_action('idle')