from clases.game import Game

def main():
    # Creación de una instancia del juego con dimensiones y parámetros específicos
    game = Game(300, 600, 10, 20)  # (ANCHO_VENTANA_BASE, ALTO_VENTANA_BASE, CANTIDAD_ANCHO_CAJAS_REJILLA, cANTIDAD_ALTO_CAJAS_REJILLA)
    
    # Inicio del ciclo principal del juego
    game.run()
    
    while True:
        # Inicio de un nuevo juego
        game.start_game()
        # Fin del juego
        game.game_over()

if __name__ == "__main__":
    # Llamada a la función principal si el script se ejecuta directamente
    main()
