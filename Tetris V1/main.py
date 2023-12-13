import pygame
import sys
import random

# Inicializar Pygame
pygame.init()
pygame.mixer.init()
# Definir constantes
WIDTH_BASE, HEIGHT_BASE = 300, 600
GRID_WIDTH, GRID_HEIGHT = 10, 20 
GRID_SIZE = HEIGHT_BASE // GRID_HEIGHT if HEIGHT_BASE // GRID_HEIGHT < WIDTH_BASE // GRID_WIDTH else WIDTH_BASE // GRID_WIDTH
WIDTH, HEIGHT = GRID_SIZE*GRID_WIDTH+1, GRID_SIZE * GRID_HEIGHT
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
shapes_bag=[]

# Definir formas de Tetris
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 0], [0, 1, 1]],
    [[1, 1, 1], [0, 1, 0]],
]

# Inicializar pantalla
screen = pygame.display.set_mode((WIDTH + 250, HEIGHT))
pygame.display.set_caption("Tetris")

# Pantalla de inicio
def load_high_score():
    try:
        with open("high_score.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

# Guardar puntaje máximo en un archivo
def save_high_score(score):
    with open("high_score.txt", "w") as file:
        file.write(str(score))
high_score = 0      
def show_start_screen():
    global high_score
    screen.fill(BLACK)
    high_score = load_high_score()

    # Centrar el texto "TETRIS"
    vertical_spacing = 50


# Uso de la función draw_text_centered para centrar los textos vertical y horizontalmente
    draw_text_centered("TETRIS", -vertical_spacing, WHITE)
    draw_text_centered("Presiona cualquier tecla para comenzar", vertical_spacing, WHITE)
    pygame.display.flip()
    waiting_for_key = True
    while waiting_for_key:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                waiting_for_key = False
                
    pygame.mixer.music.load("tetris.mp3")  # Reemplaza "nombre_del_archivo_de_audio.mp3" con tu archivo de audio
    pygame.mixer.music.set_volume(0.5)  # Ajusta el volumen según sea necesario
    pygame.mixer.music.play(-1)  # El argumento -1 indica reproducción en bucle


# Pantalla de juego finalizado
def show_game_over_screen():
    global board
    global totalCompleteRows
    global level
    global score
    global next_shapes
    global speed
    global combo_count
    global held_shape
    screen.fill(BLACK)
    vertical_spacing = 50
    draw_text_centered("GAME OVER", -vertical_spacing, WHITE)
    draw_text_centered(f"Puntaje final: {score}", 0, WHITE)
    draw_text_centered("Presiona 'R' para reiniciar o 'Q' para salir", vertical_spacing, WHITE)
    pygame.display.flip()
    waiting_for_key = True
    while waiting_for_key:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # Reiniciar el juego
                    board = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT+2)]
                    totalCompleteRows = 0
                    level = 1
                    score = 0
                    shapes_bag = [random.choice(SHAPES) for _ in range(7)]
                    next_shapes = [shapes_bag.pop(0) for _ in range(3)]
                    speed = 30*(0.8 - ((level - 1) * 0.007))**(level - 1)
                    combo_count = -1
                    held_shape = None
                    pygame.mixer.music.load("tetris.mp3")  # Reemplaza "nombre_del_archivo_de_audio.mp3" con tu archivo de audio
                    pygame.mixer.music.set_volume(0.5)  # Ajusta el volumen según sea necesario
                    pygame.mixer.music.play(-1)  # El argumento -1 indica reproducción en bucle
                    return  # Salir de la función para reiniciar el juego
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

# Función para dibujar el tablero
def draw_grid():
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(screen, WHITE, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, WHITE, (0, y), (WIDTH, y))

# Función para dibujar una forma en el tablero
SHAPE_COLORS = {
    0: (0, 230, 253),    # celeste
    1: (0, 0, 255),    # Azul
    2: (255, 102, 0),    # Naranjo
    3: (255, 255, 0),  # Amarillo
    4: (0, 238, 0),  # Verde
    5: (255, 0, 0),    # Rojo
    6: (255, 0, 255),    # Morado
}

def rotate_shape_clockwise(shape):
    return [[shape[y][x] for y in range(len(shape) - 1, -1, -1)] for x in range(len(shape[0]))]

def rotate_shape_counterclockwise(shape):
    return [[shape[y][x] for y in range(len(shape))] for x in range(len(shape[0]) - 1, -1, -1)]



# Inicializar el tablero
board = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
totalCompleteRows = 0
level = 1
score = 0
shapes_bag = random.sample(SHAPES, len(SHAPES))
next_shapes = [shapes_bag.pop(0) for _ in range(3)]
speed = 30*(0.8 - ((level - 1) * 0.007))**(level - 1)
held_shape = None
combo_count = -1
# Estado del juego
class GameState:
    START_SCREEN = 0
    PLAYING = 1
    GAME_OVER = 2

