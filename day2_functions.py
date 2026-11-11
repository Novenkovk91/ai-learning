# --- Объявление функции: def имя(параметры): ---
def greet(name):
    return f"Привет, {name}!"

print(greet("Кирилл"))  


# --- Параметр со значением по умолчанию ---
def format_task(title, done=False, owner="-"):
    status = "✅ DA" if done else "⬜ NET"
    return f"{status} {title} ({owner})"

# print(format_task("Военкомат"))                         # done и owner по умолчанию
# print(format_task("РОХ", done=True))                    # именованный аргумент
# print(format_task("Агенты", owner="Кир"))               # порядок не важен, если по имени


# --- Подсказки типов (type hints) и описание (docstring) ---
def count_done(todo: list[dict]) -> int:
    """Считает, сколько задач выполнено."""
    count = 0
    for item in todo:
        if item["done"]:
            count += 1
    return count

def open_tasks(todo: list[dict]) -> list:
    """Возвращает список невыполненных задач."""
    open_list = []
    for item in todo:
        if item["done"] == False:
            open_list.append(item["title"])
    return open_list

todo = [
    {"title": "Военкомат", "done": False},
    {"title": "РОХ", "done": True},
    {"title": "Агенты", "done": False, "owner": "Кир"},
]

for item in todo:
    print(format_task(item["title"], item["done"], item.get("owner", "-")))

print(f"Выполнено: {count_done(todo)} из {len(todo)}")
print("- - - - - -- - - - - - - - - - -- - - - -")
print("Невыполненные задачи:", open_tasks(todo))