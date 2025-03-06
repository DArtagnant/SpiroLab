'''  
# Automatisation de la génération du spirographe à chaque pression de la touche 'Enter'
    def on_keyboard(e: ft.KeyboardEvent):
        if e.key == 'Enter':
            recompute_spirograph('rien')
        elif e.key == 'M':
            recompute_spirograph(0) # Affiche le spirographe par défaut


    page.on_keyboard_event = on_keyboard
'''