current_state = GameState.START_SCREEN
# Función para actualizar el tablero
def update_board(shape, position, piece_type):
    global totalCompleteRows
    global level
    global score
    global speed
    global combo_count
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                board[position[1] + y][position[0] + x] = piece_type + 1

    # Verificar y eliminar líneas completas
    lines_to_remove = []
    for y, row in enumerate(board):
        if all(row):
            lines_to_remove.append(y)

    for line in lines_to_remove:
        del board[line]
        board.insert(0, [0] * GRID_WIDTH)
    totalCompleteRows += len(lines_to_remove)
    level = totalCompleteRows // 2 + 1
    speed = 30*(0.8 - ((level - 1) * 0.007))**(level - 1)
    perfect_clear = all(all(elemento == 0 for elemento in fila) for fila in board)
    if len(lines_to_remove) > 0:
        combo_count += 1
        if combo_count > 0:
            score += 50 * combo_count * level
    if len(lines_to_remove) == 1:
        score += 100 * level
    elif len(lines_to_remove) == 2:
        score += 300 * level
    elif len(lines_to_remove) == 3:
        score += 500 * level
    elif len(lines_to_remove) == 4:
        score += 800 * level
    elif len(lines_to_remove) == 1 and perfect_clear:
        score += 800 * level
    elif len(lines_to_remove) == 2 and perfect_clear:
        score += 1200 * level
    elif len(lines_to_remove) == 3 and perfect_clear:
        score += 1800 * level
    elif len(lines_to_remove) == 4 and perfect_clear:
        score += 2000 * level
    else:
        combo_count = -1

# Función para verificar si una rotación es válida
def is_valid_position(shape, position):
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                new_x, new_y = position[0] + x, position[1] + y
                # Verificar límites del tablero
                if not (0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT):
                    return False
                if new_y < len(board) and new_x < len(board[new_y]) and board[new_y][new_x]:
                    return False
    return True

