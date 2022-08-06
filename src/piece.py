import pygame
import random


class Piece:
    """класс 1 блока"""

    def __init__(self, tet_game):
        """начальные значения для позиуии, состояния"""
        self.screen = tet_game.screen
        self.settings = tet_game.settings

        self.template_width = 5
        self.template_height = 5

        self.s_shape_template = [['.....',
                                  '.....',
                                  '..OO.',
                                  '.OO..',
                                  '.....'],
                                 ['.....',
                                  '..O..',
                                  '..OO.',
                                  '...O.',
                                  '.....']]

        self.z_shape_template = [['.....',
                                  '.....',
                                  '.OO..',
                                  '..OO.',
                                  '.....'],
                                 ['.....',
                                  '..O..',
                                  '.OO..',
                                  '.O...',
                                  '.....']]

        self.i_shape_template = [['..O..',
                                  '..O..',
                                  '..O..',
                                  '..O..',
                                  '.....'],
                                 ['.....',
                                  '.....',
                                  'OOOO.',
                                  '.....',
                                  '.....']]

        self.o_shape_template = [['.....',
                                  '.....',
                                  '.OO..',
                                  '.OO..',
                                  '.....']]

        self.j_shape_template = [['.....',
                                  '.O...',
                                  '.OOO.',
                                  '.....',
                                  '.....'],
                                 ['.....',
                                  '..OO.',
                                  '..O..',
                                  '..O..',
                                  '.....'],
                                 ['.....',
                                  '.....',
                                  '.OOO.',
                                  '...O.',
                                  '.....'],
                                 ['.....',
                                  '..O..',
                                  '..O..',
                                  '.OO..',
                                  '.....']]

        self.l_shape_template = [['.....',
                                  '...O.',
                                  '.OOO.',
                                  '.....',
                                  '.....'],
                                 ['.....',
                                  '..O..',
                                  '..O..',
                                  '..OO.',
                                  '.....'],
                                 ['.....',
                                  '.....',
                                  '.OOO.',
                                  '.O...',
                                  '.....'],
                                 ['.....',
                                  '.OO..',
                                  '..O..',
                                  '..O..',
                                  '.....']]

        self.t_shape_template = [['.....',
                                  '..O..',
                                  '.OOO.',
                                  '.....',
                                  '.....'],
                                 ['.....',
                                  '..O..',
                                  '..OO.',
                                  '..O..',
                                  '.....'],
                                 ['.....',
                                  '.....',
                                  '.OOO.',
                                  '..O..',
                                  '.....'],
                                 ['.....',
                                  '..O..',
                                  '.OO..',
                                  '..O..',
                                  '.....']]

        self.pieces = {'S': self.s_shape_template,
                       'Z': self.z_shape_template,
                       'J': self.j_shape_template,
                       'L': self.l_shape_template,
                       'I': self.i_shape_template,
                       'O': self.o_shape_template,
                       'T': self.t_shape_template}

        self.box_image_s = self._load_and_transform_image("images/blue.png")
        self.box_image_z = self._load_and_transform_image("images/orange.png")
        self.box_image_j = self._load_and_transform_image("images/purple.png")
        self.box_image_l = self._load_and_transform_image("images/yellow.png")
        self.box_image_i = self._load_and_transform_image("images/red.png")
        self.box_image_o = self._load_and_transform_image("images/dark_blue.png")
        self.box_image_t = self._load_and_transform_image("images/green.png")
        self.box_image_w = self._load_and_transform_image("images/white.png")

        self.images = {'S': self.box_image_s,
                       'Z': self.box_image_z,
                       'J': self.box_image_j,
                       'L': self.box_image_l,
                       'I': self.box_image_i,
                       'O': self.box_image_o,
                       'T': self.box_image_t}

        self.shape = random.choice(list(self.pieces.keys()))
        self.form = {'shape': self.shape,
                     'rotation': random.randint(0, len(self.pieces[self.shape]) - 1),
                     'x': int(self.settings.board_width / 2) - int(self.template_width / 2),
                     'y': -2,  # start it above the board (i.e. less than 0),
                     'image': self.shape  # random.randint(0, len(self.images)-1)
                     }

    def _load_and_transform_image(self, image):
        block_image = pygame.image.load(image)
        block_image = pygame.transform.scale(block_image, (40, 40))
        return block_image
