import sys
import pygame
import time

from settings import Settings
from piece import Piece
from board import Board
from game_stats import GameStats
from text import TextImage
from stat_board import StatBoard


class Tetris:
    """ класс для управления ресурсами и поведением"""

    def __init__(self):
        """инициализация и создание ресурсов"""
        pygame.init()
        self.clock = pygame.time.Clock()  # для fps

        # настройки
        self.settings = Settings()

        pygame.display.set_icon(self.settings.icon)
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption(self.settings.caption)

        self.stats = GameStats(self)
        self.sb = StatBoard(self)
        self.text = TextImage(self)

        # переменные для начала игры
        self.board = Board(self)

    def run(self):
        """запуск основного цикла"""
        # скрываем мышь
        pygame.mouse.set_visible(False)

        while True:
            if self.stats.game_active:
                self._tetris_cycle()
            self._check_events()
            self._update_screen()

    def _check_events(self):
        # Отслеживание событий клавиатуры и мыши.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

    def _check_keydown_events(self, event):
        """нажатие клавиш"""
        try:
            if event.key == pygame.K_UP or event.key == pygame.K_KP5:
                # вращаем блок
                self.falling_piece.form['rotation'] = \
                    (self.falling_piece.form['rotation'] + 1) % len(
                        self.falling_piece.pieces[self.falling_piece.form['shape']])
                if not self.board.is_valid_position(self.board.blank_board, self.falling_piece):
                    self.falling_piece.form['rotation'] = \
                        (self.falling_piece.form['rotation'] - 1) % len(
                            self.falling_piece.pieces[self.falling_piece.form['shape']])
            elif (event.key == pygame.K_LEFT or event.key == pygame.K_KP4) \
                    and self.board.is_valid_position(self.board.blank_board, self.falling_piece, adj_x=-1):
                # двигаем фигуру влево
                self.falling_piece.form['x'] -= 1
                self.moving_left = True
                self.moving_right = False
                self.last_move_sideways_time = time.time()
            elif (event.key == pygame.K_RIGHT or event.key == pygame.K_KP6) \
                    and self.board.is_valid_position(self.board.blank_board, self.falling_piece, adj_x=1):
                # двигаем фигуру вправо
                self.falling_piece.form['x'] += 1
                self.moving_right = True
                self.moving_left = False
                self.last_move_sideways_time = time.time()
            elif event.key == pygame.K_DOWN:
                # двигаем фигуру вниз
                self.moving_down = True
                if self.board.is_valid_position(self.board.blank_board, self.falling_piece, adj_y=1):
                    self.falling_piece.form['y'] += 1
                self.last_move_down_time = time.time()
            elif event.key == pygame.K_SPACE:
                # бросаем фигуру вниз
                self.moving_down = False
                self.moving_left = False
                self.moving_right = False
                for i in range(1, self.settings.board_height):
                    if not self.board.is_valid_position(self.board.blank_board, self.falling_piece, adj_y=i):
                        break
                self.falling_piece.form['y'] += i - 1
            elif event.key == pygame.K_n:
                self._start_game()
            elif event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
        except AttributeError:
            pass

    def _check_keyup_events(self, event):
        # отпускаем клавишу; создаем непрерывное движение
        if event.key == pygame.K_LEFT or event.key == pygame.K_KP4:
            self.moving_left = False
        elif event.key == pygame.K_RIGHT or event.key == pygame.K_KP6:
            self.moving_right = False
        elif event.key == pygame.K_DOWN:
            self.moving_down = False
        elif event.key == pygame.K_p or event.key == pygame.K_PAUSE:
            # пауза
            self.screen.fill((0, 0, 0))
            self.text.show_text_screen('Pause')
            self._control_time()
        elif event.key == pygame.K_i:
            # информация
            self.screen.fill((0, 0, 0))
            self.text.show_info_screen('Tetris 2.0', self.text.info_text)
            self._control_time()
        elif event.key == pygame.K_F1 or event.key == pygame.K_h:
            # help
            self.screen.fill((0, 0, 0))
            self.text.show_info_screen('Control Keys', self.text.control_keys)
            self._control_time()

    def _control_time(self):
        """контроль времени в случае нажатия информационных клавиш или паузы"""
        self.last_move_down_time = time.time()
        self.last_move_sideways_time = time.time()
        self.last_fall_time = time.time()

    def _tetris_cycle(self):
        """игра"""
        if self.falling_piece is None:
            # No falling piece in play, so start a new piece at the top
            self.falling_piece = self.next_piece
            self.next_piece = Piece(self)
            self.last_fall_time = time.time()  # reset lastFallTime

            if not self.board.is_valid_position(self.board.blank_board, self.falling_piece):
                self.stats.game_active = False
                # вывести и записать результат
                # сравниваем с последней записью в словаре рекордов
                key, value = self.stats.records.popitem()
                if self.stats.score > value:
                    self.text.show_text_enter_name()
                    # получить name
                    name = self.text.get_name()
                    self.stats.save_record(name, self.stats.score)
                    if key != name:
                        self.stats.save_record(key, value)
                else:
                    self.stats.records[key] = value

        self._moving_and_falling()

    def _moving_and_falling(self):
        """управление движением фигуры"""
        if (self.moving_left or self.moving_right) and time.time() - self.last_move_sideways_time > \
                self.settings.move_side_ways_freq:
            if self.moving_left and self.board.is_valid_position(self.board.blank_board, self.falling_piece, adj_x=-1):
                self.falling_piece.form['x'] -= 1
            elif self.moving_right and self.board.is_valid_position(self.board.blank_board, self.falling_piece,
                                                                    adj_x=1):
                self.falling_piece.form['x'] += 1
            self.last_move_sideways_time = time.time()

        if self.moving_down and time.time() - self.last_move_down_time > self.settings.move_down_freq \
                and self.board.is_valid_position(self.board.blank_board, self.falling_piece, adj_y=1):
            self.falling_piece.form['y'] += 1
            self.last_move_down_time = time.time()

            # let the piece fall if it is time to fall
        if time.time() - self.last_fall_time > self.stats.fall_freq:
            # see if the piece has landed
            if not self.board.is_valid_position(self.board.blank_board, self.falling_piece, adj_y=1):
                # falling piece has landed, set it on the board
                self.board.add_to_board(self.board.blank_board, self.falling_piece)
                num_of_lines = self.board.remove_complete_lines(self.board.blank_board)
                if num_of_lines > 0:
                    self._calculate_points(num_of_lines)
                self.falling_piece = None
                # 10 за каждую фигуру
                self.stats.score += self.settings.point_piece
                self.sb.prep_score()
            else:
                # piece did not land, just move the piece down
                self.falling_piece.form['y'] += 1
                self.last_fall_time = time.time()

        self._calculate_level()

    def _calculate_points(self, num_of_lines):
        """подсчет очков"""
        if num_of_lines > 1:
            self.stats.score += self.settings.point_line * num_of_lines + \
                                self.settings.point_line * self.stats.level
            if num_of_lines == 4:
                self.stats.score += self.settings.tetris * self.stats.level
        else:
            self.stats.score += self.settings.point_line * self.stats.level
        self.sb.prep_score()

    def _calculate_level(self):
        self.stats.level, self.stats.fall_freq = self.stats.calculate_level_and_fallfreq(self.stats.level)
        self.sb.prep_level()

    def convert_to_pixel_coords(self, boxx, boxy):
        """" Convert the given xy coordinates of the board to xy coordinates of the location on the screen."""
        pixel_x = self.settings.x_margin + (boxx * self.settings.box_size)
        pixel_y = self.settings.top_margin + (boxy * self.settings.box_size)
        return pixel_x, pixel_y

    def draw_box(self, boxx, boxy, image, pixelx=None, pixely=None):
        """" draw a single box (each tetris piece has four boxes) at xy coordinates on the board.
        Or, if pixelx & pixely are specified, draw to the pixel coordinates stored in pixelx & pixely
        (this is used for the "Next" piece)."""
        if image == self.settings.blank:
            return
        if pixelx is None and pixely is None:
            pixelx, pixely = self.convert_to_pixel_coords(boxx, boxy)
        self.screen.blit(self.next_piece.images[image], (pixelx, pixely))
        # pygame.draw.rect(self.screen, (0, 0, 0), (pixelx + 1, pixely + 1, self.settings.box_size - 1, self.settings.box_size - 1))
        # pygame.draw.rect(DISPLAYSURF, LIGHTCOLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 4, BOXSIZE - 4))

    def draw_piece(self, piece, pixelx=None, pixely=None):
        shape_to_draw = piece.pieces[piece.form['shape']][piece.form['rotation']]
        if pixelx is None and pixely is None:
            # if pixelx & pixely hasn't been specified, use the location stored in the piece data structure
            pixelx, pixely = self.convert_to_pixel_coords(piece.form['x'], piece.form['y'])

        # draw each of the boxes that make up the piece
        for x in range(piece.template_width):
            for y in range(piece.template_height):
                if shape_to_draw[y][x] != self.settings.blank:
                    self.draw_box(None, None, piece.form['image'],
                                  pixelx + (x * self.settings.box_size), pixely + (y * self.settings.box_size))

    def draw_board(self, board):
        # draw the individual boxes on the board
        for x in range(self.settings.board_width):
            for y in range(self.settings.board_height):
                self.draw_box(x, y, board[x][y])

    def draw_next_piece(self, piece):
        """отображение следующей фигуры"""
        self.draw_piece(piece, pixelx=self.settings.screen_width - 1100, pixely=180)

    def _start_game(self):
        self.text.show_text_screen('T E T R I S')
        # сброс статистики
        self.stats.reset_stats()
        # загружаем рекорды
        self.stats.load_records()
        # запуск игры
        self.stats.game_active = True
        # показываем score, level, lines
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_records()
        # обнуляем установки
        del self.board
        self.board = Board(self)
        self.last_move_down_time = time.time()
        self.last_move_sideways_time = time.time()
        self.last_fall_time = time.time()
        self.moving_down = False
        self.moving_left = False
        self.moving_right = False
        # выводим на экран новые фигуры
        self.falling_piece = Piece(self)
        self.next_piece = Piece(self)

    def _draw_status(self):
        self.text.show_text_next('NEXT', (self.settings.screen_height / 2) - 390)
        self.text.show_text_next('LEVEL', self.settings.screen_height / 2)
        self.text.show_text_next('SCORE', (self.settings.screen_height / 2) + 200)

    def _update_screen(self):
        # При каждом проходе цикла перерисовывается экран
        self.screen.blit(self.settings.background, (0, 0))

        if not self.stats.game_active:
            self._start_game()
        self._draw_status()
        self.sb.show_score()
        self.sb.show_records()
        self.draw_board(self.board.blank_board)
        self.draw_next_piece(self.next_piece)
        if self.falling_piece is not None:
            self.draw_piece(self.falling_piece)

        # отображение последнего прорисованного окна
        pygame.display.flip()
        # скорость
        self.clock.tick(self.settings.fps)


if __name__ == '__main__':
    # Создание экземпляра и запуск игры.
    tet = Tetris()
    tet.run()
