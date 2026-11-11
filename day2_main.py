import todo_utils                         # подключить весь модуль
from todo_utils import open_tasks         # или взять из него конкретную функцию

todo = [
    {"title": "Военкомат", "done": False},
    {"title": "РОХ", "done": True},
    {"title": "Агенты", "done": False, "owner": "Кир"},
]

for task in todo:
    print(todo_utils.format_task(task))   # обращение через имя модуля
print("Открытые:", open_tasks(todo))      # обращение напрямую

import json                               # формат JSON — язык обмена данными с API и ИИ
from datetime import date                 # даты
from pathlib import Path                  # работа с файлами и путями

# Сохранить список дел в файл JSON
Path("todo.json").write_text(json.dumps(todo, ensure_ascii=False, indent=2), encoding="utf-8")

# Прочитать обратно
loaded = json.loads(Path("todo.json").read_text(encoding="utf-8"))
print(f"Загружено задач: {len(loaded)}, сегодня {date.today()}")

print("--------------------------------")
print("Список решеных дел:", todo_utils.count_done(todo))
