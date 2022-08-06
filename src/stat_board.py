import pygame.font


class StatBoard():
    """вывод игровой статистики"""

    def __init__(self, tet_game):
        """инициализация атрибутов подсчета"""
        self.screen = tet_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = tet_game.settings
        self.stats = tet_game.stats
        # self.text = tet_game.text

        # Настройки шрифта для вывода счета.
        self.text_color = (255, 255, 85)
        self.records_color = (255, 85, 0)
        self.font = pygame.font.SysFont(None, (self.settings.screen_height // 10))
        self.font_records = pygame.font.SysFont(None, self.settings.screen_width // 40)
        # Подготовка исходного изображения.
        self.prep_score()
        self.prep_level()
        self.prep_records()

    def prep_score(self):
        """Преобразует текущий счет в графическое изображение."""
        # делаем пробел между сотнями и тысячами
        score_str = str(self.stats.score)
        if self.stats.score >= 1000:
            str_score = str(self.stats.score)
            thousands = str(self.stats.score // 1000)
            hundreds = str_score[len(str_score)-3 : len(str_score)+1]
            score_str = f'{thousands} {hundreds}'
        # создаем изображение
        self.score_image = self.font.render(score_str, True, self.text_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.center = (self.settings.x_margin / 2, self.settings.screen_height / 2 + (self.settings.screen_height / 10) * 3)

    def prep_level(self):
        """преобразование уровня в графическое изображение"""
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.center = (self.settings.x_margin / 2, self.settings.screen_height / 2 + self.settings.screen_height / 10)

    def prep_records(self):
        """вывод рекордов"""
        self.name_image = []
        self.name_rect = []
        self.result_image = []
        self.result_rect = []
        index = 0

        for name, value in self.stats.records.items():
            # name
            # чтобы выровнять 1 - 9
            if (index + 1) < 10:
                name = f' {index+1}    {name}'
            else:
                name = f'{index+1}   {name}'
            self.name_image.append(self.font_records.render(name, True, self.records_color))
            self.name_rect.append(self.name_image[index].get_rect())
            self.name_rect[index].left = (self.settings.screen_width - self.settings.x_margin) + self.settings.box_size
            self.name_rect[index].top = (self.settings.screen_height // 10) + index * (self.settings.screen_height // 34)
            # result
            # форматируем - отделяем тысячи от сотен
            result = str(value)
            if value >= 1000:
                str_value = str(value)
                thousands = str(value // 1000)
                hundreds = str_value[len(str_value) - 3: len(str_value) + 1]
                result = f'{thousands} {hundreds}'
            self.result_image.append(self.font_records.render(result, True, self.records_color))
            self.result_rect.append(self.result_image[index].get_rect())
            self.result_rect[index].left = (self.settings.screen_width - self.settings.x_margin) + (self.settings.screen_width //4)
            self.result_rect[index].top = (self.settings.screen_height // 10) + index * (self.settings.screen_height // 34)
        
            index += 1

    def show_score(self):
        """Выводит счет на экран."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.level_image, self.level_rect)

    def show_records(self):
        for index in range(len(self.stats.records)):
            self.screen.blit(self.name_image[index], self.name_rect[index])
            self.screen.blit(self.result_image[index], self.result_rect[index])

