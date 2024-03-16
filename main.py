import pygame
import sys
import modules.input
from modules.entities import PhysicsEntity, Player, ItemColecionavel
from modules.utils import load_image, load_images, Animation, subtract_vectors
from modules.tilemap import Tilemap
def distance(A, B): return (sum(((B[i] - A[i])**2 for i in range(2))))**0.5

class Game(modules.input.Input):
    def __init__(self):
        modules.input.Input.__init__(self)
        self.width = 1280
        self.height = 960

        pygame.init()
        pygame.display.set_caption("coffeboy e watergirl")

        self.screen = pygame.display.set_mode((self.width, self.height))
        #gera uma imagem. Pra aumentar o tamanho das coisas na tela,
        #renderizamos nela e depois escalamos pra screen 
        #é no display que gravaremos as coisas
        self.display = pygame.Surface((320, 240))

        self.player_x, self.player_y = self.width // 2, self.height // 2
        self.movement = [False, False]

        #loads the images as a list of assets containing every variant of that type
        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'player': load_image('entities/player/idle/00.png'),
            'background': load_image("Background2.png"),
            'player/idle': Animation(load_images('entities/player/idle'), img_dur=6),
            'player/run': Animation(load_images('entities/player/run'), img_dur=4),
            'player/slide': Animation(load_images('entities/player/slide'), img_dur=4),
            'player/jump': Animation(load_images('entities/player/jump'), img_dur=4),
            'player/wall_slide': Animation(load_images('entities/player/wall_slide'), img_dur=4),
            'colecionavel/idle': load_image('entities/player/idle/00.png'),

            }
        #print(self.assets)
        self.player = Player(self, (50, 50), (8, 15))
        self.tilemap = Tilemap(self, map_filename="data/maps/0.json", tile_size=16)
        self.back = pygame.image.load("data/images/clouds/cloud_1.png")
        item1 = ItemColecionavel(self, 'colecionavel', (80,50), (8,15))
        item2 = ItemColecionavel(self, 'colecionavel', (100,50), (8,15))
        self.itens_colecionaveis = [item1,item2]
        self.inventario = []

        #esse é o offset da camera
        self.scroll = [0,0]

        self.font = pygame.font.SysFont(None, 10)  # Definindo a fonte para o timer

        self.tela_inicio()

        #preparar o background
        self.assets['background'] = pygame.transform.scale(self.assets['background'], self.display.get_size())\
        

    def tela_inicio(self):
        font_title = pygame.font.Font(None, 64)
        font_button = pygame.font.Font(None, 32)

        # Nome do jogo
        game_title = font_title.render("Coffeboy e Watergirl", True, (255, 255, 255))
        title_rect = game_title.get_rect(center=(self.width//2, self.height//4))

        # Botão Iniciar
        start_button_text = font_button.render("Iniciar", True, (90, 65, 112))
        start_button_rect = start_button_text.get_rect(center=(self.width//2, self.height//2))

        # Botão Sair
        quit_button_text = font_button.render("Sair", True, (90, 65, 112))
        quit_button_rect = quit_button_text.get_rect(center=(self.width//2, self.height * 3//4))

        while True:
            self.screen.fill((0, 0, 0))  # Preencha a tela com preto

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button_rect.collidepoint(event.pos):
                        self.run()  # Inicie o jogo
                    elif quit_button_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

            # Desenha o nome do jogo
            self.screen.blit(game_title, title_rect)

            # Desenha os botões
            pygame.draw.rect(self.screen, (0, 0, 0, 0), start_button_rect, border_radius=10)
            pygame.draw.rect(self.screen, (0, 0, 0, 0), quit_button_rect, border_radius=10)
            self.screen.blit(start_button_text, start_button_rect)
            self.screen.blit(quit_button_text, quit_button_rect)

            pygame.display.flip()
    def run(self):
        clock = pygame.time.Clock()

        start_time = pygame.time.get_ticks()  # Obtendo o tempo de início

        while True:
            #self.display.fill((200,200,255))
            self.display.blit(self.assets['background'], (0,0))


            #dividir por 2 pra que fique no meio
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() // 2 - self.scroll[0]) // 10
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() // 2 - self.scroll[1]) // 10

            self.tilemap.render(self.display, offset=self.scroll)
            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display, offset=self.scroll)
            # Renderizar os itens colecionáveis
            for item in self.itens_colecionaveis:
                if not item.coletado:
                    item.render(self.display, self.scroll)
            for item in self.itens_colecionaveis:
                if not item.coletado and self.player.rect().colliderect(item.rect()):
                    self.inventario.append(item)
                    item.coletado = True
                    # Remova o item da lista de itens colecionáveis
                    self.itens_colecionaveis.remove(item)
                    break  # Sair do loop assim que um item for coletado
            


            #print(self.tilemap.physics_rects_around(self.player.pos))
            elapsed_time = pygame.time.get_ticks() - start_time  # Calculando o tempo decorrido
            timer_text = self.font.render(f"Tempo: {elapsed_time // 1000} s", True, (0,0,0))
            self.display.blit(timer_text, (10, 18))  # Renderizando o texto do timer no canto superior esquerdo

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_UP:
                        self.player.velocity[1] = -3
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
                
                    

            pygame.draw.rect(self.display, (255,0,0), (self.player_x, self.player_y, 10, 16))

            # isto aqui é o que escala o display pra screen (A tela de vdd)
            # e escreve na tela as alteracoes que fizemos, a cada iter
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))
            pygame.display.update()
            clock.tick(60)












Game().run()