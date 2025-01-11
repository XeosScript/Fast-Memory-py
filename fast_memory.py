import time
import json
import pickle
import asyncio
import hashlib
import threading
import logging
import zlib
import msgpack
import ujson
import heapq
import sys
import array
import bisect
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict, Counter, deque
from typing import Any, Dict, List, Set, Optional, Union, Tuple, Callable, Generator, AsyncIterator
from threading import Lock, RLock
from datetime import datetime, timedelta
from contextlib import contextmanager
from functools import lru_cache, wraps
import mmh3  # Мурмур хеш - быстрее встроенного hash
from sortedcontainers import SortedDict, SortedList  # Для эффективной сортировки
import xxhash  # Ещё более быстрый хеш

# Оптимизированные структуры данных
@dataclass(slots=True)  # slots для уменьшения потребления памяти
class CacheEntry:
    value: Any
    expire_time: Optional[float]
    hits: int = 0
    last_access: float = time.time()

@dataclass(slots=True)
class QueueItem:
    priority: int
    data: Any
    timestamp: float = time.time()

class OptimizedSet:
    """Оптимизированное множество с быстрым поиском"""
    def __init__(self):
        self._data = array.array('Q')  # Используем array для экономии памяти
        self._hash_func = xxhash.xxh64()  # Быстрая хеш-функция

    def add(self, item: Any) -> None:
        h = self._hash_func.update(str(item).encode()).intdigest()
        if h not in self._data:
            bisect.insort(self._data, h)

    def remove(self, item: Any) -> None:
        h = self._hash_func.update(str(item).encode()).intdigest()
        idx = bisect.bisect_left(self._data, h)
        if idx < len(self._data) and self._data[idx] == h:
            self._data.pop(idx)

    def __contains__(self, item: Any) -> bool:
        h = self._hash_func.update(str(item).encode()).intdigest()
        idx = bisect.bisect_left(self._data, h)
        return idx < len(self._data) and self._data[idx] == h

