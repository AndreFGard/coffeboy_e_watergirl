import pygame
import sys
import modules.input
from modules.entities import PhysicsEntity, Player, Itemcoletavel, Buff_velocidade, Buff_pulo, k_vector

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
        self.render_scale = self.width // 320
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
            'grao_de_cafe': load_image("hud/inventory/coffee_beans/00.png"),
            'grao_de_cafe/idle':Animation([pygame.transform.scale(load_image("hud/inventory/coffee_beans/00.png"), (17,17))]),
            'agua_quente': load_image("hud/inventory/water_cup/00.png"),
            'agua_quente/idle':Animation([pygame.transform.scale(load_image("hud/inventory/water_cup/00.png"), (17,17))]),
            'botas': load_image("buffs/boots/00.png"),
            'botas/idle':Animation([pygame.transform.scale(load_image("buffs/boots/00.png"), (17,17))]),
            'raio': load_image("buffs/lightning/00.png"),
            'raio/idle':Animation([pygame.transform.scale(load_image("buffs/lightning/00.png"), (17,17))]),
            
            # O copo_de_cafe não é coletável, seria usado no fim da fase para 'transformar' os coletados no copo_de_cafe (objetivo)
            'copo_de_cafe': load_image("buffs/coffee/00.png"),
            'copo_de_cafe/idle':Animation([pygame.transform.scale(load_image("buffs/coffee/00.png"), (17,17))]),
            }
        #print(self.assets)
        self.player = Player(self, (50, 50), ())
        self.tilemap = Tilemap(self, map_filename="data/maps/0.json", tile_size=16)
        self.back = pygame.image.load("data/images/clouds/cloud_1.png")

        item1 = Item(self, 'moeda', (80,50), ())
        item2 = Item(self, 'grao_de_cafe', (100,50), ())
        item3 = Item(self, 'grao_de_cafe', (120,50), ())
        item4 = Item(self, 'agua_quente', (150, 150), ())
        buff_velocidade = Buff_velocidade(self, "raio", (140, 50), ())
        buff_pulo = Buff_pulo(self, 'botas', (200, 50), ())
        self.itens_coletaveis = [*[Item(self, 'moeda', (80 - 25 * i,80), ()) for i in range(3)], item1,item2, item3, item4, buff_velocidade, buff_pulo]
        self.requisitos_vitoria = [item1, item2, item4]

        # parâmetros gerais do inventário
        slot1 = InventorySlot(100, 800)
        slot2 = InventorySlot(200, 800)
        slot3 = InventorySlot(300, 800)
        self.inventory = Inventory(3)
        self.inventory.add_slot(slot1)
        self.inventory.add_slot(slot2)
        self.inventory.add_slot(slot3)

        self.inventario = []
        self.inventario_tipos = []

        self.font = pygame.font.Font(None, 34)  # Definindo a fonte para o timer
        
        #esse é o offset da camera
        self.scroll = [0,0]
        self.active_buffs = []
        #preparar o background
        self.assets['background'] = pygame.transform.scale(self.assets['background'], self.display.get_size())

        self.total_time = 53 * 1000
        
        
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
        width = self.width
        height = self.height
        
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

        minimalfont = pygame.font.SysFont('Corbel', 30)
        # Loop principal do menu
        while True:
            # Preenche a tela com uma cor de fundo
            self.screen.fill((60, 25, 60))
            
            # Obtém a posição do mouse
            mouse = pygame.mouse.get_pos()

            instrucoes = {f"Você tem {self.total_time // 1000} segundos pra tomar o seu café a tempo da prova de cálculo", "Rápido, pegue moedas, café e água quente e vá correndo pra área II!"}
            
            h = 100
            for surf in tuple(map(lambda txt: minimalfont.render(txt,True, color), instrucoes)):
                h += 60
                self.screen.blit(surf,(self.width//4, h))
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
        dialog_message = ""  # Variável para armazenar a mensagem do balão de diálogo
        start_time = pygame.time.get_ticks()  # Obtendo o tempo de início
        # tempo maximo para ganhar o jogo(colocar a qts em segundos antes da multiplicacao)

        # essas 2 variaveis vao controlar o tempo para o jogo fechar
        contador = 0
        fim = False
        #usada pra pegar a pontuacao somente uma vez
        pontuacao_ = False
        #é usado quando vai contar a pontuacao, para contar a qtd de moedas no inventario
        moedas = 0
        
    
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

            #renderizar o timer
            if pontuacao_ == False:
                elapsed_time = pygame.time.get_ticks() - start_time
                remaining_time = max((self.total_time - elapsed_time) // 1000, 0)
                timer_text = self.font.render(f"Tempo restante: {remaining_time} s", True, (0, 0, 100))
                 
            

            global buff_image
            buff_image = ""
                    
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
                        buff_image = self.assets[item.tipo]
                    else:
                        self.inventario.append(item)
                        self.inventario_tipos.append(item.name)
                        self.inventory.add_item_to_slot(item, 0)

                            
                    # Remova o item da lista de itens colecionáveis
                    self.itens_coletaveis.remove(item)
                    break  # Sair do loop assim que um item for coletado
            
            if "agua_quente" in self.inventario_tipos:
                if "grao_de_cafe" in self.inventario_tipos:
                    if self.inventario_tipos.count("moeda") >= 3:
                        #vencer o jogo 
                        dialog_message = "Ufa, consegui o café a tempo da prova de cálculo"
                    # removendo os itens do inventario e colocando o cafe preparado
            def coletou_tudo(self):
                for item_needed in self.requisitos_vitoria:
                    if item_needed not in self.inventario:
                        return False
                return True

            if coletou_tudo(self) == True:
                Inventory.apagar_inventario(self)
                self.inventario = []
                cafe = Item(self, 'copo_de_cafe', (0,0), ())
                self.inventory.add_item_to_slot(cafe, 0)

             #atualizar os buffs
            for i,buff in enumerate(self.active_buffs):
                #se o buff nao estiver mais ativo, removê-lo
                if not buff.update(self.tilemap):
                    self.active_buffs.pop(i)
            



            #print(self.tilemap.physics_rects_around(self.player.pos))
            lose_text = ""
            if dialog_message:   

                    
                
                self.movement = [False, False] 
                # Posição x é ajustada para a direita da cabeça do personagem
                dialog_x = self.player.rect().right + 30
                # Posição y é ajustada para cima da cabeça do personagem
                dialog_y = self.player.rect().top - 40
                # Renderiza a mensagem de diálogo na tela sem fundo
                dialog_font = pygame.font.Font('./data/font/MadimiOne-Regular.ttf', 20)  # Defina a fonte e o tamanho da fonte
                dialog_text = dialog_font.render(dialog_message, True, (255, 255, 255))  # Renderiza o texto
                dialog_rect = dialog_text.get_rect(topleft=(dialog_x, dialog_y))  # Obtém o retângulo que envolve o texto

                # isso era pra renderizar o texto de vitoria
                victory_x = self.player.rect().right - 20
                victory_y = self.player.rect().top - 80
                victory_font = pygame.font.Font('./data/font/MadimiOne-Regular.ttf', 72)
                victory_text = victory_font.render("Corra para Área II", True, (0, 0, 0))
                victory_rect = victory_text.get_rect(topleft=k_vector(self.render_scale, (victory_x, victory_y)))
                
                
                
                    
                contador += 1
                if pontuacao_ == False:
                    #usar moedas para dar mais pontuacao aqui
                    moedas = sum(1 for item in self.inventario if item.name == 'moeda')
                    pontos = remaining_time * 2 + moedas * 50
                    pontuacao_ = True
                # Determinar posição para pontuacao
                pontuacao_x = self.player.rect().right 
                pontuacao_y = self.player.rect().top - 60
                # Renderizar pontuacao
                pontuacao_font = pygame.font.Font(None, 18)
                pontuacao_text = pontuacao_font.render(f"Pontuaçao: {pontos}", True, (255, 255, 255))
                countdown_rect = pontuacao_text.get_rect(topleft=(pontuacao_x, pontuacao_y))
                
                fim = True
                         
                # contador_x = self.player.rect().right - 30
                # contador_y = self.player.rect().top - 80
                # contador_font = pygame.font.Font(None, 18)
                # contador_text = contador_font.render(f"contador: {contador}", True, (0, 0, 0))
                # contador_rect = contador_text.get_rect(topleft=(contador_x, contador_y))
                # self.display.blit(contador_text, contador_rect.topleft)
                if contador >= 300:
                    pygame.quit()
                    sys.exit()
            # coloquei esse else pq essa mensagem de derrota apareca bem no final antes de fechar o programa quando ganhava
            else:
                if pygame.time.get_ticks() - start_time >= self.total_time:
                    self.movement = [False, False]
                    lose_x = self.player.rect().right + 20
                    lose_y = self.player.rect().top - 50
                    lose_font = pygame.font.Font(None, 20)
                    lose_text = lose_font.render("Você não conseguirá chegar a tempo para a prova de cálculo", True, (0, 0, 0))
                    lose_rect = lose_text.get_rect(topleft=(lose_x, lose_y))
                    
                    contador +=1
                    fim = True
                    if contador >= 200:
                        self.RESTART = True
                        pygame.quit()
                        sys.exit()
    
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # Movimentação do personagem
                elif event.type == pygame.KEYDOWN and fim == False:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    elif event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    elif event.key == pygame.K_UP:
                        self.player.velocity[1] = self.player.velocidade_pulo
                        
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

            ## renderizar os textos diretamente na tela, nao no display
            # pra evitar fontes em baixa resolucao
            if dialog_message:
                self.screen.blit(dialog_text, k_vector(self.render_scale, dialog_rect.topleft))  # Renderiza o texto na tela
                self.screen.blit(victory_text, k_vector(self.render_scale, victory_rect.topleft))
                self.screen.blit(pontuacao_text, k_vector(self.render_scale, countdown_rect.topleft))
            elif pygame.time.get_ticks() - start_time >= self.total_time:
                if lose_text: 
                    self.screen.blit(lose_text, k_vector(self.render_scale, lose_rect.topleft))
            self.screen.blit(timer_text, (40, 120))


            self.draw_invent(buff_image)  # mostra o inventário na tela



    def draw_invent(self, buff_image):
        # Atualizando o inventário
        self.inventory.draw_inventory(self)
        if self.active_buffs:
            for i in self.active_buffs:
                buff_image = self.assets[i.tipo]
                buff_image = pygame.transform.smoothscale(buff_image, (60,60))
                if i == self.active_buffs[0]:
                    self.screen.blit(buff_image, (50, 300))
                else:
                    self.screen.blit(buff_image, (50, 380))
        pygame.display.flip()

    









Game().main_menu()
