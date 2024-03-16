import pygame
from modules.utils import sum_vectors, subtract_vectors, k_vector
from modules.tilemap import Tilemap
class PhysicsEntity:
    def __init__(self, game, e_type, pos, size=()):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.velocity = [0,0]

        self.action = ''
        self.apply_gravity = True
        #esse offset tira o padding que as imagens das animacoes tem como margem
        # pra representar seus movimentos
        self.anim_offset = (-3, -3)
        self.movement_multiplier = 1
        self.velocidade_pulo = -3
        
        #pra caso ele esteja virado pro outro lado
        self.flip = False
        self.set_action('idle')
        self.size = size or self.animation.get_size()

    def set_action(self, action):
        if action != self.action:
            self.action = action
            #criamos uma nova instanccia da animacao a cada vez que precisarmos dela
            #é aqui onde o caminho praas animacoes é definido.
            self.animation = self.game.assets[self.type + "/" + self.action].copy()

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def rect_with_offset(self, offset:tuple):
        return pygame.Rect(sum_vectors(subtract_vectors(self.pos, offset),
                                 self.anim_offset), self.size)

    def update(self, tilemap:Tilemap, movement=(0,0)):
        """moves the player"""
        self.collisions = {'up': False, 'down': False, 'left': False, 'right': False}
        frame_movement = sum_vectors(movement,self.velocity)


        #-------------------------------------------------------#
        # colisao
        self.pos[0] += int(frame_movement[0] * self.movement_multiplier)
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
        if self.apply_gravity:
            self.velocity[1] = min(5, self.velocity[1] + 0.1)

        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0


        self.animation.update()

    def render(self, surface: pygame.Surface, offset, coordinate_system_scale=1):
        """renders the entity in the passed surface"""
        #o coordinate_system_scale permite que se renderize a entidade
        #num espaço de coordenadas onde tudo é maior do que o espaço onde existe a entidade
        surface.blit(pygame.transform.flip(self.animation.img(), self.flip, False),
                     k_vector(coordinate_system_scale,
                        sum_vectors(subtract_vectors(self.pos, offset),
                                    self.anim_offset)))

        # pygame.draw.rect(surface, (0,0,150), pygame.Rect(self.pos[0] -offset[0], self.pos[1] -offset[1], self.size[0], self.size[1]) )
        # surface.blit(self.game.assets['player'], 
        #              subtract_vectors(self.pos, offset))


class AnimatedSimplePhysicsEntity(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'coletavel', pos, size)

        #tempo que passou no ar
        self.air_time = 0

    def update(self, tilemap, movement=(0,3)):
        super().update(tilemap, movement=movement)


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

        
class Itemcoletavel(PhysicsEntity):
    def __init__(self, game, tipo, posicao, tamanho, pontuacao=10):
        if not tamanho:
            tamanho = game.assets[tipo + "/" + "idle"].size
        super().__init__(game, tipo, posicao, tamanho)
        self.pontuacao = pontuacao
        self.coletado = False
        self.is_buff = False
        self.apply_gravity = False

        #pegar o tamanho da imagem, se ele nao for fornecido


    def update(self, tilemap: Tilemap, movement=(0, 0)):
        """Atualiza a animacao e move o item colecionável"""
        super().update(tilemap, movement)

        # Lógica adicional de atualização específica para itens colecionáveis pode ser adicionada aqui

    # def render(self, superficie: pygame.Surface, deslocamento):
    #     """Renderiza o item colecionável"""
    #     pygame.draw.rect(superficie, (0, 0, 0), pygame.Rect(self.pos[0] - deslocamento[0], self.pos[1] - deslocamento[1], self.size[0], self.size[1]))
    #     # Você pode personalizar a renderização do item colecionável conforme necessário


class Buff_velocidade(ItemColecionavel):
    def __init__(self, game, tipo, posicao, tamanho, pontuacao=10):
        super().__init__(game, tipo, posicao, tamanho)
        self.is_buff = True
        
        #se o buff esta sendo aplicado agora
        self.applying = False
        #tempo em frames durante o qual o target sera afetado pelo buff
        self.validity = 7 * 60

    def apply_to_target(self, target:PhysicsEntity):
        """Apenas um exemplo do que um buff faria a um jogador"""
        self.target = target
        self.applying = True
        target.movement_multiplier += 4

    def __remove_buff(self, target:PhysicsEntity):
        """Apenas um exemplo da reversão de um buff"""
        target.movement_multiplier = 1

    def update(self, tilemap: Tilemap, movement=(0,0)):
        """atualiza a animacao e verifica se o buff ainda deve ser aplicado"""
        super().update(tilemap, movement)
        if self.applying:
            self.validity -= 1
            if self.validity < 0:
                self.__remove_buff(self.target)
                return False
        return True
    
class Buff_pulo(ItemColecionavel):
    def __init__(self, game, tipo, posicao, tamanho, pontuacao=10):
        super().__init__(game, tipo, posicao, tamanho)
        self.is_buff = True
        
        #se o buff esta sendo aplicado agora
        self.applying = False
        #tempo em frames durante o qual o target sera afetado pelo buff
        self.validity = 10 * 60

    def apply_to_target(self, target:PhysicsEntity):
        """Apenas um exemplo do que um buff faria a um jogador"""
        self.target = target
        self.applying = True
        target.velocidade_pulo -= 3

    def __remove_buff(self, target:PhysicsEntity):
        """Apenas um exemplo da reversão de um buff"""
        target.velocidade_pulo = -3

    def update(self, tilemap: Tilemap, movement=(0,0)):
        """atualiza a animacao e verifica se o buff ainda deve ser aplicado"""
        super().update(tilemap, movement)
        if self.applying:
            self.validity -= 1
            if self.validity < 0:
                self.__remove_buff(self.target)
                return False
        return True