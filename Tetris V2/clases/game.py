import pygame
import sys
import random
from clases.shape import Shape  # Importa la clase Shape desde el módulo shape
from clases.board import Board  # Importa la clase Board desde el módulo board
from constants import BLACK, WHITE  # Importa las constantes BLACK y WHITE

class Game:

    def __init__(self, WIDTH_BASE, HEIGHT_BASE, GRID_WIDTH, GRID_HEIGHT):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("Tetris")
        # Inicialización de variables y configuración de la ventana pygame
        self.GRID_WIDTH, self.GRID_HEIGHT = GRID_WIDTH, GRID_HEIGHT 
        self.GRID_SIZE = HEIGHT_BASE // GRID_HEIGHT if HEIGHT_BASE // GRID_HEIGHT < WIDTH_BASE // GRID_WIDTH else WIDTH_BASE // GRID_WIDTH
        self.WIDTH, self.HEIGHT = self.GRID_SIZE*GRID_WIDTH+1, self.GRID_SIZE * GRID_HEIGHT
        self.screen = pygame.display.set_mode((self.WIDTH + 250, self.HEIGHT))
        self.FONT = pygame.font.Font(None, 36)

    def draw_text_centered(self, text, y_offset, color):
        # Función para dibujar texto centrado en la pantalla
        text_surface = self.FONT.render(text, True, color)
        text_rect = text_surface.get_rect(center=((self.WIDTH+250) // 2, self.HEIGHT // 2 + y_offset))
        self.screen.blit(text_surface, text_rect)

    def draw_game_shape(self, shape, position):
        # Función para dibujar una forma en el juego fura de la grilla
        color = shape.color
        for y, row in enumerate(shape.original_shape):
            for x, cell in enumerate(row):
                if cell:
                    # Dibujar el cuadro interior de la forma
                    pygame.draw.rect(
                        self.screen,
                        color,
                        (position[0] * self.GRID_SIZE + x * self.GRID_SIZE, position[1] * self.GRID_SIZE + y * self.GRID_SIZE, self.GRID_SIZE, self.GRID_SIZE),
                    )
                    # Dibujar el contorno del cuadro
                    pygame.draw.rect(
                        self.screen,
                        WHITE,
                        (position[0] * self.GRID_SIZE + x * self.GRID_SIZE, position[1] * self.GRID_SIZE + y * self.GRID_SIZE, self.GRID_SIZE, self.GRID_SIZE),
                        1  # Grosor del contorno
                    )

    def draw_text(self, text, x, y, color):
        # Función para dibujar texto en la pantalla
        text_surface = self.FONT.render(text, True, color)
        self.screen.blit(text_surface, (x, y))

    def draw_arrow(self, x, y):
        # Función para dibujar una flecha simple en la pantalla
        pygame.draw.polygon(self.screen, WHITE, [(x, y), (x, y+20), (x+20, y+10)])

    def draw_next_shapes(self, next_shapes):
        # Función para dibujar las próximas piezas que aparecerán en la pantalla
        self.draw_text("Next Pieces:", self.WIDTH + 20, 160, WHITE)
        for i, shape in enumerate(next_shapes):
            shape_position = [self.GRID_WIDTH + 2.5, 7 + i * 3]
            self.draw_game_shape(Shape(shape), shape_position)
            # Dibuja la flecha apuntando a la primera next_shape
            if i == 0:
                arrow_x = shape_position[0] * self.GRID_SIZE - 40
                arrow_y = shape_position[1] * self.GRID_SIZE + 10
                self.draw_arrow(arrow_x, arrow_y)

    def draw_held_shape(self,held_shape):
        # Función para dibujar la pieza retenida en la pantalla
        self.draw_text("Held Piece:", self.WIDTH + 20, 480, WHITE)
        if held_shape is not None:
            self.draw_game_shape(held_shape, [self.GRID_WIDTH + 2, 17.5]) 
    
    def score_calculator(self, lines_to_remove, perfect_clear, drop_height = 0):
        # Función para calcular el puntaje del jugador
        self.total_complete_rows += lines_to_remove
        if lines_to_remove > 0:
            self.combo_count += 1
            if self.combo_count > 0:
                self.score += 50 * self.combo_count * self.level
        if lines_to_remove == 1:
            self.score += 100 * self.level
        elif lines_to_remove == 2:
            self.score += 300 * self.level
        elif lines_to_remove == 3:
            self.score += 500 * self.level
        elif lines_to_remove == 4:
            self.score += 800 * self.level
        elif lines_to_remove == 1 and perfect_clear:
            self.score += 800 * self.level
        elif lines_to_remove == 2 and perfect_clear:
            self.score += 1200 * self.level
        elif lines_to_remove == 3 and perfect_clear:
            self.score += 1800 * self.level
        elif lines_to_remove == 4 and perfect_clear:
            self.score += 2000 * self.level
        elif lines_to_remove == 0:
            self.combo_count = -1  
        self.score += 2 * drop_height
        self.level = self.total_complete_rows // 10 + 1

    def load_high_score(self):
        # Función para cargar la puntuación más alta guardada
        try:
            with open("high_score.txt", "r") as file:
                return int(file.read())
        except FileNotFoundError:
            return 0

    def save_high_score(self):
        # Función para guardar la puntuación más alta
        with open("high_score.txt", "w") as file:
            file.write(str(self.score))
            
    def run(self):
        # Función para ejecutar la pantalla de inicio del juego
        pygame.display.set_caption("Tetris")
        self.screen.fill(BLACK)
        vertical_spacing = 50
        self.draw_text_centered("TETRIS", -vertical_spacing, WHITE)
        self.draw_text_centered("Presiona cualquier tecla para comenzar", vertical_spacing, WHITE)
        pygame.display.flip()
        waiting_for_key = True
        while waiting_for_key:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    waiting_for_key = False

    def start_game(self):
        # Función para iniciar el juego y gestionar la lógica del mismo
        clock = pygame.time.Clock()
        pygame.mixer.music.load("tetris.mp3")  # Reemplaza "nombre_del_archivo_de_audio.mp3" con tu archivo de audio
        pygame.mixer.music.set_volume(0.5)  # Ajusta el volumen según sea necesario
        pygame.mixer.music.play(-1)  # El argumento -1 indica reproducción en bucle
        board= Board(self.screen,self.GRID_WIDTH,self.GRID_HEIGHT,self.GRID_SIZE,self.WIDTH,self.HEIGHT)
        shapes_bag = random.sample(range(7), 6)
        shape = Shape(shapes_bag.pop(0))
        next_shapes = [shapes_bag.pop(0) for _ in range(3)]
        self.score=0
        self.level=1
        self.total_complete_rows= 0
        self.combo_count = -1
        key_left_pressed = False
        key_rigth_pressed = False
        key_down_pressed = False
        released_shape = False
        held_shape = None
        fps=0
        move_timer = 0
        move_delay = 8

        high_score = self.load_high_score()
        board.shape_entry(shape)
        while not any(board.grid[0]):
            self.screen.fill(BLACK)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        key_left_pressed = True
                    elif event.key == pygame.K_RIGHT:
                        key_rigth_pressed = True
                    elif event.key == pygame.K_UP:
                        board.rotate_shape_clockwise()      
                    elif event.key == pygame.K_DOWN:
                        key_down_pressed = True
                    elif event.key == pygame.K_SPACE:
                        fps=0
                        drop_height = board.hard_drop()                        
                        released_shape = False
                        lines_to_remove, perfect_clear = board.complete_lines()
                        self.score_calculator(lines_to_remove, perfect_clear, drop_height)
                        shape= Shape(next_shapes.pop(0))
                        next_shapes.append(shapes_bag.pop(0))
                        if len(shapes_bag) == 0:
                            shapes_bag = random.sample(range(7), 6)
                        board.shape_entry(shape)
                    elif event.key == pygame.K_z or event.key == pygame.K_LCTRL:
                        board.rotate_counterclockwise()
                    elif event.key == pygame.K_c or event.key == pygame.K_LSHIFT:
                        if held_shape is None:
                            fps=0
                            held_shape = board.shape
                            shape= Shape(next_shapes.pop(0))
                            next_shapes.append(shapes_bag.pop(0))
                            if len(shapes_bag) == 0:
                                shapes_bag = random.sample(range(7), 6)  
                            board.shape_entry(shape)
                        else:
                            if released_shape == False:
                                fps=0
                                board.shape_entry(held_shape)
                                released_shape = True
                                held_shape = shape
                        
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        key_down_pressed = False
                    elif event.key == pygame.K_LEFT:
                        key_left_pressed = False
                        move_timer = 0 
                    elif event.key == pygame.K_RIGHT:
                        key_rigth_pressed = False
                        move_timer = 0 

            if key_left_pressed:
                if move_timer == 0 or move_timer > move_delay:
                    board.move_shape_sides(-1, fps)
                move_timer += 1

            elif key_rigth_pressed:
                if move_timer == 0 or move_timer > move_delay:
                    board.move_shape_sides(1, fps)
                move_timer += 1
        

            original_board_speed = ((0.8 - ((self.level - 1) * 0.007))**(self.level - 1))
            if key_down_pressed:
                board.set_speed( original_board_speed / 10)
            else:
                board.set_speed(original_board_speed)

            if fps > board.speed * 30:
                fps=0
                if board.move_shape_down() == False:
                    released_shape = False
                    lines_to_remove, perfect_clear = board.complete_lines()
                    self.score_calculator(lines_to_remove, perfect_clear)
                    shape= Shape(next_shapes.pop(0))
                    next_shapes.append(shapes_bag.pop(0))
                    if len(shapes_bag) == 0:
                        shapes_bag = random.sample(range(7), 6)                  
                    board.shape_entry(shape)
                else:
                    if key_down_pressed:
                        self.score += 1

            self.draw_text(f"Level: {self.level}", self.WIDTH + 20, 10, WHITE)
            self.draw_text(f"Score: {self.score}", self.WIDTH + 20, 60, WHITE)
            self.draw_text(f"High Score: {high_score}", self.WIDTH + 20, 110, WHITE)
            self.draw_next_shapes(next_shapes)
            self.draw_held_shape(held_shape)
            board.draw_board()
            pygame.display.flip()

            fps += 1
            clock.tick(30)

        if self.score > high_score:
            self.save_high_score()
        
        pygame.mixer.music.stop()

    def game_over(self):
        # Función para manejar la pantalla de fin de juego
        self.screen.fill(BLACK)
        vertical_spacing = 50
        self.draw_text_centered("GAME OVER", -vertical_spacing, WHITE)
        self.draw_text_centered(f"Puntaje final: {self.score}", 0, WHITE)
        self.draw_text_centered("Presiona 'R' para reiniciar o 'Q' para salir", vertical_spacing, WHITE)
        pygame.display.flip()
        waiting_for_key = True
        while waiting_for_key:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        waiting_for_key = False
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
