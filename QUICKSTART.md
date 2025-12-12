# Быстрый старт

## Установка

1. **Установите Python 3.7+** (если ещё не установлен)
   - Скачайте с https://www.python.org/
   - При установке отметьте "Add Python to PATH"

2. **Установите зависимости**
   
   Вариант А (автоматически):
   ```powershell
   setup.bat
   ```
   
   Вариант Б (вручную):
   ```powershell
   python -m pip install -r requirements.txt
   ```

## Использование

### Базовый запуск
```powershell
python config_lang_parser.py test_simple.conf
```

### Сохранить в файл
```powershell
python config_lang_parser.py test_simple.conf -o output.yaml
```

### Примеры из разных областей
```powershell
# Конфигурация веб-сервера
python config_lang_parser.py examples/webserver_config.conf

# Игровой персонаж
python config_lang_parser.py examples/game_character.conf

# Университетские курсы
python config_lang_parser.py examples/university_courses.conf
```

## Запуск тестов

### Простой способ
```powershell
run_tests.bat
```

### Вручную
```powershell
python -m pytest test_config_parser.py -v
```

### С покрытием кода
```powershell
python -m pytest test_config_parser.py --cov=config_lang_parser --cov-report=html
```

## Создание своей конфигурации

1. Создайте файл с расширением `.conf`
2. Используйте синтаксис:

```
; Комментарий
let константа = значение

{
  ключ => значение,
  число => 42,
  строка => @"текст",
  массив => [1, 2, 3],
  словарь => {x => 1, y => 2}
}
```

3. Запустите парсер:
```powershell
python config_lang_parser.py your_config.conf
```

## Справка по синтаксису

| Конструкция | Пример |
|-------------|--------|
| Число | `42`, `-15`, `0` |
| Строка | `@"Hello"` |
| Массив | `[1, 2, 3]` |
| Словарь | `{name => @"John", age => 30}` |
| Константа | `let x = 10` |
| Использование | `.(x).` |
| Комментарий | `; комментарий` |

## Устранение проблем

### Python не найден
```
Error: Python was not found
```
**Решение**: Установите Python и добавьте в PATH

### Модуль не найден
```
ModuleNotFoundError: No module named 'lark'
```
**Решение**: Запустите `python -m pip install -r requirements.txt`

### Ошибка синтаксиса
```
Error: Syntax error in configuration file
```
**Решение**: Проверьте синтаксис в конфигурационном файле

### Неопределенная константа
```
Error: Undefined constant: x
```
**Решение**: Объявите константу через `let x = значение` перед использованием

## Что дальше?

- Прочитайте полную документацию в `README.md`
- Изучите примеры в папке `examples/`
- Посмотрите тесты в `test_config_parser.py`
- Следуйте инструкции `GIT_SETUP.md` для публикации в Git
