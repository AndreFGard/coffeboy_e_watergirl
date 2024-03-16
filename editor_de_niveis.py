import pygame
import sys
import modules.input
from modules.entities import PhysicsEntity, Player
from modules.utils import load_image, load_images, Animation, subtract_vectors, k_vector,sum_vectors
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
        self.render_scale = self.width // 320
        self.player_x, self.player_y = self.width // 2, self.height // 2
        self.movement = [False, False]

        #loads the images as a list of assets containing every variant of that type
        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'tea': load_images('tiles/tea'),
            'player': load_image('entities/player/idle/00.png'),
            'background': load_image("Background2.png"),
            'player/idle': Animation(load_images('entities/player/idle'), img_dur=6),
            'player/run': Animation(load_images('entities/player/run'), img_dur=4),
            'player/slide': Animation(load_images('entities/player/slide'), img_dur=4),
            'player/jump': Animation(load_images('entities/player/jump'), img_dur=4),
            'player/wall_slide': Animation(load_images('entities/player/wall_slide'), img_dur=4)
            }
        #print(self.assets)
        self.player = Player(self, (0, 0), (8, 15))
        self.tilemap = Tilemap(self, map_filename="data/maps/1.json", tile_size=16)
        self.back = pygame.image.load("data/images/clouds/cloud_1.png")
        #esse é o offset da camera
        self.scroll = [0,0]
        self.shift_pressed = False

        #preparar o background
        self.assets['background'] = pygame.transform.scale(self.assets['background'], self.display.get_size())

    def get_mouse_pos(self):
        """retorna a posicao do mouse no sistema local de coordenadas"""
        pos = pygame.mouse.get_pos()
        # passar a posicao de volta pro sistema de coordenadas local
        pos = pos[0]//self.render_scale, pos[1]//self.render_scale
        pos = sum_vectors(pos, self.scroll)
        return pos

    def get_pos_at_tilemap(self, pos):
        """traduz a coordenada local pra coordenada do tilemap"""
        return f"{pos[0] // self.tilemap.tile_size};{pos[1] // self.tilemap.tile_size}"

    def get_tile_at_pos(self, pos):
        #passar a coordenada local pra coordenada tilemap
        coord_translated = self.get_pos_at_tilemap(pos)
        if coord_translated in self.tilemap.tilemap:
            return self.tilemap.tilemap[coord_translated]
        else:
            #print(self.tilemap.tilemap)
            return {}

    def run(self):
        clock = pygame.time.Clock()
        a = False
        selected_tile = {}
        while True:
            #self.display.fill((200,200,255))
            self.display.blit(self.assets['background'], (0,0))


            #dividir por 2 pra que fique no meio
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() // 2 - self.scroll[0]) // 10
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() // 2 - self.scroll[1]) // 10

            self.tilemap.render(self.display, offset=self.scroll)
            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display, offset=self.scroll)

            #print(self.tilemap.physics_rects_around(self.player.pos))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.tilemap.__dump_map__()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_UP:
                        self.player.velocity[1] = -3
                    if event.key == pygame.K_LSHIFT:
                        self.shift_pressed = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
                    if event.key == pygame.K_LSHIFT:
                        self.shift_pressed = False

                #pegar e carregar bloco 
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if selected_tile and self.shift_pressed: 
                        #se o tile ja ta selecionado eo shift ta sendo apertado
                        # adicionar este tipo de tile nesta posicao
                        selected_tile = selected_tile.copy()
                        posicao_tilemap = self.get_pos_at_tilemap(self.get_mouse_pos())
                        print(posicao_tilemap.split(";"))
                        selected_tile['pos'] = list(map(int, posicao_tilemap.split(";")))
                        self.tilemap.tilemap[posicao_tilemap] = selected_tile
                        
                    mouse_pos = self.get_mouse_pos()
                    selected_tile = self.get_tile_at_pos(mouse_pos)
                    if selected_tile:
                        if event.button == 3:
                            #clique direito
                            #remover tile do mapa
                            pos_tilemap = self.get_pos_at_tilemap(mouse_pos)
                            self.tilemap.tilemap.pop(pos_tilemap) 

                        #print(selected_tile)
            
            if selected_tile:
                #se se
                self.display.blit(self.assets[selected_tile['type']][selected_tile['variant']], subtract_vectors(self.get_mouse_pos(), self.scroll))
                #pygame.draw.rect(self.display, (255,0,0), (*subtract_vectors(self.get_mouse_pos(), self.scroll),10, 16))

            pygame.draw.rect(self.display, (255,0,0), (self.player_x, self.player_y, 10, 16))

            # isto aqui é o que escala o display pra screen (A tela de vdd)
            # e escreve na tela as alteracoes que fizemos, a cada iter
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))
            pygame.display.update()
            clock.tick(60)












Game().run()