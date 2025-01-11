# FastMemory 2.0 - Efficient In-Memory Data Store

## Introduction
FastMemory is a high-performance in-memory data store designed for fast and reliable data management. It provides a wide range of data structures and advanced features to meet the demands of modern applications.

## Key Features
- **Data Structures**: Supports various data structures such as strings, lists, sets, hashes, and sorted sets.
- **Caching**: Powerful caching mechanism with configurable eviction policies (LRU, LFU, TTL).
- **Transactions**: Optimistic locking and transaction support for atomic operations.
- **Indexing**: Efficient indexing and search capabilities for fast data retrieval.
- **Persistence**: Optional persistence to disk with automatic backup and restore.
- **Clustering**: Support for distributed deployments and data replication.
- **Monitoring**: Detailed statistics and monitoring capabilities.
- **Compression**: Efficient compression of large data values.
- **Serialization**: Support for various serialization formats (Pickle, MessagePack, JSON).

## Getting Started
To use FastMemory, simply install the library and start interacting with the data store:

```python
from fastmemory import FastMemory

fm = FastMemory()
fm.set('key', 'value')
value = fm.get('key')
```

## Data Structures

### Strings
- `set(key, value, ttl=None)`: Set a value for the given key with an optional TTL.
- `get(key, default=None)`: Retrieve the value for the given key.

### Lists
- `lpush(key, *values)`: Push one or more elements to the beginning of the list.
- `rpush(key, *values)`: Push one or more elements to the end of the list.
- `lpop(key)`: Pop an element from the beginning of the list.
- `rpop(key)`: Pop an element from the end of the list.

### Sets
- `sadd(key, *members)`: Add one or more members to the set.
- `srem(key, *members)`: Remove one or more members from the set.

### Hashes
- `hset(key, field, value)`: Set a field in the hash stored at key.
- `hget(key, field)`: Get the value of the specified field in the hash.

### Sorted Sets
- `zadd(key, *args, **kwargs)`: Add one or more members to the sorted set, or update the scores of members if they already exist.
- `zrange(key, start, end, desc=False, withscores=False)`: Return a range of members in the sorted set.
- `zrem(key, *members)`: Remove one or more members from the sorted set.

## Caching
FastMemory provides a powerful caching mechanism with configurable eviction policies. The available methods are:

- `cache_set(key, value, ttl=None, policy=None)`: Set a value in the cache with the selected policy.
- `cache_get(key, default=None)`: Retrieve a value from the cache.
- `cache_delete(key)`: Delete a key from the cache.

Eviction Policies:
- `lru`: Least Recently Used - evicts the least recently used keys.
- `lfu`: Least Frequently Used - evicts the least frequently used keys.
- `ttl`: Time To Live - evicts keys whose time-to-live has expired.

## Transactions and Optimistic Locking
FastMemory supports optimistic locking and transactions for atomic operations.

```python
with fm.transaction():
    fm.set('key1', 'value1')
    fm.set('key2', 'value2')
```

You can also track keys for optimistic locking:

```python
fm.watch('key1', 'key2')
# Perform operations dependent on the keys
fm.unwatch()
```

## Indexing and Search
FastMemory provides efficient indexing and search capabilities.

```python
fm.create_index('user_index', 'users:*', 'name')
user_keys = fm.search_by_index('user_index', 'John Doe')
```

Key features of indexing:
- Support for complex key patterns.
- Ability to index fields in hash tables.
- Efficient search using binary search.

## Persistence and Replication
FastMemory supports saving data to disk and replicating data between nodes.

```python
fm = FastMemory(persistence_path='/path/to/data')
fm.save_to_disk()
fm.load_from_disk()
```

For replicating data between nodes, use the `replicate_to` method:

```python
other_fm = FastMemory()
fm.replicate_to(other_fm)
```

Cluster mode allows automatic synchronization of data between all nodes:

```python
fm1 = FastMemory(cluster_mode=True)
fm2 = FastMemory(cluster_mode=True)
fm1.sync_cluster([fm1, fm2])
```

## Monitoring and Statistics
FastMemory provides detailed statistics and monitoring capabilities.

```python
stats = fm.get_stats()
print(stats)

for metrics in fm.monitor():
    print(metrics)
```

The available statistics include:
- Memory usage
- Operation counts
- Key information
- Caching statistics
- Priority queue and delayed task data

