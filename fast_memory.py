import os
import threading
from typing import Any, Dict, List, Optional, Union
from contextlib import contextmanager
from datetime import datetime

class FastMemory:
    def __init__(self, folder: str, filename: str):
        """
        Инициализация FastMemory.
        
        Args:
            folder (str): Путь к папке для хранения данных
            filename (str): Имя файла для хранения данных
        """
        self.filename = os.path.join(folder, filename)
        self.lock = threading.Lock()
        os.makedirs(folder, exist_ok=True)
        self.data: Dict[str, dict] = self.load()

    @classmethod
    def new(cls, folder_path: str, file_name: str) -> 'FastMemory':
        """
        Создает новый экземпляр FastMemory с заданным путем и именем файла.
        """
        instance = cls(folder_path, file_name)
        instance.save()
        return instance

    def load(self) -> Dict[str, Any]:
        """Читает данные из файла и возвращает их в виде словаря."""
        if not os.path.exists(self.filename):
            return {}
        
        with self.lock:
            data = {}
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    for line in f:
                        if '=' in line:
                            key, value = line.strip().split('=', 1)
                            # Проверяем TTL если он есть
                            if '||' in value:
                                val, expires = value.split('||')
                                if float(expires) > datetime.now().timestamp():
                                    data[key] = {
                                        'value': val,
                                        'expires_at': float(expires)
                                    }
                            else:
                                data[key] = {'value': value}
            except Exception:
                return {}
            return data

    def save(self) -> None:
        """Сохраняет текущие данные в файл."""
        with self.lock:
            with open(self.filename, 'w', encoding='utf-8') as f:
                for key, entry in self.data.items():
                    value = entry['value']
                    if 'expires_at' in entry:
                        value = f"{value}||{entry['expires_at']}"
                    f.write(f"{key}={value}\n")

    def set(self, key: str, value: str, ttl: Optional[int] = None) -> None:
        """
        Устанавливает значение по ключу.
        
        Args:
            key (str): Ключ
            value (str): Значение
            ttl (Optional[int]): Время жизни в секундах
        """
        with self.lock:
            entry = {'value': str(value)}
            if ttl is not None:
                entry['expires_at'] = datetime.now().timestamp() + ttl
            self.data[key] = entry
            self.save()

    def get(self, key: str, default: Any = None) -> Optional[str]:
        """
        Возвращает значение по ключу.
        """
        with self.lock:
            entry = self.data.get(key)
            if entry is None:
                return default

            if 'expires_at' in entry:
                if datetime.now().timestamp() > entry['expires_at']:
                    self.delete(key)
                    return default

            return entry['value']

    def delete(self, key: str) -> None:
        """Удаляет значение по ключу."""
        with self.lock:
            self.data.pop(key, None)
            self.save()

    def exists(self, key: str) -> bool:
        """Проверяет, существует ли ключ."""
        entry = self.data.get(key)
        if not entry:
            return False
            
        if 'expires_at' in entry:
            if datetime.now().timestamp() > entry['expires_at']:
                self.delete(key)
                return False
        return True

    def keys(self) -> List[str]:
        """Возвращает список всех действительных ключей."""
        return [key for key in self.data.keys() if self.exists(key)]

    def clear(self) -> None:
        """Удаляет все данные."""
        with self.lock:
            self.data.clear()
            self.save()

    def cleanup_expired(self) -> int:
        """
        Очищает просроченные записи.
        
        Returns:
            int: Количество удаленных записей
        """
        with self.lock:
            current_time = datetime.now().timestamp()
            expired_keys = [
                key for key, entry in self.data.items()
                if 'expires_at' in entry and current_time > entry['expires_at']
            ]
            
            for key in expired_keys:
                del self.data[key]
            
            if expired_keys:
                self.save()
            
            return len(expired_keys)

    def update(self, other_data: Dict[str, str]) -> None:
        """
        Обновляет несколько значений одновременно.
        
        Args:
            other_data (Dict[str, str]): Словарь с новыми данными
        """
        with self.lock:
            for key, value in other_data.items():
                self.set(key, value)

    @contextmanager
    def auto_clear(self):
        """Контекстный менеджер для автоматической очистки памяти при выходе."""
        try:
            yield self
        finally:
            self.clear()