class FastMemory:
    def __init__(self, 
                 persistence_path: Optional[str] = None,
                 max_memory: Optional[int] = None,
                 auto_cleanup: bool = True,
                 backup_interval: int = 3600,
                 log_level: str = 'INFO',
                 cluster_mode: bool = False,
                 compression: bool = False,
                 max_connections: int = 100,
                 cache_policy: str = 'lru',
                 max_cache_size: int = 1000,
                 optimize_level: int = 2):  # Новый параметр для уровня оптимизации

        # Оптимизированные структуры данных
        self._storage = SortedDict()  # Быстрый доступ и сортировка
        self._lists = defaultdict(deque)  # deque вместо list для O(1) вставки/удаления
        self._sets = defaultdict(OptimizedSet)  # Оптимизированные множества
        self._hashes = defaultdict(dict)
        self._sorted_sets = defaultdict(SortedList)  # Эффективная сортировка
        
        # Оптимизированные индексы
        self._indexes = defaultdict(lambda: SortedDict())
        self._reverse_indexes = defaultdict(set)
        
        # Кеш часто используемых значений
        self._hot_keys = SortedList(key=lambda x: (-x[1], x[0]))  # (key, hits)
        self._value_cache = {}  # Кеш для часто используемых значений
        
        # Оптимизация блокировок
        self._locks = defaultdict(RLock)  # Более гранулярные блокировки
        self._global_lock = RLock()
        
        # Буферы для batch операций
        self._write_buffer = deque(maxlen=1000)
        self._read_buffer = {}
        
        # Остальные атрибуты...
        self._ttl = SortedDict()  # Для быстрого поиска истекших ключей
        self._optimize_level = optimize_level
        
        # Инициализация оптимизаций
        self._setup_optimizations()

    def _setup_optimizations(self):
        """Настройка оптимизаций в зависимости от уровня"""
        if self._optimize_level >= 1:
            # Базовые оптимизации
            self._setup_key_prefetch()
            self._setup_value_compression()
            
        if self._optimize_level >= 2:
            # Продвинутые оптимизации
            self._setup_hot_keys_tracking()
            self._setup_adaptive_indexing()

    @lru_cache(maxsize=1000)
    def _get_lock(self, key: str) -> RLock:
        """Получение блокировки для конкретного ключа"""
        return self._locks[xxhash.xxh64(key.encode()).intdigest()]

    def set(self, key: str, value: Any, ttl: Optional[float] = None) -> bool:
        """Оптимизированная установка значения"""
        # Получаем блокировку для конкретного ключа
        with self._get_lock(key):
            # Буферизация записи
            self._write_buffer.append(('set', key, value, ttl))
            
            # Если буфер полон, применяем все изменения
            if len(self._write_buffer) >= self._write_buffer.maxlen:
                self._flush_write_buffer()
            
            # Обновляем горячие ключи
            self._update_hot_keys(key)
            
            # Быстрая установка значения
            self._storage[key] = value
            if ttl:
                self._ttl[key] = time.time() + ttl
                
            return True

    def get(self, key: str, default: Any = None) -> Any:
        """Оптимизированное получение значения"""
        # Проверяем кеш горячих ключей
        if key in self._value_cache:
            return self._value_cache[key]

        with self._get_lock(key):
            # Проверяем TTL
            if key in self._ttl and time.time() > self._ttl[key]:
                self._remove_expired_key(key)
                return default

            # Получаем значение
            value = self._storage.get(key, default)
            
            # Обновляем статистику использования
            self._update_hot_keys(key)
            
            # Кешируем часто используемые значения
            if self._is_hot_key(key):
                self._value_cache[key] = value
                
            return value

    def _update_hot_keys(self, key: str) -> None:
        """Обновление статистики горячих ключей"""
        for idx, (k, hits) in enumerate(self._hot_keys):
            if k == key:
                self._hot_keys.pop(idx)
                self._hot_keys.add((key, hits + 1))
                return
        self._hot_keys.add((key, 1))

    def _is_hot_key(self, key: str) -> bool:
        """Проверка, является ли ключ горячим"""
        return any(k == key and h > 100 for k, h in self._hot_keys)

    def _flush_write_buffer(self) -> None:
        """Применение буферизированных записей"""
        with self._global_lock:
            while self._write_buffer:
                op, *args = self._write_buffer.popleft()
                if op == 'set':
                    key, value, ttl = args
                    self._storage[key] = value
                    if ttl:
                        self._ttl[key] = time.time() + ttl

    def _remove_expired_key(self, key: str) -> None:
        """Оптимизированное удаление истекшего ключа"""
        self._storage.pop(key, None)
        self._ttl.pop(key, None)
        self._value_cache.pop(key, None)
        
        # Удаляем из индексов
        for index in self._reverse_indexes.get(key, set()):
            self._indexes[index].pop(key, None)
        self._reverse_indexes.pop(key, None)

    # Оптимизированные операции со списками
    def lpush(self, key: str, *values: Any) -> int:
        """Оптимизированное добавление в начало списка"""
        with self._get_lock(key):
            dq = self._lists[key]
            dq.extendleft(reversed(values))  # O(1) для каждого элемента
            return len(dq)

    def rpush(self, key: str, *values: Any) -> int:
        """Оптимизированное добавление в конец списка"""
        with self._get_lock(key):
            dq = self._lists[key]
            dq.extend(values)  # O(1) для каждого элемента
            return len(dq)

    # Оптимизированные операции с множествами
    def sadd(self, key: str, *members: Any) -> int:
        """Оптимизированное добавление в множество"""
        with self._get_lock(key):
            optimized_set = self._sets[key]
            original_size = len(optimized_set._data)
            for member in members:
                optimized_set.add(member)
            return len(optimized_set._data) - original_size

    def srem(self, key: str, *members: Any) -> int:
        """Оптимизированное удаление из множества"""
        with self._get_lock(key):
            optimized_set = self._sets[key]
            original_size = len(optimized_set._data)
            for member in members:
                optimized_set.remove(member)
            return original_size - len(optimized_set._data)

    # Оптимизированный поиск
    def search_by_index(self, index_name: str, value: Any) -> Set[str]:
        """Оптимизированный поиск по индексу"""
        # Используем быстрый хеш для поиска
        index = self._indexes[index_name]
        value_hash = xxhash.xxh64(str(value).encode()).intdigest()
        
        # Используем бинарный поиск
        start_idx = index.bisect_left(value_hash)
        end_idx = index.bisect_right(value_hash)
        
        return set(index.values()[start_idx:end_idx])

    # Оптимизированная сериализация
    def serialize(self, value: Any, format: str = 'msgpack') -> bytes:
        """Оптимизированная сериализация"""
        if format == 'msgpack':
            return msgpack.packb(value, use_bin_type=True)
        elif format == 'json':
            return ujson.dumps(value).encode()
        return pickle.dumps(value, protocol=pickle.HIGHEST_PROTOCOL)

    def deserialize(self, value: bytes, format: str = 'msgpack') -> Any:
        """Оптимизированная десериализация"""
        if format == 'msgpack':
            return msgpack.unpackb(value, raw=False)
        elif format == 'json':
            return ujson.loads(value.decode())
        return pickle.loads(value)

    # Оптимизированное сжатие
    def compress_value(self, value: Any) -> bytes:
        """Оптимизированное сжатие значения"""
        serialized = self.serialize(value)
        if len(serialized) > 1024:  # Сжимаем только большие значения
            return zlib.compress(serialized, level=1)  # Используем быстрое сжатие
        return serialized

    def decompress_value(self, value: bytes) -> Any:
        """Оптимизированная распаковка значения"""
        try:
            # Проверяем, сжаты ли данные
            if value.startswith(b'x\x9c'):  # Маркер сжатых данных zlib
                value = zlib.decompress(value)
            return self.deserialize(value)
        except Exception:
            return value

    # Оптимизированная очистка
    def _cleanup_expired(self) -> None:
        """Оптимизированная очистка устаревших данных"""
        current_time = time.time()
        
        # Используем бинарный поиск для нахождения истекших ключей
        expired_keys = []
        for key, expire_time in self._ttl.items():
            if expire_time <= current_time:
                expired_keys.append(key)
            else:
                break  # Благодаря сортировке можем остановиться
                
        # Пакетное удаление
        if expired_keys:
            with self._global_lock:
                for key in expired_keys:
                    self._remove_expired_key(key)