## Compression and Serialization
FastMemory supports efficient compression and various serialization formats.

```python
value = fm.compress_value('large_data')
decompressed = fm.decompress_value(value)

serialized = fm.serialize(data, format='msgpack')
deserialized = fm.deserialize(serialized, format='msgpack')
```

Supported serialization formats:
- Pickle
- MessagePack
- JSON

Compression is automatically applied for large values.

## Performance Optimizations
FastMemory utilizes several optimizations to achieve high performance:

- Efficient data structures: SortedDict, SortedList, deque
- Granular locking for individual keys
- Caching of hot keys and write buffering
- Usage of faster hash functions (xxhash, murmurhash)
- Adaptive indexing of most frequently accessed keys
- Compression of large values for memory savings

You can configure the optimization level when creating a FastMemory instance:

```python
fm = FastMemory(optimize_level=2)
```

Level 1 includes basic optimizations, while level 2 includes more advanced ones.

## API Reference

### `set(key, value, ttl=None)`
- **Description**: Set a value for the given key with an optional TTL (time-to-live).
- **Parameters**:
  - `key (str)`: The key to set the value for.
  - `value (Any)`: The value to set.
  - `ttl (float, optional)`: The time-to-live for the key in seconds (optional).
- **Returns**: `True` on successful operation, `False` otherwise.

### `get(key, default=None)`
- **Description**: Retrieve the value for the given key.
- **Parameters**:
  - `key (str)`: The key to retrieve the value for.
  - `default (Any, optional)`: The default value to return if the key is not found.
- **Returns**: The value for the specified key, or `default` if the key is not found.

[Add descriptions for the remaining methods]

## Usage Examples

### Using Strings
```python
fm.set('greeting', 'Hello, World!')
print(fm.get('greeting'))  # Output: 'Hello, World!'
```

### Working with Lists
```python
fm.lpush('numbers', 1, 2, 3)
fm.rpush('numbers', 4, 5)
print(fm.lrange('numbers', 0, -1))  # Output: [3, 2, 1, 4, 5]
```

[Add examples for other data structures and features]

I hope this helps you better understand and utilize the capabilities of FastMemory. If you have any questions or suggestions, please don't hesitate to reach out.

# FastMemory - Эффективное хранилище данных в памяти

## Введение
FastMemory - это высокопроизводительное хранилище данных в памяти, разработанное для быстрого и надежного управления данными. Оно предоставляет широкий спектр структур данных и расширенных функций для удовлетворения потребностей современных приложений.

## Быстрый старт
Для начала работы с FastMemory, установите библиотеку и создайте экземпляр:

```python
from fastmemory import FastMemory

fm = FastMemory()
fm.set('key', 'value')
value = fm.get('key')
```

## Структуры данных

### Строки
- `set(key, value, ttl=None)`: Установка значения для ключа с опциональным TTL.
- `get(key, default=None)`: Получение значения для ключа.

### Списки
- `lpush(key, *values)`: Добавление элементов в начало списка.
- `rpush(key, *values)`: Добавление элементов в конец списка.
- `lpop(key)`: Извлечение элемента с начала списка.
- `rpop(key)`: Извлечение элемента с конца списка.

### Множества
- `sadd(key, *members)`: Добавление элементов в множество.
- `srem(key, *members)`: Удаление элементов из множества.

### Хэши
- `hset(key, field, value)`: Установка поля в хэш-таблице.
- `hget(key, field)`: Получение значения поля из хэш-таблицы.

### Упорядоченные множества
- `zadd(key, *args, **kwargs)`: Добавление элементов с оценками в упорядоченное множество.
- `zrange(key, start, end, desc=False, withscores=False)`: Получение элементов из упорядоченного множества по индексу.
- `zrem(key, *members)`: Удаление элементов из упорядоченного множества.

## Кэширование
FastMemory предоставляет мощный механизм кэширования с настраиваемыми политиками вытеснения. Доступны следующие методы:

- `cache_set(key, value, ttl=None, policy=None)`: Установка значения в кэш с выбранной политикой.
- `cache_get(key, default=None)`: Получение значения из кэша.
- `cache_delete(key)`: Удаление ключа из кэша.

