import pygame.font
import pygame
import sys


class TextImage():
    """для вывода текстовой информации"""

    def __init__(self, tet_game):
        self.screen = tet_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = tet_game.settings
        self.text_color = (0, 255, 255)
        self.text_shadow_color = (0, 85, 255)
        self.text_next_color = (0, 0, 170)
        self.name_color = (255, 85, 0)
        self.small_font = pygame.font.SysFont(None, 60)
        self.big_font = pygame.font.SysFont(None, 100)
        self.next_font = pygame.font.SysFont(None, 50)
        self.info_font = pygame.font.SysFont(None, 30)

        self.info_text = ['This game is clone Tetris-game created Alex Pajitnov in 1984.',
                          'Also this clone based on Al Sweigarts some coding idea and some idea',
                          'which represented by A.Banzhaf and E.Kappel in their Tetris clone - Professional TET42.',
                          'Pieces are drawn on the basis of Damian Yerricks picture:',
                          'https://commons.wikimedia.org/w/index.php?curid=1368672',
                          '',
                          '© Oleh Suchalkin 2021']

        self.control_keys = ['LEFT or 4 - left move',
                             'RIGHT or 6 - right move',
                             'UP or 5 - rotation',
                             'DOWN - down move',
                             '',
                             'P or PAUSE = pause',
                             'N - new game',
                             'I - info',
                             'Q - exit',
                             'H or F1 - this help']

    def make_text_obj(self, text, font, color):
        image = font.render(text, True, color)
        image_rect = image.get_rect()
        return image, image_rect

    def show_text_screen(self, text):
        """показывает большой текст в центре экрана - название, окончание и проч."""
        # рисует тень
        title_screen, title_rect = self.make_text_obj(text, self.big_font, self.text_shadow_color)
        title_rect.center = (int(self.settings.screen_width / 2),
                             int(self.settings.screen_height / 2))
        self.screen.blit(title_screen, title_rect)

        # рисует текст
        title_screen, title_rect = self.make_text_obj(text, self.big_font, self.text_color)
        title_rect.center = (int(self.settings.screen_width / 2) - 3,
                             int(self.settings.screen_height / 2) - 3)
        self.screen.blit(title_screen, title_rect)

        # рисуем "Press a key to play"
        presskey_screen, presskey_rect = self.make_text_obj('Press a key to play', self.small_font, self.text_color)
        presskey_rect.center = (int(self.settings.screen_width / 2),
                                int(self.settings.screen_height / 2) + 300)
        self.screen.blit(presskey_screen, presskey_rect)

        while self.check_for_keypress() is None:
            pygame.display.flip()

    def check_for_keypress(self):
        """ожидает события KEYUP"""
        # проверка на выход из програмы (Х или ESC)
        self.check_for_quit()
        for event in pygame.event.get([pygame.KEYDOWN, pygame.KEYUP]):
            if event == pygame.KEYDOWN:
                continue
            return event.key
        return None

    def check_for_quit(self):
        for event in pygame.event.get(pygame.QUIT):  # get all the QUIT event
            pygame.quit()
            sys.exit()

    def show_text_next(self, text, y):
        """Next, Level, Score"""
        title_screen, title_rect = self.make_text_obj(text, self.next_font, self.text_next_color)
        title_rect.center = (int(self.settings.x_margin / 2), y)
        self.screen.blit(title_screen, title_rect)

    def show_text_enter_name(self):
        title_screen = self.small_font.render('Enter your name:', True, self.name_color, (0, 0, 0))
        title_rect = title_screen.get_rect()
        title_rect.center = (int(self.settings.screen_width / 2),
                             int(self.settings.screen_height / 2) - 120)
        self.screen.blit(title_screen, title_rect)

        pygame.display.flip()

    def get_name(self):
        # параметры окна ввода
        screen_width, screen_height = self.settings.board_width * self.settings.box_size, 100
        screen_color = (0, 0, 0)
        screen_rect = pygame.Rect(0, 0, screen_width, screen_height)
        screen_rect.midbottom = self.screen_rect.center
        # получаем ввод
        name = ""
        input_active = True
        while input_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    break
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    input_active = True
                    name = ""
                elif event.type == pygame.KEYDOWN and input_active:
                    if event.key == pygame.K_RETURN:
                        input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        name += event.unicode
                        if len(name) > 10:
                            name = name[:-1]
                # отображаем окно ввода
                self.screen.fill(screen_color, screen_rect)
                name_image = self.big_font.render(name, True, self.name_color)
                name_image_rect = name_image.get_rect()
                name_image_rect.center = screen_rect.center
                self.screen.blit(name_image, name_image_rect)

                pygame.display.flip()

        return name

    def show_info_screen(self, title, text):
        """показывает большой текст в центре экрана - название, окончание и проч."""
        # рисует тень
        title_screen, title_rect = self.make_text_obj(title, self.big_font, self.text_shadow_color)
        title_rect.center = (int(self.settings.screen_width / 2), 100)
        self.screen.blit(title_screen, title_rect)

        # рисует текст
        title_screen, title_rect = self.make_text_obj(title, self.big_font, self.text_color)
        title_rect.center = (int(self.settings.screen_width / 2) - 3, 100 - 3)
        self.screen.blit(title_screen, title_rect)

        i = 1
        for info in text:
            title_screen, title_rect = self.make_text_obj(info, self.info_font, self.text_color)
            title_rect.center = (int(self.settings.screen_width / 2), 300 + 30 * i)
            self.screen.blit(title_screen, title_rect)
            i += 1

        # рисуем "Press a key to play"
        presskey_screen, presskey_rect = self.make_text_obj('Press a key to play', self.small_font, self.text_color)
        presskey_rect.center = (int(self.settings.screen_width / 2),
                                int(self.settings.screen_height / 2) + 300)
        self.screen.blit(presskey_screen, presskey_rect)

        while self.check_for_keypress() is None:
            pygame.display.flip()
