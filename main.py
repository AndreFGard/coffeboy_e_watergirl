import pygame
import sys
import modules.input
from modules.entities import PhysicsEntity, Player, ItemColecionavel, Buff
from modules.utils import load_image, load_images, Animation, subtract_vectors
from modules.tilemap import Tilemap
def distance(A, B): return (sum(((B[i] - A[i])**2 for i in range(2))))**0.5
from modules.hud import Item, InventorySlot, Inventory, pause_menu

class Game(modules.input.Input):
    def __init__(self):
        modules.input.Input.__init__(self)
        self.width = 1280
        self.height = 960
        self.is_fullscreen = False
    
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
            'moeda/idle': Animation(load_images("coins"), img_dur=4),
            'moeda': load_image("coins/00.png"),
            'Grão de Café': load_image("hud/inventory/coffee_beans/00.png"),
            'Grão de Café/idle':Animation([pygame.transform.scale(load_image("hud/inventory/coffee_beans/00.png"), (17,17))]),
            'Água quente': load_image("hud/inventory/water_cup/00.png"),
            'Água quente/idle':Animation([pygame.transform.scale(load_image("hud/inventory/water_cup/00.png"), (17,17))]),
            
            # O copo de café não é coletável, seria usado no fim da fase para 'transformar' os coletados no copo de café (objetivo)
            'Copo de café': load_image("hud/inventory/coffee_cup/00.png"),
            'Copo de café/idle':Animation([pygame.transform.scale(load_image("hud/inventory/coffee_cup/00.png"), (17,17))]),
            }
        #print(self.assets)
        self.player = Player(self, (50, 50), (8, 15))
        self.tilemap = Tilemap(self, map_filename="data/maps/0.json", tile_size=16)
        self.back = pygame.image.load("data/images/clouds/cloud_1.png")
        item1 = Item(self, 'moeda', (80,50), (8,15))
        item2 = Item(self, 'Grão de Café', (100,50), (8,15))
        item3 = Item(self, 'Grão de Café', (120,50), (8,15))
        item4 = Item(self, 'Água quente', (150, 150), (8,15))
        buff1 = Buff(self, "moeda", (40, 50), (8,15))
        self.itens_colecionaveis = [item1,item2, item3, item4, buff1]
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
        
    

    def main_menu(self):
        # Define as cores utilizadas no menu
        color = (255, 255, 255)  # Cor do texto
        color_light = (170, 170, 170)  # Cor quando o botão é destacado
        color_dark = (100, 100, 100)  # Cor quando o botão não está destacado
        
        # Define a largura e a altura da janela do jogo
        width = 1280
        height = 960
        
        # Define a largura e a altura dos botões
        button_width = 300
        button_height = 100
        
        # Define o espaçamento vertical entre os botões
        button_spacing = 20  
        
        # Define a fonte e o tamanho do texto dos botões
        smallfont = pygame.font.SysFont('Corbel', 50)  
        
        # Lista de botões, contendo texto, posição e tamanho de cada botão
        buttons = [
            {"text": "Start", "position": (width / 2, height / 2 - button_height - button_spacing), 'tamanho': (button_width, button_height)},
            {"text": "Quit", "position": (width / 2, height / 2 + button_spacing), 'tamanho': (button_width, button_height)}
        ]

        # Loop principal do menu
        while True:
            # Preenche a tela com uma cor de fundo
            self.screen.fill((60, 25, 60))
            
            # Obtém a posição do mouse
            mouse = pygame.mouse.get_pos()

            # Itera sobre os botões na lista de botões
            for button in buttons:
                # Renderiza o texto do botão
                text_rendered = smallfont.render(button["text"], True, color)
                # Obtém o retângulo que envolve o texto, com centro na posição do botão
                text_rect = text_rendered.get_rect(center=button["position"])

                # Cria um retângulo para representar o botão
                button_rect = pygame.Rect(button["position"][0] - button["tamanho"][0] / 2, button["position"][1] - button["tamanho"][1] / 2, button["tamanho"][0], button["tamanho"][1])

                # Verifica se o mouse está sobre o botão
                if button_rect.collidepoint(mouse):
                    # Desenha o botão com uma cor mais clara se o mouse estiver sobre ele
                    pygame.draw.rect(self.screen, color_light, button_rect)
                else:
                    # Desenha o botão com a cor padrão
                    pygame.draw.rect(self.screen, color_dark, button_rect)

                # Desenha o texto do botão na tela
                self.screen.blit(text_rendered, text_rect)

            # Loop para lidar com eventos do pygame
            for event in pygame.event.get():
                # Verifica se o evento é o fechamento da janela
                if event.type == pygame.QUIT:
                    # Fecha o jogo
                    pygame.quit()
                    sys.exit()
                # Verifica se houve um clique do mouse
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Itera sobre os botões para verificar qual botão foi clicado
                    for button in buttons:
                        # Cria um retângulo para representar o botão
                        button_rect = pygame.Rect(button["position"][0] - button["tamanho"][0] / 2, button["position"][1] - button["tamanho"][1] / 2, button["tamanho"][0], button["tamanho"][1])
                        # Verifica se o clique do mouse ocorreu dentro do retângulo do botão
                        if button_rect.collidepoint(event.pos):
                            # Verifica se o botão "Quit" foi clicado
                            if button["text"] == "Quit":
                                # Fecha o jogo
                                pygame.quit()
                                sys.exit()
                            # Verifica se o botão "Start" foi clicado
                            elif button["text"] == "Start":
                                # Inicia o jogo
                                #print("Starting the game...")  
                                Game.run(self)

            # Atualiza a tela
            pygame.display.update()



    def run(self):
        clock = pygame.time.Clock()

        # parâmetros gerais do inventário
        slot1 = InventorySlot(100, 800)
        slot2 = InventorySlot(200, 800)
        slot3 = InventorySlot(300, 800)
        inventory = Inventory(3)
        inventory.add_slot(slot1)
        inventory.add_slot(slot2)
        inventory.add_slot(slot3)
    
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
            # TODO: otimizar isso com algo semelhante aos tilemap.physics_rects_around
            for item in self.itens_colecionaveis:
                item.update(self.tilemap)
                item.render(self.display, self.scroll)
            for item in self.itens_colecionaveis:
                #desenhar area de colisao
                pygame.draw.rect(self.display, (255, 100, 0), item.rect_with_offset(self.scroll))

                if not item.coletado and self.player.rect().colliderect(item.rect()):
                    item.coletado = True

                    #tratar os buffs separadamente, pois estes nao podem ser coletados
                    if item.is_buff:
                        self.active_buffs.append(item)
                        item.apply_to_target(self.player)
                    else:    
                        self.inventario.append(item)
                        inventory.add_item_to_slot(item, 0)
                    # Remova o item da lista de itens colecionáveis
                    self.itens_colecionaveis.remove(item)
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
                        
                # Fullscreen e pause
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.toggle_fullscreen()
                    if event.key == pygame.K_ESCAPE:
                        pause_menu(self)
                
                    

            pygame.draw.rect(self.display, (255,0,0), (self.player_x, self.player_y, 10, 16))

            # isto aqui é o que escala o display pra screen (A tela de vdd)
            # e escreve na tela as alteracoes que fizemos, a cada iter
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))
            # Atualiza a tela
            
            #pygame.display.update()
            
            clock.tick(60)
            self.draw_invent(inventory)  # mostra o inventário na tela
            
            
    def draw_invent(self, inventory):
        # Atualizando o inventário
        Inventory.draw_inventory(self, inventory)
        pygame.display.flip()

        









Game().main_menu()
