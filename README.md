# Fast-memory-py
RU:

`FastMemory` — это простой и удобный класс для работы с данными в памяти, который позволяет сохранять и загружать данные в файл. Он поддерживает автоматическую очистку памяти и интуитивно понятный интерфейс.

## Установка

Для начала, убедитесь, что у вас установлен Python. Затем создайте файл `fast_memory.py` и вставьте в него код класса `FastMemory`.

## Импорт класса

Рекомендуется импортировать класс с использованием псевдонима для упрощения работы с ним:

```python
from fast_memory import FastMemory as fm
```

Это позволит вам использовать `fm` вместо полного имени `FastMemory`, что делает код более удобным и читаемым.

## Пример использования

Вот пример использования класса `FastMemory`:

```python
# example.py

from fast_memory import FastMemory as fm

# Создание нового экземпляра FastMemory
folder_path = 'C:/Users/nevil/OneDrive/Desktop/Fast memory'
file_name = 'data.fm'

# Используем метод new для создания экземпляра
with fm.new(folder_path, file_name).auto_clear() as memory:
    # Установка значений
    memory.set('name', 'Alice')
    memory.set('age', '30')

    # Получение значений
    print(memory.get('name'))  # Вывод: Alice
    print(memory.get('age'))   # Вывод: 30

    # Проверка наличия ключа
    print(memory.exists('age'))  # Вывод: True
    print(memory.exists('gender'))  # Вывод: False

    # Получение всех ключей
    print(memory.keys())  # Вывод: ['name', 'age']

# Здесь память автоматически очищена
print(memory.keys())  # Вывод: []
```

## Методы класса

- **`new(folder_path, file_name)`**: Создает новый экземпляр `FastMemory` с заданным путем к папке и именем файла. Файл будет создан автоматически, если он не существует.
  
- **`set(key, value)`**: Устанавливает значение по указанному ключу.

- **`get(key)`**: Возвращает значение по указанному ключу.

- **`delete(key)`**: Удаляет значение по указанному ключу.

- **`exists(key)`**: Проверяет, существует ли указанный ключ.

- **`keys()`**: Возвращает список всех ключей.

- **`clear()`**: Удаляет все данные.

- **`auto_clear()`**: Контекстный менеджер для автоматической очистки памяти при выходе из блока `with`.

## Автоматическая очистка памяти

Используя метод `auto_clear()`, вы можете гарантировать, что данные будут очищены после завершения работы с ними, что позволяет избежать переполнения памяти и защищает конфиденциальные данные.

EN:

`FastMemory` is a simple and convenient class for working with in-memory data, which allows you to save and load data to and from a file. It supports automatic memory clearing and an intuitive interface.

## Installation

First, ensure you have Python installed. Then create a file named `fast_memory.py` and paste the code of the `FastMemory` class into it.

## Importing the Class

It is recommended to import the class using an alias for easier use:

```python
from fast_memory import FastMemory as fm
```

This allows you to use `fm` instead of the full name `FastMemory`, making your code more convenient and readable.

## Example Usage

Here’s an example of how to use the `FastMemory` class:

```python
# example.py

from fast_memory import FastMemory as fm

# Creating a new FastMemory instance
folder_path = 'C:/Users/nevil/OneDrive/Desktop/Fast memory'
file_name = 'data.fm'

# Use the new method to create an instance
with fm.new(folder_path, file_name).auto_clear() as memory:
    # Setting values
    memory.set('name', 'Alice')
    memory.set('age', '30')

    # Getting values
    print(memory.get('name'))  # Output: Alice
    print(memory.get('age'))   # Output: 30

    # Checking for the existence of a key
    print(memory.exists('age'))  # Output: True
    print(memory.exists('gender'))  # Output: False

    # Getting all keys
    print(memory.keys())  # Output: ['name', 'age']

# Memory is automatically cleared here
print(memory.keys())  # Output: []
```

## Class Methods

- **`new(folder_path, file_name)`**: Creates a new instance of `FastMemory` with the specified folder path and filename. The file will be automatically created if it does not exist.
  
- **`set(key, value)`**: Sets a value for the specified key.

- **`get(key)`**: Returns the value for the specified key.

- **`delete(key)`**: Deletes the value for the specified key.

- **`exists(key)`**: Checks whether the specified key exists.

- **`keys()`**: Returns a list of all keys.

- **`clear()`**: Clears all data.

- **`auto_clear()`**: Context manager for automatically clearing memory upon exiting the `with` block.

## Automatic Memory Clearing

By using the `auto_clear()` method, you can ensure that your data will be cleared after you are done working with it, helping to prevent memory overflow and protecting sensitive information.
