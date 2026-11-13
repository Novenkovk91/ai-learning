"""Хук Claude Code: проверка синтаксиса .py-файла после Edit или Write.

Claude Code запускает этот скрипт сам (настройка в .claude/settings.json)
и передаёт на стандартный ввод JSON с описанием правки, например:
    {"tool_name": "Edit", "tool_input": {"file_path": "C:\\...\\day3_todo_cli.py", ...}}

Если файл — не .py, скрипт ничего не делает.
Если в .py-файле синтаксическая ошибка — печатает её в stderr и выходит с кодом 2:
для хука PostToolUse код 2 значит «покажи этот текст Claude, пусть исправит».
"""

import json                                # разбор JSON, который прислал Claude Code
import py_compile                          # стандартный модуль: компилирует файл и находит синтаксические ошибки
import sys                                 # stdin, stderr и код выхода

data = json.load(sys.stdin)                # читаем весь stdin и сразу превращаем JSON в словарь
file_path = data.get("tool_input", {}).get("file_path", "")   # путь к изменённому файлу; "" если его почему-то нет

if not file_path.endswith(".py"):          # проверяем только Python-файлы
    sys.exit(0)                            # код 0 — «всё хорошо, продолжай»

try:
    py_compile.compile(file_path, doraise=True)   # doraise=True — при ошибке бросить исключение, а не просто напечатать
except py_compile.PyCompileError as error:        # синтаксическая ошибка в файле
    print(f"Синтаксическая ошибка в {file_path}:\n{error.msg}", file=sys.stderr)   # file=sys.stderr — печать в поток ошибок
    sys.exit(2)                            # код 2 — Claude Code передаст текст из stderr модели
