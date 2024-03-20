
import pygame
import sys

from modules.entities import PhysicsEntity, Player, Itemcoletavel, Speed_buff, Jump_buff, k_vector, Tea
from modules.utils import load_image, load_images, distance, subtract_vectors, load_assets, get_pos_from_tilemap_pos
from modules.animation import Animation
from modules.tilemap import Tilemap
from modules.hud import Item, InventorySlot, Inventory
from modules.pause_menu import pause_menu

WHITE = (255, 255, 255)
GREY = (170, 170, 170)
DARK_GREY = (100, 100, 100)
DARK_PURPLE =  (60, 25, 60)


class Game():
    def __init__(self):
        self.is_fullscreen = False
        host_screen_height, host_screen_width = pygame.display.Info().current_h, pygame.display.Info().current_w

        self.width = min(1280, host_screen_width)
        self.height = min(960, host_screen_height)
        self.render_scale = self.width // 320

        pygame.init()
        pygame.display.set_caption("coffeeboy e watergirl")

        self.screen = pygame.display.set_mode((self.width, self.height))
        self.display = pygame.Surface((320, 240))

        self.player_x, self.player_y = self.width//2, self.height//2
        self.movement = [False, False]

        # carrega as imagens como uma lista contendo todas as variantes desse tipo        
        self.assets = load_assets()

        self.player = Player(self, (50, 50), ())
        self.tilemap = Tilemap(self, map_filename="data/maps/0.json", tile_size=16)
        self.back = pygame.image.load("data/images/clouds/cloud_1.png")

        # itens no mapa
        moeda = Item(self, 'moeda', (514,17), ())
        cafes = (Item(self, 'grao_de_cafe', (830,85), ()), Item(self, 'grao_de_cafe', (608,-35), ()),)
        agua  = Item(self, 'agua_quente', (1285, 17), ())
        speed_buff = Speed_buff(self, "raio", (140, 50), ())
        jump_buffs = (Jump_buff(self, 'botas', (1100, 16), ()), Jump_buff(self, 'botas', (765, 0), ()), Jump_buff(self, 'botas', (484, 274), ()))
        chas_mortais = [Tea(self, 'tea', (get_pos_from_tilemap_pos(pos)), ()) for pos in self.tilemap.chas_posicoes]

        posicoes_moedas = ((913,40), (1255,-61), (180, 192), (437, 274), (476, 274))
        self.collectible_items = [*[Item(self, 'moeda', pos, ()) for pos in posicoes_moedas], moeda, agua, *chas_mortais, speed_buff, *cafes, *jump_buffs]
        self.victory_req = [moeda, cafes[1], agua]

        # música de fundo
        self.back_music = pygame.mixer.music.load('data/sfx/BackgroundMusic.mp3')
        pygame.mixer.music.play(-1)

        # efeitos sonoros
        self.coffee_sound = pygame.mixer.Sound('data/sfx/coffee_sound.wav')
        self.coin_sound = pygame.mixer.Sound('data/sfx/moeda_sound.wav')
        self.collect_sound = pygame.mixer.Sound('data/sfx/coleta_sound.wav')

        # inventário
        slot1 = InventorySlot(100, 800)
        slot2 = InventorySlot(200, 800)
        slot3 = InventorySlot(300, 800)
        self.inventory = Inventory(3)
        self.inventory.add_slot(slot1)
        self.inventory.add_slot(slot2)
        self.inventory.add_slot(slot3)

        self.inventory_list = []
        self.inventory_types = []

        # Definindo a fonte para o timer
        self.font = pygame.font.Font(None, 34) 
        
        # Offset da camera
        self.scroll = [0,0]

        self.active_buffs = []

        # Preparar o background
        self.assets['background'] = pygame.transform.scale(self.assets['background'], self.display.get_size())

        self.total_time = 53 * 1000
         

    def reviver(self):
        self.player.pos = [50,50]
        # se vc joga mal, eu espero que você tenha bastante memória 
        Game().run()


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

    def main_menu(self):
        # Tamanho dos botões
        button_width = 300
        button_height = 100
        
        # Espaçamento vertical entre os botões
        button_spacing = 20  
        
        # Fontes
        large_font = pygame.font.SysFont('Corbel', 50)  
        minimal_font = pygame.font.SysFont('Corbel', 30)

        buttons = [
            {
                'text': 'Start', 
                'position': (self.width / 2, self.height / 2 - button_height - button_spacing), 
                'tamanho': (button_width, button_height)
            },
            {
                'text': 'Quit',
                'position': (self.width / 2, self.height / 2 + button_spacing), 
                'tamanho': (button_width, button_height)
            }
        ]

        # Loop principal do menu
        while True:
            # Background
            self.screen.fill(DARK_PURPLE)
            
            mouse_position = pygame.mouse.get_pos()

            instructions = [f"Você tem {self.total_time // 1000} segundos pra tomar o seu café a tempo da prova de cálculo", 
                            "Rápido, pegue moedas, café e água quente e vá correndo pra área II!"]
            
            height = 100
            for text in instructions:
                height += 60
                self.screen.blit(minimal_font.render(text,True, WHITE),(self.width//4, height))
            
            for button in buttons:
                text_rendered = large_font.render(button["text"], True, WHITE)
                text_rect = text_rendered.get_rect(center=button["position"])

                # Desenha o texto do botão na tela
                self.screen.blit(text_rendered, text_rect)
                
                button_rect = pygame.Rect(button["position"][0] - button["tamanho"][0]/2, button["position"][1] - button["tamanho"][1]/2, button["tamanho"][0], button["tamanho"][1])

                # Verifica se o mouse está sobre o botão
                if button_rect.collidepoint(mouse_position):
                    pygame.draw.rect(self.screen, GREY, button_rect)
                else:
                    pygame.draw.rect(self.screen, DARK_GREY, button_rect)

                # Desenha o texto do botão na tela
                self.screen.blit(text_rendered, text_rect)

            # Loop para lidar com eventos do pygame
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # Verifica se houve um clique do mouse
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Itera sobre os botões para verificar qual botão foi clicado
                    for button in buttons:
                        button_rect = pygame.Rect(button["position"][0] - button["tamanho"][0]/2, button["position"][1] - button["tamanho"][1]/2, button["tamanho"][0], button["tamanho"][1])
                        # Verifica se o clique do mouse ocorreu dentro do retângulo do botão
                        if button_rect.collidepoint(event.pos):
                            if button["text"] == "Quit":
                                # Fecha o jogo
                                pygame.quit()
                                sys.exit()
                            elif button["text"] == "Start":
                                Game.run(self)

            pygame.display.update()


    def run(self):
        def toggle_fullscreen(self):
            # Alterna entre o modo' de tela cheia e o modo de janela
            self.is_fullscreen = not self.is_fullscreen

            if self.is_fullscreen:
                self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
            else:
                self.screen = pygame.display.set_mode((self.width, self.height))
        def coletou_tudo(self):
            for item_needed in self.victory_req:
                if item_needed not in self.inventory_list:
                    return False
            return True
        
        clock = pygame.time.Clock()
        dialog_message = ""  # balão de diálogo
        start_time = pygame.time.get_ticks()  # Obtendo o tempo de início
        # tempo maximo para ganhar o jogo (colocar a qts em segundos antes da multiplicacao)

        # essas 2 variaveis vao controlar o tempo para o jogo fechar
        contador = 0
        fim = False

        # usada pra pegar a pontuacao somente uma vez
        pontuacao_ = False
        # é usado quando vai contar a pontuacao, para contar a qtd de moedas no inventario
        moedas = 0
        

        while True:
            self.display.blit(self.assets['background'], (0,0))

            #dividir por 2 pra que fique no meio
            self.scroll[0] += (self.player.get_rect().centerx - 320//2 - self.scroll[0])//10
            self.scroll[1] += (self.player.get_rect().centery - 240//2 - self.scroll[1])//10

            #renderizar o mapa
            self.tilemap.render(self.display, offset=self.scroll)

            #atualizar a posicao do player e renderizá-lo
            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            pygame.draw.rect(self.display, (255,100,0), self.player.get_rect_with_offset(self.scroll))

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
            for item in self.collectible_items:
                # desenhar area de colisao
                pygame.draw.rect(self.display, (255, 100, 0), item.get_rect_with_offset(self.scroll))
                item.update(self.tilemap)
                item.render(self.display, self.scroll)

                if not item.coletado and self.player.get_rect().colliderect(item.get_rect()):
                    item.coletado = True

                    # tratar os buffs separadamente, pois estes nao podem ser coletados
  
                    if item.is_buff:
                        self.active_buffs.append(item)
                        item.apply_to_target(self.player)
                        buff_image = self.assets[item.tipo]
                        self.collect_sound.play()
                    else:
                        self.inventory_list.append(item)
                        self.inventory_types.append(item.name)
                        self.inventory.add_item_to_slot(item, 0)

                        # som de coleta
                        if item.name == 'moeda':
                            self.coin_sound.play()
                        elif item.name == 'grao_de_cafe':
                            self.coffee_sound.play()
                        else:
                            self.collect_sound.play()

                            
                    # Remova o item da lista de itens colecionáveis
                    self.collectible_items.remove(item)
                    break  # Sair do loop assim que um item for coletado
            
            if "agua_quente" in self.inventory_types:
                if self.inventory_types.count("grao_de_cafe") >= 2 and self.inventory_types.count("moeda") >= 3:
                    dialog_message = "Ufa, consegui o café a tempo da prova de cálculo"
                    Inventory.delete_inventory(self)
                    self.inventory_list = []
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
                dialog_x = self.player.get_rect_with_offset(self.scroll).right + 30
                # Posição y é ajustada para cima da cabeça do personagem
                dialog_y = self.player.get_rect_with_offset(self.scroll).top - 40
                # Renderiza a mensagem de diálogo na tela sem fundo
                dialog_font = pygame.font.Font('./data/font/MadimiOne-Regular.ttf', 20)  # Defina a fonte e o tamanho da fonte
                dialog_text = dialog_font.render(dialog_message, True, (255, 255, 255))  # Renderiza o texto
                dialog_rect = dialog_text.get_rect(topleft=(dialog_x, dialog_y))  # Obtém o retângulo que envolve o texto

                # isso era pra renderizar o texto de vitoria
                victory_x = self.player.get_rect_with_offset(self.scroll).right - 20
                victory_y = self.player.get_rect_with_offset(self.scroll).top - 80
                victory_font = pygame.font.Font('./data/font/MadimiOne-Regular.ttf', 72)
                victory_text = victory_font.render("Corra para Área II", True, (0, 0, 0))
                victory_rect = victory_text.get_rect(topleft=k_vector(1, (victory_x, victory_y)))
                
                contador += 1
                if pontuacao_ == False:
                    #usar moedas para dar mais pontuacao aqui
                    moedas = sum(1 for item in self.inventory_list if item.name == 'moeda')
                    pontos = remaining_time * 2 + moedas * 50
                    pontuacao_ = True
                # Determinar posição para pontuacao
                pontuacao_x = self.player.get_rect_with_offset(self.scroll).right 
                pontuacao_y = self.player.get_rect_with_offset(self.scroll).top - 60
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
                    lose_x = self.player.get_rect_with_offset(self.scroll).right + 20
                    lose_y = self.player.get_rect_with_offset(self.scroll).top - 50
                    lose_font = pygame.font.Font(None, 72)
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
                        toggle_fullscreen(self)
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


Game().main_menu()
