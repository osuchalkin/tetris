import pygame


class Settings():
    """класс для хранения всех настроек игры"""

    def __init__(self):
        """Инициализирует статические настройки игры"""
        # параметры экрана
        if pygame.display.Info().current_w < 1200 or pygame.display.Info().current_h < 1000:
            self.screen_width = 840
            self.screen_height = 700
            self.background = pygame.transform.scale(pygame.image.load("images/tet.bmp"), (self.screen_width, self.screen_height))
        else:
            self.screen_width = 1200
            self.screen_height = 1000
            self.background = pygame.image.load("images/tet.bmp")      
        
        # получить разрешение монитора
        #  desktop_width, desktop_height = pygame.display.get_desktop_sizes()[0]
        self.fps = 90
        
        self.caption = "TETRIS 2.0"
        self.icon = pygame.image.load("images/tetris.png")

        # параметры box, piece, board
        self.box_size = self.screen_width / 30
        self.board_width = 10
        self.board_height = 20
        self.blank = '.'
        self.removed_line = False

        # параметры времени
        self.move_side_ways_freq = 0.15  # скорость клавиш left, right
        self.move_down_freq = 0.1  # скорость клавиш down
        self.fall_speed = 0.7  # скорость падения фигуры
        self.wait_time = 50 # 50 секунд на один level
        self.scale_level = 0.05

        # статистика
        self.point_piece = 10
        self.point_line = 100
        self.tetris = 1000

        # другие параметры экрана
        self.x_margin = int((self.screen_width - self.board_width * self.box_size) / 2)  # от края экрана до board
        self.top_margin = self.screen_height - (self.board_height * self.box_size) - self.box_size  # от верха до board
