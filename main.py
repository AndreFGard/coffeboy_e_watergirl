import pygame
import sys
import modules.input
from modules.entities import PhysicsEntity
def distance(A, B): return (sum(((B[i] - A[i])**2 for i in range(2))))**0.5

class Game(modules.input.Input):
    def __init__(self):
        modules.input.Input.__init__(self)
        self.width = 1280
        self.height = 720
        self.velocity = 5 
        self.jumpcount = 10
        self.isJumping = False
        self.negative = 1 

        self.assets ={'player': 'data/images/entities/player/idle/00.png'}

    
        pygame.init()
        pygame.display.set_caption("coffeboy e watergirl")

        self.screen = pygame.display.set_mode((self.width, self.height))
        self.las_pressed_pos = tuple()
        self.player_x, self.player_y = self.width // 2, self.height // 2
    
        #carregar a imagem numa surface
        self.img = pygame.image.load('data/images/clouds/cloud_1.png')
        #set_colorkey diz que cor da imagem é o seu background, o qual deve ser transparente
        self.img.set_colorkey((0,0,0))
        self.img_pos = [160, 260]
        self.collision_area = pygame.Rect(50,50,300,50)


        self.movement = [False, False]

        #ignorar isto
        self.player = PhysicsEntity(self, 'player', (50, 50), (8, 15))

    def run(self):

        #display = pygame.Surface((700, 700)) ???
        clock = pygame.time.Clock()

   
        while True:
            self.screen.fill((200,200,255))


            #rect criado a partir imagem
            img_r = pygame.Rect(*self.img_pos, *self.img.get_size())
            if img_r.colliderect(self.collision_area):
                pygame.draw.rect(self.screen, (0, 100, 255), self.collision_area)
            else:
                pygame.draw.rect(self.screen, (100, 100, 255), self.collision_area)

            # a blit desenha uma imagem sobre uma outra. No caso, sobre a imagem que
            # renderizamos como janela do jogo
            self.img_pos[1] += self.movement[1] - self.movement[0]
            self.screen.blit(self.img, self.img_pos)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quitt()
                    sys.exit()

                elif event.type == pygame.MOUSEMOTION:
                    mouse_pos = pygame.mouse.get_pos()
                    if not self.las_pressed_pos: self.las_pressed_pos = mouse_pos
                    if distance(self.las_pressed_pos, mouse_pos) > 100:
                        pygame.draw.circle(self.screen, (240, 0, 0),mouse_pos, 20, 5)
                        self.las_pressed_pos = mouse_pos

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.movement[0] = True
                    if event.key == pygame.K_DOWN:
                        self.movement[1] = True

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        self.movement[0] = False
                    if event.key == pygame.K_DOWN:
                        self.movement[1] = False          

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.player_x -= self.velocity
            if keys[pygame.K_DOWN]:
                self.player_y += self.velocity            
        
            if keys[pygame.K_SPACE]:
                self.isJumping = True

            if self.isJumping:
                if self.jumpcount >= -10:
                    if self.jumpcount < 0:
                        self.negative = -1
                    self.player_y -= (self.jumpcount ** 2 ) * self.negative
                    self.jumpcount -= 1 
                else:
                    self.isJumping = False
                    self.jumpcount = 10
                    self.negative = 1


            pygame.draw.rect(self.screen, (255,0,0), (self.player_x, self.player_y, 10, 16))

            #isto aqui é o que desenha na tela as alterações que fazemos a cada
            # iter do loop
            pygame.display.update()
            clock.tick(60)












Game().run()