# Función principal
font = pygame.font.Font(None, 36)
def draw_text(text, x, y, color):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def draw_text_centered(text, y_offset, color):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=((WIDTH+250) // 2, HEIGHT // 2 + y_offset))
    screen.blit(text_surface, text_rect)

def draw_next_shapes(next_shapes):
    draw_text("Next Pieces:", WIDTH + 20, 150, WHITE)
    for i, shape in enumerate(next_shapes):
        draw_shape(shape, [GRID_WIDTH + 1, 6 + i * 3], piece_type=SHAPES.index(shape))

def draw_shape(shape, position, piece_type):
    color = SHAPE_COLORS[piece_type]
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                # Dibujar el cuadro interior de la forma
                pygame.draw.rect(
                    screen,
                    color,
                    (position[0] * GRID_SIZE + x * GRID_SIZE, position[1] * GRID_SIZE + y * GRID_SIZE, GRID_SIZE, GRID_SIZE),
                )
                # Dibujar el contorno del cuadro
                pygame.draw.rect(
                    screen,
                    WHITE,
                    (position[0] * GRID_SIZE + x * GRID_SIZE, position[1] * GRID_SIZE + y * GRID_SIZE, GRID_SIZE, GRID_SIZE),
                    1  # Grosor del contorno
                )
def draw_shadow(shape, position):
    shadow_position = [position[0], position[1]]
    shadow_shape = [row[:] for row in shape]  # Copia la forma actual

    while is_valid_position(shadow_shape, (shadow_position[0], shadow_position[1] + 1)):
        shadow_position[1] += 1

    for y, row in enumerate(shadow_shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(
                    screen,
                    (100, 100, 100),  # Color de la sombra (gris oscuro)
                    (shadow_position[0] * GRID_SIZE + x * GRID_SIZE, shadow_position[1] * GRID_SIZE + y * GRID_SIZE, GRID_SIZE, GRID_SIZE),
                )
                pygame.draw.rect(
                    screen,
                    WHITE,
                    (shadow_position[0] * GRID_SIZE + x * GRID_SIZE, shadow_position[1] * GRID_SIZE + y * GRID_SIZE, GRID_SIZE, GRID_SIZE),
                    1  # Grosor del contorno
                )

def draw_held_shape(held_shape):
    draw_text("Held Piece:", WIDTH + 20, 480, WHITE)
    if held_shape is not None:
        draw_shape(held_shape, [GRID_WIDTH + 1, 17], piece_type=SHAPES.index(held_shape))

def main():
    global board
    global totalCompleteRows
    global level
    global score
    global next_shapes
    global speed
    global held_shape
    global shapes_bag
    global combo_count
    combo_count = -1
    clock = pygame.time.Clock()
    current_shape = shapes_bag.pop(0)
    original_current_shape = current_shape
    current_position = [GRID_WIDTH // 2 - len(current_shape[0]) // 2, 0]
    current_piece_type = SHAPES.index(current_shape)
    released_shape = False
    show_start_screen()  # Mostrar pantalla de inicio al principio
    fps=0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and current_position[0] > 0:
                    if is_valid_position(current_shape, (current_position[0] - 1, current_position[1])):
                        current_position[0] -= 1
                elif event.key == pygame.K_RIGHT and current_position[0] < GRID_WIDTH - len(current_shape[0]):
                    if is_valid_position(current_shape, (current_position[0] + 1, current_position[1])):
                        current_position[0] += 1
                elif event.key == pygame.K_SPACE:
                    # Mover hacia abajo hasta la posición de la sombra
                    before_position = current_position[:]
                    while is_valid_position(current_shape, (current_position[0], current_position[1] + 1)):
                        current_position[1] += 1
                    score += 2 * (current_position[1]-before_position[1])
                    update_board(current_shape, current_position, current_piece_type)
                    current_shape = next_shapes.pop(0)
                    original_current_shape = current_shape
                    if len(shapes_bag) == 0:
                        shapes_bag = random.sample(SHAPES, len(SHAPES))
                    next_shapes.append(shapes_bag.pop(0))
                    current_position = [GRID_WIDTH // 2 - len(current_shape[0]) // 2, 0]
                    current_piece_type = SHAPES.index(current_shape)
                    released_shape = False
                elif event.key == pygame.K_UP:
                    new_shape = rotate_shape_clockwise(current_shape)
                    while is_valid_position(new_shape, (current_position[0], current_position[1]))==False:
                        new_shape = rotate_shape_clockwise(new_shape)
                    current_shape = new_shape
                        
                elif event.key == pygame.K_z or event.key == pygame.K_LCTRL:
                    new_shape = rotate_shape_counterclockwise(current_shape)
                    if is_valid_position(new_shape, current_position):
                        current_shape = new_shape
                elif event.key == pygame.K_c or event.key == pygame.K_LSHIFT:
                    # Intercambiar figura actual con la figura guardada
                    if (held_shape is None):
                        held_shape = original_current_shape
                        current_shape = next_shapes.pop(0)
                        if len(shapes_bag) == 0:
                            shapes_bag = random.sample(SHAPES, len(SHAPES))
                        next_shapes.append(shapes_bag.pop(0))
                        original_current_shape = current_shape
                        current_position = [GRID_WIDTH // 2 - len(current_shape[0]) // 2, 0]
                        current_piece_type = SHAPES.index(current_shape)
                        
                    elif (released_shape==False):
                        current_shape, held_shape = held_shape, original_current_shape
                        released_shape = True
                        original_current_shape = current_shape
                        current_position = [GRID_WIDTH // 2 - len(current_shape[0]) // 2, 0]
                        current_piece_type = SHAPES.index(current_shape)
                        

                    
                elif event.key == pygame.K_DOWN:
                    speed = speed / 6
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    speed = 30* (0.8 - ((level - 1) * 0.007))**(level - 1)
                    
        if(fps>speed):
            fps=0
            print(combo_count)
            if is_valid_position(current_shape, (current_position[0], current_position[1] + 1)):
                current_position[1] += 1
                if speed != 30*(0.8 - ((level - 1) * 0.007))**(level - 1):
                    score += 1
            else:
                update_board(current_shape, current_position, current_piece_type)
                current_shape = next_shapes.pop(0)
                original_current_shape = current_shape
                if len(shapes_bag) == 0:
                    shapes_bag = random.sample(SHAPES, len(SHAPES))
                next_shapes.append(shapes_bag.pop(0))
                current_position = [GRID_WIDTH // 2 - len(current_shape[0]) // 2, 0]
                current_piece_type = SHAPES.index(current_shape)
                print(False)
        

        if any(board[0]):
            print("Fin del juego")
            pygame.mixer.music.stop()  # El argumento -1 indica reproducción en bucle
            if(score > high_score):
                save_high_score(score)
            show_game_over_screen()  # Mostrar pantalla de juego finalizado


        screen.fill(BLACK)
        draw_grid()
        draw_text(f"Level: {level}", WIDTH + 20, 10, WHITE)
        draw_text(f"Score: {score}", WIDTH + 20, 60, WHITE)
        draw_text(f"High Score: {load_high_score()}", WIDTH + 20, 110, WHITE)

        

        for y, row in enumerate(board):
            for x, cell in enumerate(row):
                if cell > 0:
                    draw_shape([[1]], [x, y], piece_type=cell - 1)

            shadow_position = [current_position[0], current_position[1]]
            shadow_shape = [row[:] for row in current_shape]  # Copia la forma actual

            while is_valid_position(shadow_shape, (shadow_position[0], shadow_position[1] + 1)):
                shadow_position[1] += 1
        draw_shadow(shadow_shape, shadow_position)
        draw_shape(current_shape, current_position, piece_type=current_piece_type)
        draw_next_shapes(next_shapes)
        draw_held_shape(held_shape)

        pygame.display.flip()
        fps+=1
        clock.tick(30)

if __name__ == "__main__":
    while True:
        main()