Политики вытеснения:
- `lru`: Least Recently Used - вытесняет наименее используемые ключи.
- `lfu`: Least Frequently Used - вытесняет наименее часто используемые ключи.
- `ttl`: Time To Live - вытесняет ключи, срок действия которых истек.

## Транзакции и блокировки
FastMemory поддерживает оптимистичную блокировку и транзакции для атомарных операций.

```python
with fm.transaction():
    fm.set('key1', 'value1')
    fm.set('key2', 'value2')
```

Для отслеживания ключей используются методы `watch` и `unwatch`:

```python
fm.watch('key1', 'key2')
# Выполнение операций, зависящих от ключей
fm.unwatch()
```

## Индексирование и поиск
FastMemory предоставляет возможность индексирования данных для быстрого поиска.

```python
fm.create_index('user_index', 'users:*', 'name')
user_keys = fm.search_by_index('user_index', 'John Doe')
```

Ключевые особенности индексирования:
- Поддержка сложных ключевых шаблонов.
- Возможность индексирования полей в хэш-таблицах.
- Эффективный поиск по индексам с использованием бинарного поиска.

## Постоянное хранение и репликация
FastMemory поддерживает сохранение данных на диск и репликацию между узлами.

```python
fm = FastMemory(persistence_path='/path/to/data')
fm.save_to_disk()
fm.load_from_disk()
```

Для репликации данных между узлами используется метод `replicate_to`:

```python
other_fm = FastMemory()
fm.replicate_to(other_fm)
```

Кластерный режим позволяет автоматически синхронизировать данные между всеми узлами:

```python
fm1 = FastMemory(cluster_mode=True)
fm2 = FastMemory(cluster_mode=True)
fm1.sync_cluster([fm1, fm2])
```

## Мониторинг и статистика
FastMemory предоставляет детальную статистику и возможности мониторинга.

```python
stats = fm.get_stats()
print(stats)

for metrics in fm.monitor():
    print(metrics)
```

Доступная статистика включает:
- Использование памяти
- Количество операций
- Информацию о ключах
- Статистику кэширования
- Данные о приоритетных очередях и отложенных задачах

## Сжатие и сериализация
FastMemory поддерживает эффективное сжатие и различные форматы сериализации.

```python
value = fm.compress_value('large_data')
decompressed = fm.decompress_value(value)

serialized = fm.serialize(data, format='msgpack')
deserialized = fm.deserialize(serialized, format='msgpack')
```

Форматы сериализации:
- Pickle
- MessagePack
- JSON

Сжатие данных выполняется автоматически для больших значений.

## Производительность и оптимизация
FastMemory использует ряд оптимизаций для достижения высокой производительности:

- Эффективные структуры данных: SortedDict, SortedList, deque
- Гранулярные блокировки для отдельных ключей
- Кэширование горячих ключей и буферизация операций
- Использование быстрых хеш-функций (xxhash, murmurhash)
- Адаптивное индексирование наиболее часто используемых ключей
- Сжатие больших значений для экономии памяти

Вы можете настроить уровень оптимизации при создании экземпляра FastMemory:

```python
fm = FastMemory(optimize_level=2)
```

Уровень 1 включает базовые оптимизации, а уровень 2 - более продвинутые.

## API Справочник

### `set(key, value, ttl=None)`
- **Описание**: Установка значения для ключа с опциональным TTL (время жизни).
- **Параметры**:
  - `key (str)`: Ключ, для которого устанавливается значение.
  - `value (Any)`: Значение, которое нужно установить.
  - `ttl (float, optional)`: Время жизни ключа в секундах (опционально).
- **Возвращает**: `True` в случае успешной операции, `False` в противном случае.

### `get(key, default=None)`
- **Описание**: Получение значения для ключа.
- **Параметры**:
  - `key (str)`: Ключ, значение которого нужно получить.
  - `default (Any, optional)`: Значение, которое будет возвращено, если ключ не найден.
- **Возвращает**: Значение для указанного ключа или `default`, если ключ не найден.

### `lpush(key, *values)`
- **Описание**: Добавление одного или нескольких элементов в начало списка.
- **Параметры**:
  - `key (str)`: Ключ списка, в который нужно добавить элементы.
  - `*values (Any)`: Один или несколько элементов, которые нужно добавить в начало списка.
- **Возвращает**: Длину списка после добавления элементов.

