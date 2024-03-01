import pygame
import pyguix.ui.elements as ui
import sys

# Configurações da tela
width, height = 1280, 960
screen = pygame.display.set_mode((width, height))

class Item: # representa os itens que podem ser armazenados no inventário
    def __init__(self, name, image_path):
        self.name = name
        self.image_path = image_path

class InventorySlot: # representa um slot individual no inventário.
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.item = None

    def set_item(self, item):
        self.item = item

class Inventory: # representa o inventário como um todo.
    def __init__(self, capacity):
        self.capacity = capacity
        self.slots = []

    def add_slot(self, slot):
        self.slots.append(slot)

    def add_item_to_slot(self, item, slot_index):
        if slot_index < len(self.slots):
            self.slots[slot_index].set_item(item)
            print(f"{item.name} adicionado ao slot {slot_index + 1}")
        else:
            print("Slot inválido")

    # Função para desenhar o inventário na tela
    def draw_inventory(self, inventory):
        # Carrega a imagem do slot
        slot_image = pygame.image.load("./data/images/hud/inventory/empty_slot.png")
        
        # Ajusta as dimensões do retângulo do slot (por exemplo, 80x80 pixels)
        slot_width = 80
        slot_height = 80
        
        # Espaçamento entre os slots
        slot_spacing = 50
        
        # Calcula a largura total dos slots, levando em conta o espaçamento
        total_slots_width = len(inventory.slots) * (slot_width + slot_spacing) - slot_spacing
        
        # Calcula a posição inicial para centralizar os slots horizontalmente
        start_x = (width - total_slots_width) // 2
            
        for i, slot in enumerate(inventory.slots):
            # Ajuste as dimensões da imagem do slot (por exemplo, 60x60 pixels)
            slot_image = pygame.transform.scale(slot_image, (slot_width, slot_height))
            
            # Mostra a imagem do slot
            self.screen.blit(slot_image, (start_x + i * (slot_width + slot_spacing), slot.y))

            if slot.item:
                item_image = pygame.image.load(slot.item.image_path)
                
                # Ajusta o tamanho desejado da imagem do item (por exemplo, 60x60 pixels)
                item_image = pygame.transform.scale(item_image, (60, 60))

                # Calcula as coordenadas para centralizar a imagem do item dentro do slot
                item_x = start_x + i * (slot_width +slot_spacing) + (slot_width - item_image.get_width()) // 2
                item_y = slot.y + (slot_height - item_image.get_height()) // 2

                self.screen.blit(item_image, (item_x, item_y))  # Mostra a imagem do item no slot


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

