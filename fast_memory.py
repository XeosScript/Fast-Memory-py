import os
from contextlib import contextmanager

class FastMemory:
    def __init__(self, folder, filename):
        self.filename = os.path.join(folder, filename)
        os.makedirs(folder, exist_ok=True)
        self.data = self.load()

    @classmethod
    def new(cls, folder_path, file_name):
        """Создает новый экземпляр FastMemory с заданным путем и именем файла."""
        instance = cls(folder_path, file_name)
        instance.save()
        return instance

    def load(self):
        """Читает данные из файла и возвращает их в виде словаря."""
        if not os.path.exists(self.filename):
            return {}
        with open(self.filename, 'r') as f:
            return dict(line.strip().split('=', 1) for line in f)

    def save(self):
        """Сохраняет текущие данные в файл."""
        with open(self.filename, 'w') as f:
            f.writelines(f"{key}={value}\n" for key, value in self.data.items())

    def set(self, key, value):
        """Устанавливает значение по ключу."""
        self.data[key] = value
        self.save()

    def get(self, key):
        """Возвращает значение по ключу."""
        return self.data.get(key)

    def delete(self, key):
        """Удаляет значение по ключу."""
        self.data.pop(key, None)
        self.save()

    def exists(self, key):
        """Проверяет, существует ли ключ."""
        return key in self.data

    def keys(self):
        """Возвращает список всех ключей."""
        return list(self.data.keys())

    def clear(self):
        """Удаляет все данные."""
        self.data.clear()
        self.save()

    @contextmanager
    def auto_clear(self):
        """Контекстный менеджер для автоматической очистки памяти при выходе."""
        try:
            yield self
        finally:
            self.clear()