### `rpush(key, *values)`
- **Описание**: Добавление одного или нескольких элементов в конец списка.
- **Параметры**:
  - `key (str)`: Ключ списка, в который нужно добавить элементы.
  - `*values (Any)`: Один или несколько элементов, которые нужно добавить в конец списка.
- **Возвращает**: Длину списка после добавления элементов.

### `lpop(key)`
- **Описание**: Извлечение и удаление элемента с начала списка.
- **Параметры**:
  - `key (str)`: Ключ списка, из которого нужно извлечь элемент.
- **Возвращает**: Извлеченный элемент или `None`, если список пуст.

### `rpop(key)`
- **Описание**: Извлечение и удаление элемента с конца списка.
- **Параметры**:
  - `key (str)`: Ключ списка, из которого нужно извлечь элемент.
- **Возвращает**: Извлеченный элемент или `None`, если список пуст.

### `sadd(key, *members)`
- **Описание**: Добавление одного или нескольких элементов в множество.
- **Параметры**:
  - `key (str)`: Ключ множества, в которое нужно добавить элементы.
  - `*members (Any)`: Один или несколько элементов, которые нужно добавить в множество.
- **Возвращает**: Количество новых элементов, добавленных в множество.

### `srem(key, *members)`
- **Описание**: Удаление одного или нескольких элементов из множества.
- **Параметры**:
  - `key (str)`: Ключ множества, из которого нужно удалить элементы.
  - `*members (Any)`: Один или несколько элементов, которые нужно удалить из множества.
- **Возвращает**: Количество удаленных элементов.

### `hset(key, field, value)`
- **Описание**: Установка поля в хэш-таблице.
- **Параметры**:
  - `key (str)`: Ключ хэш-таблицы.
  - `field (str)`: Поле, которое нужно установить.
  - `value (Any)`: Значение, которое нужно установить для поля.
- **Возвращает**: `True` в случае успешной операции, `False` в противном случае.

### `hget(key, field)`
- **Описание**: Получение значения поля из хэш-таблицы.
- **Параметры**:
  - `key (str)`: Ключ хэш-таблицы.
  - `field (str)`: Поле, значение которого нужно получить.
- **Возвращает**: Значение поля или `None`, если поле не найдено.

### `zadd(key, *args, **kwargs)`
- **Описание**: Добавление одного или нескольких элементов с оценками в упорядоченное множество.
- **Параметры**:
  - `key (str)`: Ключ упорядоченного множества.
  - `*args`: Последовательность значений и оценок (значение1, оценка1, значение2, оценка2, ...).
  - `**kwargs`: Именованные аргументы в виде пар ключ-значение (значение=оценка, ...).
- **Возвращает**: Количество новых элементов, добавленных в множество.

### `zrange(key, start, end, desc=False, withscores=False)`
- **Описание**: Получение элементов из упорядоченного множества по индексу.
- **Параметры**:
  - `key (str)`: Ключ упорядоченного множества.
  - `start (int)`: Начальный индекс (включительно).
  - `end (int)`: Конечный индекс (включительно).
  - `desc (bool, optional)`: Флаг, указывающий на необходимость сортировки в обратном порядке.
  - `withscores (bool, optional)`: Флаг, указывающий на необходимость возврата оценок вместе со значениями.
- **Возвращает**: Список элементов (и оценок, если указан флаг `withscores`).

### `zrem(key, *members)`
- **Описание**: Удаление одного или нескольких элементов из упорядоченного множества.
- **Параметры**:
  - `key (str)`: Ключ упорядоченного множества.
  - `*members (Any)`: Один или несколько элементов, которые нужно удалить из множества.
- **Возвращает**: Количество удаленных элементов.

### `transaction()`
- **Описание**: Контекстный менеджер для выполнения транзакций.
- **Использование**:
  ```python
  with fm.transaction():
      fm.set('key1', 'value1')
      fm.set('key2', 'value2')
  ```
- **Пояснение**: Все операции, выполненные внутри блока `with`, будут обработаны как единая транзакция. Если возникнет исключение, все изменения будут отменены.

### `watch(*keys)`
- **Описание**: Отслеживание ключей для оптимистичной блокировки.
- **Параметры**:
  - `*keys (str)`: Один или несколько ключей, которые нужно отслеживать.
