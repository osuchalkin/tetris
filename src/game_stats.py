import time
import json


class GameStats():
    """Отслеживание статистики"""

    def __init__(self, tet_game):
        self.settings = tet_game.settings

        self.fall_speed = self.settings.fall_speed
        self.wait_time = self.settings.wait_time

        self.file_records = 'tet.json'
        self.records = {}

        self.reset_stats()
        self.game_active = False

    def calculate_level_and_fallfreq(self, level):
        """ вычисляет уровень и скорость падения фигур"""
        if level == 12:
            pass  # 12 уровень - последний, скорость больше не увеличивается
        else:
            now = time.time()
            if (now - self.begin_time) > self.wait_time:
                level += 1
                self.begin_time = time.time()
        fall_freq = self.fall_speed - (level * self.settings.scale_level)
        return level, fall_freq

    def reset_stats(self):
        """обновление статистики перед новой игрой"""
        self.begin_time = time.time()
        self.score = 0
        self.level = 1
        self.level, self.fall_freq = self.calculate_level_and_fallfreq(self.level)
        self.records = {}

    def save_record(self, name, score):
        """записываем рекорд в файл"""
        # добавляем запись в словарь
        self.records[name] = score
        # сортируем словарь
        sorted_dict = {}
        sorted_keys = sorted(self.records, key=self.records.get, reverse=True)
        for w in sorted_keys:
            sorted_dict[w] = self.records[w]
        # оставляем в словаре первые 30 значений
        if len(sorted_dict) > 30:
            key, value = sorted_dict.popitem()
        with open(self.file_records, "w") as f:
            json.dump(sorted_dict, f)

    def load_records(self):
        """загружаем файл рекордов"""
        try:
            with open(self.file_records, "r") as f:
                self.records = json.load(f)
        except FileNotFoundError:
            #  генератор - запись в словарь значений типа 'tetris-1': 0, 'tetris-2': 0 и т.д.
            self.records = {f'tetris-{str(index + 1)}': 0 for index in range(30)}
            """ то же самое обычным способом
            for index in range(30):
                index_str = f'tetris-{str(index + 1)}'
                self.records[index_str] = 0
                """
            with open(self.file_records, "w") as f:
                json.dump(self.records, f)
