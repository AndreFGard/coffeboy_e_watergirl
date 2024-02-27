import pygame
import sys
import modules.input
from modules.entities import PhysicsEntity
from modules.utils import load_image
def distance(A, B): return (sum(((B[i] - A[i])**2 for i in range(2))))**0.5

class Game(modules.input.Input):
    def __init__(self):
        modules.input.Input.__init__(self)
        self.width = 640
        self.height = 480
        self.velocity = 5 
        self.jumpcount = 10
        self.isJumping = False
        self.negative = 1 
        pygame.init()
        pygame.display.set_caption("coffeboy e watergirl")

        self.screen = pygame.display.set_mode((self.width, self.height))
        self.las_pressed_pos = tuple()
        self.player_x, self.player_y = self.width // 2, self.height // 2
        self.movement = [False, False]

        #loading everything's sprites
        self.assets = {
            'player': load_image('entities/player/idle/00.png')}

        self.player = PhysicsEntity(self, 'player', (50, 50), (8, 15))



    def run(self):
        clock = pygame.time.Clock()

        while True:
            self.screen.fill((200,200,255))

            self.player.update((self.movement[1] - self.movement[0], 0))
            self.player.render(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False

            pygame.draw.rect(self.screen, (255,0,0), (self.player_x, self.player_y, 10, 16))

            #isto aqui é o que desenha na tela as alterações que fazemos a cada
            # iter do loop
            pygame.display.update()
            clock.tick(60)












Game().run()