- **Использование**:
  ```python
  fm.watch('key1', 'key2')
  # Выполнение операций, зависящих от ключей
  fm.unwatch()
  ```
- **Пояснение**: Метод `watch` позволяет отслеживать изменения в указанных ключах. Если в процессе выполнения операций один из отслеживаемых ключей был изменен, транзакция будет отменена.

### `create_index(name, key_pattern, field)`
- **Описание**: Создание индекса для быстрого поиска.
- **Параметры**:
  - `name (str)`: Имя индекса.
  - `key_pattern (str)`: Шаблон ключей, которые нужно индексировать.
  - `field (str)`: Поле, по которому нужно индексировать.
- **Возвращает**: `True` в случае успешного создания индекса, `False` в противном случае.
- **Пояснение**: Индексы позволяют ускорить поиск данных по определенным критериям.

### `search_by_index(index_name, value)`
- **Описание**: Поиск ключей по индексу.
- **Параметры**:
  - `index_name (str)`: Имя индекса, по которому нужно выполнить поиск.
  - `value (Any)`: Значение, по которому нужно найти ключи.
- **Возвращает**: Множество ключей, соответствующих заданному значению.
- **Пояснение**: Метод позволяет быстро находить ключи, соответствующие определенному значению в индексируемом поле.

### `compress_value(value)`
- **Описание**: Сжатие значения.
- **Параметры**:
  - `value (Any)`: Значение, которое нужно сжать.
- **Возвращает**: Сжатое значение в виде байтов.
- **Пояснение**: Метод автоматически сжимает большие значения для экономии памяти.

### `decompress_value(value)`
- **Описание**: Распаковка сжатого значения.
- **Параметры**:
  - `value (bytes)`: Сжатое значение в виде байтов.
- **Возвращает**: Распакованное значение.
- **Пояснение**: Метод распаковывает значение, если оно было сжато ранее.

### `serialize(value, format='msgpack')`
- **Описание**: Сериализация значения.
- **Параметры**:
  - `value (Any)`: Значение, которое нужно сериализовать.
  - `format (str, optional)`: Формат сериализации ('msgpack', 'json' или 'pickle').
- **Возвращает**: Сериализованное значение в виде байтов.
- **Пояснение**: FastMemory поддерживает различные форматы сериализации для эффективной работы с данными.

### `deserialize(value, format='msgpack')`
- **Описание**: Десериализация значения.
- **Параметры**:
  - `value (bytes)`: Сериализованное значение в виде байтов.
  - `format (str, optional)`: Формат сериализации ('msgpack', 'json' или 'pickle').
- **Возвращает**: Десериализованное значение.
- **Пояснение**: Метод позволяет восстановить данные из сериализованного представления.

### `replicate_to(target)`
- **Описание**: Репликация данных на другой экземпляр FastMemory.
- **Параметры**:
  - `target (FastMemory)`: Экземпляр FastMemory, на который нужно выполнить репликацию.
- **Возвращает**: `True` в случае успешной репликации, `False` в противном случае.
- **Пояснение**: Метод позволяет реплицировать данные между экземплярами FastMemory для обеспечения отказоустойчивости и распределенной обработки.

### `sync_cluster(nodes)`
- **Описание**: Синхронизация данных между узлами кластера.
- **Параметры**:
  - `nodes (List[FastMemory])`: Список экземпляров FastMemory, входящих в кластер.
- **Возвращает**: `True` в случае успешной синхронизации, `False` в противном случае.
- **Пояснение**: Метод позволяет синхронизировать данные между всеми узлами кластера, обеспечивая согласованность данных.

### `get_stats()`
- **Описание**: Получение детальной статистики.
- **Возвращает**: Словарь с информацией о использовании памяти, количестве операций, ключей, кэше, очередях и отложенных задачах.
- **Пояснение**: Метод предоставляет подробную статистику о работе FastMemory, что помогает в мониторинге и диагностике.

### `monitor(interval=1)`
- **Описание**: Генератор для мониторинга метрик в реальном времени.
- **Параметры**:
  - `interval (int, optional)`: Интервал в секундах между генерацией метрик.
- **Возвращает**: Генератор, который периодически возвращает словарь с текущими метриками.
- **Пояснение**: Метод позволяет получать обновляемую статистику в режиме реального времени для мониторинга производительности.
