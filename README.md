# Fast-memory-py 1.1

<p align="center">
  <a href="#ru">Русский</a> |
  <a href="#en">English</a>
</p>

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<h2 id="ru">🇷🇺 Русский</h2>

FastMemory — это легковесная библиотека для эффективной работы с данными в памяти. Главные принципы: простота, скорость и надёжность.

### ⚡ Особенности
- Простой текстовый формат хранения данных
- Потокобезопасные операции
- Поддержка TTL для записей
- Автоматическая очистка памяти
- Минимум зависимостей

### 📦 Установка

```python
# Создайте файл fast_memory.py и вставьте код класса FastMemory
from fast_memory import FastMemory as fm
```

### 🚀 Пример использования

```python
from fast_memory import FastMemory as fm

# Создание экземпляра
folder_path = 'data'
file_name = 'storage.fm'

with fm.new(folder_path, file_name).auto_clear() as memory:
    # Установка значений
    memory.set('name', 'Alice')
    memory.set('temp_key', 'value', ttl=3600)  # Истечет через час

    # Получение значений
    print(memory.get('name'))  # Alice

    # Проверка существования
    print(memory.exists('name'))  # True

    # Список ключей
    print(memory.keys())  # ['name', 'temp_key']
```

### 📚 Методы

- `new(folder_path, file_name)`: Создание нового экземпляра
- `set(key, value, ttl=None)`: Установка значения
- `get(key)`: Получение значения
- `delete(key)`: Удаление значения
- `exists(key)`: Проверка существования ключа
- `keys()`: Список всех ключей
- `clear()`: Очистка данных
- `auto_clear()`: Автоматическая очистка при выходе из контекста

---

<h2 id="en">🇬🇧 English</h2>

FastMemory is a lightweight library for efficient in-memory data management. Core principles: simplicity, speed, and reliability.

### ⚡ Features
- Simple text-based data storage
- Thread-safe operations
- TTL support for records
- Automatic memory cleanup
- Minimal dependencies

### 📦 Installation

```python
# Create fast_memory.py file and paste the FastMemory class code
from fast_memory import FastMemory as fm
```

### 🚀 Usage Example

```python
from fast_memory import FastMemory as fm

# Creating instance
folder_path = 'data'
file_name = 'storage.fm'

with fm.new(folder_path, file_name).auto_clear() as memory:
    # Setting values
    memory.set('name', 'Alice')
    memory.set('temp_key', 'value', ttl=3600)  # Expires in 1 hour

    # Getting values
    print(memory.get('name'))  # Alice

    # Checking existence
    print(memory.exists('name'))  # True

    # List of keys
    print(memory.keys())  # ['name', 'temp_key']
```

### 📚 Methods

- `new(folder_path, file_name)`: Create new instance
- `set(key, value, ttl=None)`: Set value
- `get(key)`: Get value
- `delete(key)`: Delete value
- `exists(key)`: Check key existence
- `keys()`: List all keys
- `clear()`: Clear data
- `auto_clear()`: Automatic cleanup when exiting context
