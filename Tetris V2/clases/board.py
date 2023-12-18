import pygame
from clases.shape import Shape
from constants import WHITE, SHAPE_COLORS

class Board:
    def __init__(self, screen, width_boxes, height_boxes, box_size, width_game, height_game ):
        # Inicialización del tablero con propiedades y dimensiones
        self.grid = [[0] * width_boxes for _ in range(height_boxes)]
        self.speed = 1  # [s]
        self.screen = screen
        self.width = width_boxes
        self.height = height_boxes
        self.width_game = width_game
        self.height_game = height_game
        self.box_size = box_size

    def is_valid_position(self, shape, position):
        # Verifica si la posición de una forma en el tablero es válida
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x, new_y = position[0] + x, position[1] + y
                    if not (0 <= new_x < self.width and 0 <= new_y < self.height):
                        return False
                    if new_y < len(self.grid) and new_x < len(self.grid) and self.grid[new_y][new_x]:
                        return False
        return True
    
    def hard_drop(self):
        # Realiza un "hard drop" de la forma hasta que no sea posible seguir bajando
        before_position = self.shape_position[:]
        while self.is_valid_position(self.shape.current_state, (self.shape_position[0], self.shape_position[1] + 1)):
            self.shape_position[1] += 1
        self.update_board()
        return self.shape_position[1] - before_position[1]
        
    def move_shape_sides(self, direction, fps): 
        # Mueve la forma hacia los lados (izquierda o derecha)
        if (self.is_valid_position(self.shape.current_state, (self.shape_position[0]+direction, self.shape_position[1]))):
            self.shape_position[0] += direction
    
    def move_shape_down(self):
        # Mueve la forma hacia abajo
        if (self.is_valid_position(self.shape.current_state, (self.shape_position[0], self.shape_position[1] + 1))):
            self.shape_position[1] += 1
            return True
        else:
            self.update_board()
            return False
        
    def rotate_shape_clockwise(self):
        # Rota la forma en sentido horario
        new_shape_rotated = list(zip(*self.shape.current_state[::-1]))
        while self.is_valid_position(new_shape_rotated, self.shape_position) == False:
            new_shape_rotated = list(zip(*new_shape_rotated[::-1]))
        self.shape.set_current_state(new_shape_rotated)

    def rotate_counterclockwise(self):
        # Rota la forma en sentido antihorario
        new_shape_rotated = [list(reversed(col)) for col in zip(*self.shape.current_state)]
        while self.is_valid_position(new_shape_rotated, self.shape_position) == False:
            new_shape_rotated = [list(reversed(col)) for col in zip(*new_shape_rotated)]
        self.shape.set_current_state(new_shape_rotated)
    
    def update_board(self):
        # Actualiza el tablero con la posición actual de la forma
        for y, row in enumerate(self.shape.current_state):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[self.shape_position[1] + y][self.shape_position[0] + x] = self.shape.type + 1
        
    def complete_lines(self):
        # Verifica y elimina líneas completas en el tablero
        lines_to_remove = []
        for y, row in enumerate(self.grid):
            if all(row):
                lines_to_remove.append(y)

        for line in lines_to_remove:
            del self.grid[line]
            self.grid.insert(0, [0] * self.width)
        return len(lines_to_remove), all(all(elemento == 0 for elemento in fila) for fila in self.grid)

    def set_speed(self, speed):
        # Establece la velocidad del juego
        self.speed = speed

    def shape_entry(self, shape):
        # Coloca una nueva forma en la parte superior del tablero
        self.shape = shape
        self.shape_position = [self.width // 2 - len(shape.current_state[0]) // 2, 0]
    
    def draw_board(self):
        # Dibuja todo relativo al tablero
        for x in range(0, self.width_game, self.box_size):
            pygame.draw.line(self.screen, WHITE, (x, 0), (x, self.height_game))
        for y in range(0, self.height_game, self.box_size):
            pygame.draw.line(self.screen, WHITE, (0, y), (self.width_game, y))
        self.draw_shadow()
        self.draw_shape()
        self.draw_current_shapes()

    def draw_shape(self):
        # Dibuja la forma actual en el tablero
        color = self.shape.color
        for y, row in enumerate(self.shape.current_state):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(
                        self.screen,
                        color,
                        (self.shape_position[0] * self.box_size + x * self.box_size, self.shape_position[1] * self.box_size + y * self.box_size, self.box_size, self.box_size),
                    )
                    pygame.draw.rect(
                        self.screen,
                        WHITE,
                        (self.shape_position[0] * self.box_size + x * self.box_size, self.shape_position[1] * self.box_size + y * self.box_size, self.box_size, self.box_size),
                        1  
                    )

    def draw_current_shapes(self):
        # Dibuja las formas ya colocadas en el tablero
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell > 0:
                    color = SHAPE_COLORS[cell - 1]
                    for sy, srow in enumerate([[1]]):
                        for sx, scell in enumerate(srow):
                            if scell:
                                pygame.draw.rect(
                                    self.screen,
                                    color,
                                    (x * self.box_size + sx * self.box_size, y * self.box_size + sy * self.box_size, self.box_size, self.box_size),
                                )
                                pygame.draw.rect(
                                    self.screen,
                                    WHITE,
                                    (x * self.box_size + sx * self.box_size, y * self.box_size + sy * self.box_size, self.box_size, self.box_size),
                                    2  
                                )

    def draw_shadow(self):
        # Dibuja la sombra de la forma actual
        shadow_position = [self.shape_position[0], self.shape_position[1]]
        shadow_shape = [row[:] for row in self.shape.current_state]  

        while self.is_valid_position(shadow_shape, (shadow_position[0], shadow_position[1] + 1)):
            shadow_position[1] += 1

        for y, row in enumerate(shadow_shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(
                        self.screen,
                        (100, 100, 100),  
                        (shadow_position[0] * self.box_size + x * self.box_size, shadow_position[1] * self.box_size + y * self.box_size, self.box_size, self.box_size),
                    )
                    pygame.draw.rect(
                        self.screen,
                        WHITE,
                        (shadow_position[0] * self.box_size + x * self.box_size, shadow_position[1] * self.box_size + y * self.box_size, self.box_size, self.box_size),
                        1  
                    )
