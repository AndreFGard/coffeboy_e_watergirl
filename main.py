import pygame
import sys
import modules.input
from modules.entities import PhysicsEntity, Player, Itemcoletavel, Buff
from modules.utils import load_image, load_images, Animation, subtract_vectors
from modules.tilemap import Tilemap
def distance(A, B): return (sum(((B[i] - A[i])**2 for i in range(2))))**0.5
from modules.hud import Item, InventorySlot, Inventory, pause_menu

class Game(modules.input.Input):
    def __init__(self):
        modules.input.Input.__init__(self)

        self.is_fullscreen = False
        host_screen_height, host_screen_width = pygame.display.Info().current_h, pygame.display.Info().current_w

        self.width = min(1280, host_screen_width)
        self.height = min(960, host_screen_height)

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
            'tea' : load_images('tiles/tea'),
            'player': load_image("entities/player/idle/00.png"),
            'background': load_image("Background2.png"),
            'player/idle': Animation(load_images('entities/player/idle'), img_dur=6),
            'player/run': Animation(load_images('entities/player/run'), img_dur=4),
            'player/slide': Animation(load_images('entities/player/slide'), img_dur=4),
            'player/jump': Animation(load_images('entities/player/jump'), img_dur=4),
            'player/wall_slide': Animation(load_images('entities/player/wall_slide'), img_dur=4),
            'moeda/idle': Animation(load_images("coins"), img_dur=4),
            'moeda': load_image("coins/00.png"),
            "Grão de Café": load_image("hud/inventory/coffee_beans/00.png"),
            'Grão de Café/idle':Animation([pygame.transform.scale(load_image("hud/inventory/coffee_beans/00.png"), (17,17))]),
            
            }
        #print(self.assets)
        self.player = Player(self, (50, 50), ())
        self.tilemap = Tilemap(self, map_filename="data/maps/0.json", tile_size=16)
        self.back = pygame.image.load("data/images/clouds/cloud_1.png")
        item1 = Item(self, 'moeda', (80,50), tamanho=())
        item2 = Item(self, 'Grão de Café', (100,50), tamanho=())
        item3 = Item(self, 'Grão de Café', (120,50), tamanho=())
        buff1 = Buff(self, "moeda", (40, 50), tamanho=())
        self.itens_coletaveis = [item1,item2, item3, buff1]

        # parâmetros gerais do inventário
        slot1 = InventorySlot(100, 800)
        slot2 = InventorySlot(200, 800)
        slot3 = InventorySlot(300, 800)
        self.inventory = Inventory(3)
        self.inventory.add_slot(slot1)
        self.inventory.add_slot(slot2)
        self.inventory.add_slot(slot3)
        self.inventario = []


        #esse é o offset da camera
        self.scroll = [0,0]
        self.active_buffs = []
        #preparar o background
        self.assets['background'] = pygame.transform.scale(self.assets['background'], self.display.get_size())
        
        
    
    def toggle_fullscreen(self):
        # Alterna entre o modo de tela cheia e o modo de janela
        self.is_fullscreen = not self.is_fullscreen


        if self.is_fullscreen:
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((self.width, self.height))
            
            
    def run(self):
        clock = pygame.time.Clock()


    
        while True:
            #self.display.fill((200,200,255))
            self.display.blit(self.assets['background'], (0,0))


            #dividir por 2 pra que fique no meio
            self.scroll[0] += (self.player.rect().centerx - 320 // 2 - self.scroll[0]) // 10
            self.scroll[1] += (self.player.rect().centery - 240 // 2 - self.scroll[1]) // 10

            #renderizar o mapa
            self.tilemap.render(self.display, offset=self.scroll)

            #atualizar a posicao do player e renderizá-lo
            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            pygame.draw.rect(self.display, (255,100,0), self.player.rect_with_offset(self.scroll))
            self.player.render(self.display, offset=self.scroll) 


            # Renderizar os itens colecionáveis
            # TODO: otimizar isso com algo semelhante aos tilemap.physics_rects_around
            for item in self.itens_coletaveis:
                #desenhar area de colisao
                pygame.draw.rect(self.display, (255, 100, 0), item.rect_with_offset(self.scroll))
                item.update(self.tilemap)
                item.render(self.display, self.scroll)

                if not item.coletado and self.player.rect().colliderect(item.rect()):
                    item.coletado = True

                    #tratar os buffs separadamente, pois estes nao podem ser coletados
                    if item.is_buff:
                        self.active_buffs.append(item)
                        item.apply_to_target(self.player)
                    else:    
                        self.inventario.append(item)
                        self.inventory.add_item_to_slot(item, 0)
                    # Remova o item da lista de itens colecionáveis
                    self.itens_coletaveis.remove(item)
                    break  # Sair do loop assim que um item for coletado
            
            #atualizar os buffs
            for i,buff in enumerate(self.active_buffs):
                #se o buff nao estiver mais ativo, removê-lo
                if not buff.update(self.tilemap):
                    self.active_buffs.pop(i)

            #print(self.tilemap.physics_rects_around(self.player.pos))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # Movimentação do personagem
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    elif event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    elif event.key == pygame.K_UP:
                        self.player.velocity[1] = -3
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    elif event.key == pygame.K_RIGHT:
                        self.movement[1] = False
                        
                # Fullscreen e pause
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.toggle_fullscreen()
                    elif event.key == pygame.K_ESCAPE:
                        pause_menu(self)
                
                    

            #pygame.draw.rect(self.display, (255,0,0), (self.player_x, self.player_y, 10, 32))

            # isto aqui é o que escala o display pra screen (A tela de vdd)
            # e escreve na tela as alteracoes que fizemos, a cada iter
            self.screen.blit(pygame.transform.scale(self.display, (self.width, self.height)), (0,0))
            # Atualiza a tela
                       
            #pygame.display.update()
            
            clock.tick(60)
            self.draw_invent()  # mostra o inventário na tela
            
            


    def draw_invent(self):
        # Atualizando o inventário
        self.inventory.draw_inventory(self)
        pygame.display.flip()

        









Game().run()
