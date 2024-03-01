import pygame
import pyguix.ui.elements as ui
import sys


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

