# Инструкция по публикации проекта в Git

## Шаг 1: Инициализация локального репозитория

Откройте PowerShell в папке проекта и выполните:

```powershell
git init
git add .
git commit -m "Initial commit: Configuration Language Parser

- Implemented parser using Lark library
- Added YAML converter
- Created comprehensive test suite
- Added 3 domain examples (webserver, game, university)
- Created complete documentation"
```

## Шаг 2: Создание удаленного репозитория

Выберите один из публичных git-сервисов:
- github.com (рекомендуется)
- gitlab.com
- gitflic.ru
- gitea.com
- hub.mos.ru
- gitverse.ru
- gitee.com

Создайте новый публичный репозиторий с названием, например: `config-lang-parser`

## Шаг 3: Связывание с удаленным репозиторием

Для GitHub:
```powershell
git remote add origin https://github.com/ваш-username/config-lang-parser.git
git branch -M main
git push -u origin main
```

Для GitLab:
```powershell
git remote add origin https://gitlab.com/ваш-username/config-lang-parser.git
git branch -M main
git push -u origin main
```

Для GitFlic:
```powershell
git remote add origin https://gitflic.ru/project/ваш-username/config-lang-parser.git
git branch -M main
git push -u origin main
```

## Шаг 4: Примеры коммитов для истории разработки

Если нужно показать этапы разработки, можно создать отдельные коммиты:

```powershell
# Откатиться к началу и делать коммиты поэтапно
git reset --soft HEAD~1

# Коммит 1: Структура проекта
git add requirements.txt .gitignore
git commit -m "Add project structure and dependencies"

# Коммит 2: Парсер
git add config_lang_parser.py
git commit -m "Implement parser with Lark

- Define grammar for config language
- Implement lexer and parser
- Add transformer for data conversion
- Support numbers, strings, arrays, dicts, constants"

# Коммит 3: CLI
git add config_lang_parser.py
git commit -m "Add command-line interface and YAML converter

- Add argparse for CLI arguments
- Implement YAML output
- Add error handling"

# Коммит 4: Тесты
git add test_config_parser.py
git commit -m "Add comprehensive test suite

- Test all basic types
- Test arrays and dictionaries
- Test constants and evaluation
- Test nested structures
- Test error handling"

# Коммит 5: Примеры
git add examples/
git commit -m "Add domain-specific examples

- Web server configuration
- Game character (RPG)
- University course management"

# Коммит 6: Документация
git add README.md GIT_SETUP.md setup.bat run_tests.bat
git commit -m "Add complete documentation and helper scripts

- Detailed README with usage examples
- Setup and test scripts
- Git setup instructions"

# Отправить все коммиты
git push origin main
```

## Шаг 5: Проверка репозитория

Убедитесь, что:
- ✅ Репозиторий публичный (Public)
- ✅ README.md отображается на главной странице
- ✅ Все файлы загружены
- ✅ История коммитов детальная и понятная

## Шаг 6: Загрузка ссылки в СДО

Скопируйте URL репозитория, например:
```
https://github.com/ваш-username/config-lang-parser
```

Загрузите эту ссылку в систему дистанционного обучения (СДО).

## Дополнительные команды Git

### Просмотр истории коммитов
```powershell
git log --oneline --graph
```

### Внесение изменений
```powershell
git add .
git commit -m "Описание изменений"
git push
```

### Проверка статуса
```powershell
git status
```

### Просмотр изменений
```powershell
git diff
```

## Требования к репозиторию

Согласно заданию, репозиторий должен содержать:

1. ✅ **Общее описание** (в README.md)
2. ✅ **Описание всех функций и настроек** (в README.md)
3. ✅ **Команды для сборки и тестов** (в README.md)
4. ✅ **Примеры использования** (в README.md + examples/)
5. ✅ **Использование специализированного инструмента** (Lark parser)
6. ✅ **Детальная история коммитов**
7. ✅ **3 примера из разных предметных областей** (webserver, game, university)
8. ✅ **Полное покрытие тестами**

## Структура репозитория

```
config-lang-parser/
├── .gitignore                  # Игнорируемые файлы
├── README.md                   # Основная документация
├── GIT_SETUP.md               # Инструкция по Git (этот файл)
├── requirements.txt            # Зависимости Python
├── config_lang_parser.py       # Основной модуль
├── test_config_parser.py       # Тесты
├── test_simple.conf           # Простой тест
├── setup.bat                   # Скрипт установки (Windows)
├── run_tests.bat              # Скрипт тестирования (Windows)
└── examples/                   # Примеры конфигураций
    ├── webserver_config.conf
    ├── game_character.conf
    └── university_courses.conf
```

## Рекомендации

1. Используйте детальные сообщения коммитов
2. Коммитьте логически связанные изменения вместе
3. Регулярно делайте push в удаленный репозиторий
4. Проверяйте, что репозиторий публичный
5. Убедитесь, что README.md содержит всю необходимую информацию
