import pygame
import sys
import random

pygame.init()
pygame.mixer.init()

WIDTH_BASE, HEIGHT_BASE = 300, 600
GRID_WIDTH, GRID_HEIGHT = 10, 20 
GRID_SIZE = HEIGHT_BASE // GRID_HEIGHT if HEIGHT_BASE // GRID_HEIGHT < WIDTH_BASE // GRID_WIDTH else WIDTH_BASE // GRID_WIDTH
WIDTH, HEIGHT = GRID_SIZE*GRID_WIDTH+1, GRID_SIZE * GRID_HEIGHT
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 0], [0, 1, 1]],
    [[1, 1, 1], [0, 1, 0]],
]
SHAPE_COLORS = {
    0: (0, 230, 253),    # celeste
    1: (0, 0, 255),    # Azul
    2: (255, 102, 0),    # Naranjo
    3: (255, 255, 0),  # Amarillo
    4: (0, 238, 0),  # Verde
    5: (255, 0, 0),    # Rojo
    6: (255, 0, 255),    # Morado
}


class Game:
    # Atributos de la clase
    FONT = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()
    def __init__(self,screen):
        
        self.totalCompleteRows= 0
        self.shapes_bag = random.sample(SHAPES, len(SHAPES))
        self.next_shapes = [self.shapes_bag.pop(0) for _ in range(3)]
        self.held_shape = None
        self.combo_count = -1
        self.load_high_score()
        self.screen = screen
        self.fps=0
        self.speed=30
        self.score=0
        self.level=1

    # Método de la clase
    def draw_text_centered(self, text, y_offset, color):
        text_surface = self.FONT.render(text, True, color)
        text_rect = text_surface.get_rect(center=((WIDTH+250) // 2, HEIGHT // 2 + y_offset))
        self.screen.blit(text_surface, text_rect)
    def draw_shape(self, shape, position, piece_type):
        color = SHAPE_COLORS[piece_type]
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    # Dibujar el cuadro interior de la forma
                    pygame.draw.rect(
                        self.screen,
                        color,
                        (position[0] * GRID_SIZE + x * GRID_SIZE, position[1] * GRID_SIZE + y * GRID_SIZE, GRID_SIZE, GRID_SIZE),
                    )
                    # Dibujar el contorno del cuadro
                    pygame.draw.rect(
                        self.screen,
                        WHITE,
                        (position[0] * GRID_SIZE + x * GRID_SIZE, position[1] * GRID_SIZE + y * GRID_SIZE, GRID_SIZE, GRID_SIZE),
                        1  # Grosor del contorno
                    )

    def draw_text(self,text, x, y, color):
        text_surface = self.FONT.render(text, True, color)
        self.screen.blit(text_surface, (x, y))
    
    def draw_next_shapes(self,next_shapes):
        self.draw_text("Next Pieces:", WIDTH + 20, 150, WHITE)
        for i, shape in enumerate(next_shapes):
            self.draw_shape(shape, [GRID_WIDTH + 1, 6 + i * 3], piece_type=SHAPES.index(shape))
    def draw_held_shape(self,held_shape):
        self.draw_text("Held Piece:", WIDTH + 20, 480, WHITE)
        if held_shape is not None:
            self.draw_shape(held_shape, [GRID_WIDTH + 1, 17], piece_type=SHAPES.index(held_shape)) 
    
    def score_calculator(self,lines_to_remove,board):
        print(lines_to_remove)
        self.totalCompleteRows += lines_to_remove
        self.level = self.totalCompleteRows // 2 + 1
        self.speed = 30*(0.8 - ((self.level - 1) * 0.007))**(self.level - 1)
        perfect_clear = all(all(elemento == 0 for elemento in fila) for fila in board.grid)
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
    def start_game(self):
        fps=0
        self.score=0
        board=Board(self.screen)
        self.shapes_bag = random.sample(SHAPES, len(SHAPES))
        self.speed=board.speed
        current_shape = self.shapes_bag.pop(0)
        shape=Shape(current_shape)
        original_current_shape = current_shape
        current_position = [GRID_WIDTH // 2 - len(current_shape[0]) // 2, 0]
        current_piece_type = SHAPES.index(current_shape)
        released_shape = False
        self.level = 1
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and current_position[0] > 0:
                        if board.is_valid_position(current_shape, (current_position[0] - 1, current_position[1])):
                            current_position[0] -= 1
                    elif event.key == pygame.K_RIGHT and current_position[0] < GRID_WIDTH - len(current_shape[0]):
                        if board.is_valid_position(current_shape, (current_position[0] + 1, current_position[1])):
                            current_position[0] += 1
                    elif event.key == pygame.K_SPACE:
                        # Mover hacia abajo hasta la posición de la sombra
                        before_position = current_position[:]
                        while board.is_valid_position(current_shape, (current_position[0], current_position[1] + 1)):
                            current_position[1] += 1
                        self.score += 2 * (current_position[1]-before_position[1])
                        self.score_calculator(board.update_board(current_shape, current_position, current_piece_type),board)
                        current_shape = self.next_shapes.pop(0)
                        original_current_shape = current_shape
                        if len(self.shapes_bag) == 0:
                            self.shapes_bag = random.sample(SHAPES, len(SHAPES))
                        self.next_shapes.append(self.shapes_bag.pop(0))
                        current_position = [GRID_WIDTH // 2 - len(current_shape[0]) // 2, 0]
                        current_piece_type = SHAPES.index(current_shape)
                        released_shape = False
                    elif event.key == pygame.K_UP:
                        new_shape = board.rotate_shape_clockwise(current_shape)
                        while board.is_valid_position(new_shape, (current_position[0], current_position[1]))==False:
                            new_shape = board.rotate_shape_clockwise(new_shape)
                        current_shape = new_shape
                            
                    elif event.key == pygame.K_z or event.key == pygame.K_LCTRL:
                        new_shape = board.rotate_shape_counterclockwise(current_shape)
                        if board.is_valid_position(new_shape, current_position):
                            current_shape = new_shape
                    elif event.key == pygame.K_c or event.key == pygame.K_LSHIFT:
                        # Intercambiar figura actual con la figura guardada
                        if (self.held_shape is None):
                            self.held_shape = original_current_shape
                            current_shape = self.next_shapes.pop(0)
                            if len(self.shapes_bag) == 0:
                                self.shapes_bag = random.sample(SHAPES, len(SHAPES))
                            self.next_shapes.append(self.shapes_bag.pop(0))
                            original_current_shape = current_shape
                            current_position = [GRID_WIDTH // 2 - len(current_shape[0]) // 2, 0]
                            current_piece_type = SHAPES.index(current_shape)
                            
                        elif (released_shape==False):
                            current_shape, self.held_shape = self.held_shape, original_current_shape
                            released_shape = True
                            original_current_shape = current_shape
                            current_position = [GRID_WIDTH // 2 - len(current_shape[0]) // 2, 0]
                            current_piece_type = SHAPES.index(current_shape)
                            

                        
                    elif event.key == pygame.K_DOWN:
                        self.speed = self.speed / 6
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        self.speed = 30* (0.8 - ((self.level - 1) * 0.007))**(self.level - 1)
            if(fps>self.speed):
                fps=0
                if board.is_valid_position(current_shape, (current_position[0], current_position[1] + 1)):
                    current_position[1] += 1
                    if self.speed != 30*(0.8 - ((self.level - 1) * 0.007))**(self.level - 1):
                        self.score += 1
                else:
                    self.score_calculator(board.update_board(current_shape, current_position, current_piece_type),board)
                    current_shape = self.next_shapes.pop(0)
                    original_current_shape = current_shape
                    if len(self.shapes_bag) == 0:
                        self.shapes_bag = random.sample(SHAPES, len(SHAPES))
                    self.next_shapes.append(self.shapes_bag.pop(0))
                    current_position = [GRID_WIDTH // 2 - len(current_shape[0]) // 2, 0]
                    current_piece_type = SHAPES.index(current_shape)
                    print(False)
            

            if any(board.grid[0]):
                print("Fin del juego")
                pygame.mixer.music.stop()  # El argumento -1 indica reproducción en bucle
                if(self.score > self.high_score):
                    self.save_high_score(self.score)
                return

            self.screen.fill(BLACK)
            board.draw_grid()
            self.draw_text(f"Level: {self.level}", WIDTH + 20, 10, WHITE)
            self.draw_text(f"Score: {self.score}", WIDTH + 20, 60, WHITE)
            self.draw_text(f"High Score: {self.load_high_score()}", WIDTH + 20, 110, WHITE)

            

            for y, row in enumerate(board.grid):
                for x, cell in enumerate(row):
                    if cell > 0:
                        board.draw_shape([[1]], [x, y], piece_type=cell - 1)

                shadow_position = [current_position[0], current_position[1]]
                shadow_shape = [row[:] for row in current_shape]  # Copia la forma actual

                while board.is_valid_position(shadow_shape, (shadow_position[0], shadow_position[1] + 1)):
                    shadow_position[1] += 1
            board.draw_shadow(shadow_shape, shadow_position)
            board.draw_shape(current_shape, current_position, piece_type=current_piece_type)
            self.draw_next_shapes(self.next_shapes)
            self.draw_held_shape(self.held_shape)

            pygame.display.flip()
            fps+=1
            self.clock.tick(30)



    def run(self):
        pygame.init()
        pygame.mixer.init()
        screen = pygame.display.set_mode((WIDTH + 250, HEIGHT))
        pygame.display.set_caption("Tetris")
        screen.fill(BLACK)
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
        while True:
            self.start_game()
            self.run()
    def load_high_score(self):
        try:
            with open("high_score.txt", "r") as file:
                self.high_score = int(file.read())
        except FileNotFoundError:
            self.high_score = 0
    def save_high_score(score):
        with open("high_score.txt", "w") as file:
            file.write(str(score))
class Board:
    def __init__(self,screen):
        self.grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
        self.speed = 30
        self.screen = screen

    def is_valid_position(self, shape, position):
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x, new_y = position[0] + x, position[1] + y
                    # Verificar límites del tablero
                    if not (0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT):
                        return False
                    if new_y < len(self.grid) and new_x < len(self.grid) and self.grid[new_y][new_x]:
                        return False
        return True
    def draw_grid(self):
        for x in range(0, WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, WHITE, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, WHITE, (0, y), (WIDTH, y))
    def draw_shape(self, shape, position, piece_type):
        color = SHAPE_COLORS[piece_type]
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    # Dibujar el cuadro interior de la forma
                    pygame.draw.rect(
                        self.screen,
                        color,
                        (position[0] * GRID_SIZE + x * GRID_SIZE, position[1] * GRID_SIZE + y * GRID_SIZE, GRID_SIZE, GRID_SIZE),
                    )
                    # Dibujar el contorno del cuadro
                    pygame.draw.rect(
                        self.screen,
                        WHITE,
                        (position[0] * GRID_SIZE + x * GRID_SIZE, position[1] * GRID_SIZE + y * GRID_SIZE, GRID_SIZE, GRID_SIZE),
                        1  # Grosor del contorno
                    )
    def draw_shadow(self, shape, position):
        shadow_position = [position[0], position[1]]
        shadow_shape = [row[:] for row in shape]  # Copia la forma actual

        while self.is_valid_position(shadow_shape, (shadow_position[0], shadow_position[1] + 1)):
            shadow_position[1] += 1

        for y, row in enumerate(shadow_shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(
                        self.screen,
                        (100, 100, 100),  # Color de la sombra (gris oscuro)
                        (shadow_position[0] * GRID_SIZE + x * GRID_SIZE, shadow_position[1] * GRID_SIZE + y * GRID_SIZE, GRID_SIZE, GRID_SIZE),
                    )
                    pygame.draw.rect(
                        self.screen,
                        WHITE,
                        (shadow_position[0] * GRID_SIZE + x * GRID_SIZE, shadow_position[1] * GRID_SIZE + y * GRID_SIZE, GRID_SIZE, GRID_SIZE),
                        1  # Grosor del contorno
                    )
    def update_board(self, shape, position, piece_type):
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[position[1] + y][position[0] + x] = piece_type + 1

        # Verificar y eliminar líneas completas
        lines_to_remove = []
        for y, row in enumerate(self.grid):
            if all(row):
                lines_to_remove.append(y)

        for line in lines_to_remove:
            del self.grid[line]
            self.grid.insert(0, [0] * GRID_WIDTH)
        return len(lines_to_remove)

    def rotate_shape_clockwise(self,shape):
        return [[shape[y][x] for y in range(len(shape) - 1, -1, -1)] for x in range(len(shape[0]))]

    def rotate_shape_counterclockwise(self,shape):
        return [[shape[y][x] for y in range(len(shape))] for x in range(len(shape[0]) - 1, -1, -1)]

class Shape:
    def __init__(self, shape):
        self.type = SHAPES.index(shape)
        self.color = SHAPE_COLORS[self.type]
        self.current_state = shape

    # Método de la clase
    def rotate_clockwise(self):
        return [[self.current_state[y][x] for y in range(len(self.current_state) - 1, -1, -1)] for x in range(len(self.current_state[0]))]

    def rotate_counterclockwise(self):
        return [[self.current_state[y][x] for y in range(len(self.current_state))] for x in range(len(self.current_state[0]) - 1, -1, -1)]

def main():
    screen = pygame.display.set_mode((WIDTH + 250, HEIGHT))
    pygame.display.set_caption("Tetris")
    game = Game(screen)
    game.run()
    print(game.high_score)

if __name__ == "__main__":
    main()

















