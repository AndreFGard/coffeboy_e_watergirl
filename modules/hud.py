import pygame
import pyguix.ui.elements as ui
import sys
from modules.utils import load_image
from modules.entities import Itemcoletavel

# Configurações da tela
width, height = 1280, 960
screen = pygame.display.set_mode((width, height))

ITEM_TAMANHO = 60

class Item(Itemcoletavel): # representa os itens que podem ser armazenados no inventário
    def __init__(self, game, name, posicao, tamanho,):
        super().__init__(game, name, posicao, tamanho)
        self.name = name
        self.type = name
        self.image = game.assets[self.type]

class InventorySlot: # representa um slot individual no inventário.
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.item = None
        self.quantity = 0

    def set_item(self, item:Item):
        # Ajusta o tamanho desejado da imagem do item (por exemplo, 60x60 pixels)
        item.image = pygame.transform.scale(item.image, (ITEM_TAMANHO, ITEM_TAMANHO))

        if self.item and self.item.name == item.name:
            self.quantity += 1  # Se o item já estiver no slot, aumente a quantidade
        else:
            self.item = item
            self.quantity = 1  # Se o item não estiver no slot, defina a quantidade como 1

    def get_item(self):
        return self.item

    def remove_item(self):
        self.x = 0
        self.y = 0
        self.item = None
        self.quantity = 0

class Inventory: # representa o inventário como um todo.
    def __init__(self, capacity):
        self.capacity = capacity
        self.slots = []

        slot_image = load_image("hud/inventory/empty_slot.png")
        slot_width = slot_height = 110
        self.slot_image =  pygame.transform.scale(slot_image, (slot_width, slot_height))

        self.font_37 = font = pygame.font.Font('./data/font/MadimiOne-Regular.ttf', 37)


    def add_slot(self, slot):
        self.slots.append(slot)

    def add_item_to_slot(self, item, slot_index):
        if slot_index < len(self.slots):
            item_at_slot =  self.slots[slot_index].get_item()
            if not item_at_slot:
                self.slots[slot_index].set_item(item)
                print(f"{item.name} adicionado ao slot {slot_index + 1} - Quantidade: {self.slots[slot_index].quantity}")
            else:
                if item_at_slot.name == item.name:
                    #se o slot ocupado com item do mesmo tipo que queremos
                    print("FOUND SLOT")
                    self.slots[slot_index].set_item(item)
                else:
                    print(f"buscando outro slot pra {item.name}")
                    self.add_item_to_slot(item, slot_index + 1)
                
        else:
            print("Slot inválido/sem slots restando")
            
            
    def apagar_inventario(self):
        for item in self.inventory.slots:
            InventorySlot.remove_item(item)

                
    
    # def resize_slots_to(self, slot_width=110, slot_height=110):
    #     self.slots = list(map(pygame.trans))
            
        
    # Função para desenhar o inventário na tela
    def draw_inventory(self, game):
        # Carrega a imagem do slot
        slot_image = self.slot_image
        inventory = self

        # Ajusta as dimensões do retângulo do slot (por exemplo, 80x80 pixels)
        slot_width = 110
        slot_height = 110
        
        # Espaçamento entre os slots
        slot_spacing = 50
        
        # Calcula a largura total dos slots, levando em conta o espaçamento
        total_slots_width = len(inventory.slots) * (slot_width + slot_spacing) - slot_spacing
        
        # Calcula a posição inicial para centralizar os slots horizontalmente
        start_x = (width - total_slots_width) // 2
            
        for i, slot in enumerate(inventory.slots):
            # Ajuste as dimensões da imagem do slot (por exemplo, 60x60 pixels)
            
            # Mostra a imagem do slot
            game.screen.blit(slot_image, (start_x + i * (slot_width + slot_spacing), slot.y))

            if slot.item:
                item_image = slot.item.image


                # Calcula as coordenadas para centralizar a imagem do item dentro do slot
                item_x = start_x + i * (slot_width +slot_spacing) + (slot_width - item_image.get_width()) // 2
                item_y = slot.y + (slot_height - item_image.get_height()) // 2

                game.screen.blit(item_image, (item_x, item_y))  # Mostra a imagem do item no slot
                
                if slot.quantity > 0:
                    font = self.font_37
                    quantity_text = font.render(str(slot.quantity), True, (48, 39, 32))
                    #quantity_text = font.render(str(slot.quantity), True, (0,0,0))
                    quantity_rect = quantity_text.get_rect(center=(item_x + 30, item_y + 82))
                    game.screen.blit(quantity_text, quantity_rect.topleft)

                


def pause_menu(self):
    # Upon pressing KEYDOWN event.type for key 'ESC' create an instance
    # of the pyguix.ui.elements.MessageBox class. (pygame.sprite.Sprite)
    msgbox = ui.MessageBox(
        window=self.screen, # pygame active display window
        message_text="Deseja Sair?", # message text to appear.
        title="Jogo pausado", # title of message box
        buttons=("Sim","Não"), # number of buttons and string values
        width=340, # width 
        height=180 # height
    )

    # NOTE: Call to active MessageBox instance .wait(event_list) function. 
    # Will return True until a button is clicked. Then it will return False.
    # True = (yes).wait(), False (no don't).wait()
    event_list = pygame.event.get()
    while msgbox.wait(event_list):
        # NOTE: Update event_list sent in:
        event_list = pygame.event.get()

    # This will return the button that was clicked from the active MessageBox
    # instance. 
    if msgbox.clicked() == "Sim":
        pygame.quit()
        sys.exit()
    else:
        return