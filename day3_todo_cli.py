"""День 3: консольное приложение «список дел».

Запуск:
    python day3_todo_cli.py list          — показать все задачи
    python day3_todo_cli.py add "Текст"   — добавить задачу
    python day3_todo_cli.py done 2        — отметить задачу №2 выполненной
"""

import json                                # модуль для чтения и записи формата JSON
import sys                                 # модуль sys даёт доступ к аргументам командной строки
from pathlib import Path                   # Path — удобная работа с путями к файлам

from rich.console import Console           # Console — «умный» print из библиотеки rich
from rich.table import Table               # Table — таблица для красивого вывода

from todo_utils import count_done          # берём готовую функцию подсчёта из нашего модуля

# __file__ — путь к этому скрипту; .parent — папка, где он лежит
TODO_FILE = Path(__file__).parent / "todo.json"   # todo.json ищем рядом со скриптом, откуда бы ни запускали

console = Console()                        # один объект Console на всю программу — через него печатаем

USAGE = """Команды:
  list          — показать все задачи
  add "Текст"   — добавить задачу
  done N        — отметить задачу №N выполненной"""   # подсказка, которую покажем при неверной команде


def load_todo() -> list[dict]:             # функция возвращает список задач-словарей
    """Читает задачи из todo.json. Если файла нет — возвращает пустой список."""
    if not TODO_FILE.exists():             # файла ещё нет (например, самый первый запуск)
        return []                          # значит задач пока нет — пустой список
    text = TODO_FILE.read_text(encoding="utf-8")   # читаем весь файл как строку
    return json.loads(text)                # превращаем строку JSON в список словарей Python


def save_todo(todo: list[dict]) -> None:   # None — функция ничего не возвращает, только записывает
    """Записывает задачи в todo.json."""
    text = json.dumps(todo, ensure_ascii=False, indent=2)   # список → строка JSON; ensure_ascii=False сохраняет кириллицу как есть
    TODO_FILE.write_text(text, encoding="utf-8")            # записываем строку в файл (старое содержимое заменяется)


def show_list(todo: list[dict]) -> None:   # команда list
    """Печатает задачи таблицей."""
    if not todo:                           # пустой список в Python считается «ложью»
        console.print("Задач пока нет. Добавьте: add \"Текст\"")   # \" — кавычка внутри строки
        return                             # выходим из функции, таблицу не рисуем
    table = Table(title="Мои дела")        # создаём таблицу с заголовком
    table.add_column("№")                  # колонка с номером задачи
    table.add_column("Статус")             # колонка со значком выполнено / нет
    table.add_column("Задача")             # колонка с текстом задачи
    table.add_column("Ответственный")      # колонка с ответственным
    for number, task in enumerate(todo, start=1):   # enumerate даёт номер и элемент; нумерация с 1, как у людей
        status = "✅" if task["done"] else "⬜"     # короткая запись if/else в одну строку
        owner = task.get("owner", "-")              # .get вернёт "-", если поля owner нет
        table.add_row(str(number), status, task["title"], owner)   # в таблицу rich передаём строки, поэтому str(number)
    console.print(table)                   # печатаем готовую таблицу
    console.print(f"Выполнено: {count_done(todo)} из {len(todo)}")   # используем count_done из todo_utils


def add_task(todo: list[dict], title: str) -> None:   # команда add
    """Добавляет новую задачу и сохраняет файл."""
    title = title.strip()                  # strip убирает пробелы по краям текста
    if not title:                          # пустая строка тоже считается «ложью»
        console.print("[red]Текст задачи пустой — нечего добавлять.[/red]")   # [red]...[/red] — красный цвет в rich
        sys.exit(1)                        # завершаем программу с кодом 1 — так принято сообщать об ошибке
    todo.append({"title": title, "done": False})   # добавляем новый словарь в конец списка
    save_todo(todo)                        # сразу сохраняем, иначе изменение потеряется
    console.print(f"[green]Добавлена задача №{len(todo)}:[/green] {title}")   # номер новой задачи = длина списка


def mark_done(todo: list[dict], number_text: str) -> None:   # команда done
    """Отмечает задачу с номером number_text выполненной."""
    try:                                   # пробуем превратить текст в число
        number = int(number_text)          # "2" → 2; "abc" вызовет ошибку ValueError
    except ValueError:                     # если не получилось — попадаем сюда, программа не падает
        console.print(f"[red]'{number_text}' — это не номер. Укажите число, например: done 2[/red]")   # объясняем, что не так
        sys.exit(1)                        # выходим с кодом ошибки
    if number < 1 or number > len(todo):   # номера идут от 1 до количества задач
        console.print(f"[red]Задачи №{number} нет. Всего задач: {len(todo)}.[/red]")   # сообщаем, какие номера есть
        sys.exit(1)                        # выходим с кодом ошибки
    task = todo[number - 1]                # в списке счёт с 0, поэтому вычитаем 1
    if task["done"]:                       # задача уже была выполнена
        console.print(f"Задача №{number} «{task['title']}» уже выполнена.")   # просто сообщаем, ничего не меняем
        return                             # выходим из функции без сохранения
    task["done"] = True                    # меняем словарь прямо внутри списка
    save_todo(todo)                        # сохраняем изменение в файл
    console.print(f"[green]Готово:[/green] задача №{number} «{task['title']}» выполнена.")   # подтверждаем


def main() -> None:                        # главная функция: разбирает команду и вызывает нужное действие
    args = sys.argv[1:]                    # sys.argv[0] — имя скрипта, берём всё, что после него
    if not args:                           # команду вообще не указали
        console.print("[red]Не указана команда.[/red]")   # сообщаем об ошибке
        console.print(USAGE)               # показываем подсказку
        sys.exit(1)                        # выходим с кодом ошибки
    command = args[0]                      # первое слово — название команды
    try:                                   # файл мог сломаться, например, при ручной правке
        todo = load_todo()                 # читаем задачи из файла
    except json.JSONDecodeError:           # такую ошибку json выдаёт, если в файле не JSON
        console.print(f"[red]Файл {TODO_FILE.name} повреждён — это не JSON.[/red]")   # .name — только имя файла без папок
        sys.exit(1)                        # выходим с кодом ошибки
    if command == "list":                  # команда list
        show_list(todo)                    # показываем таблицу
    elif command == "add":                 # команда add; elif — как else if в C
        if len(args) < 2:                  # после add нет текста
            console.print("[red]Укажите текст задачи: add \"Текст\"[/red]")   # подсказываем, как правильно
            sys.exit(1)                    # выходим с кодом ошибки
        add_task(todo, " ".join(args[1:]))   # склеиваем слова через пробел — сработает даже без кавычек
    elif command == "done":                # команда done
        if len(args) < 2:                  # после done нет номера
            console.print("[red]Укажите номер задачи: done 2[/red]")   # подсказываем, как правильно
            sys.exit(1)                    # выходим с кодом ошибки
        mark_done(todo, args[1])           # передаём номер как текст — функция сама проверит его
    else:                                  # любая другая команда — неизвестная
        console.print(f"[red]Неизвестная команда: {command}[/red]")   # сообщаем, что именно не так
        console.print(USAGE)               # показываем подсказку
        sys.exit(1)                        # выходим с кодом ошибки


if __name__ == "__main__":                 # True, только если файл запущен напрямую, а не импортирован
    main()                                 # запускаем программу
