# --- Простые типы ---
name = "Кирилл"          # str — строка
age = 35                 # int — целое число
rate = 4.5               # float — дробное
is_ready = True          # bool — True / False (с большой буквы!)
nothing = None           # None — «пусто», как NULL

print(type(name), type(age), type(rate), type(is_ready))

# --- Список (list): упорядоченный, изменяемый ---
tasks = ["Окружение", "Python"]
tasks.append("Claude Code")        # добавить в конец
print(tasks[0], tasks[-1])         # первый и последний элемент
print(len(tasks))                  # длина

# --- Словарь (dict): пары «ключ → значение» ---
task = {
    "title": "Купить доски",
    "where": "Леруа",
    "done": False,
}
print(task["title"])               # получить значение по ключу
task["done"] = True                # изменить
print(task)

# --- Список словарей: так выглядит почти любая «таблица» данных ---
todo = [
    {"title": "Военкомат", "done": False},
    {"title": "Вешалка", "done": False},
    {"title": "РОХ", "done": True},
    {"title": "Обучение_Агенты", "done": False, "owner": "Кир"},
]

for item in todo:
    status = "✅ da" if item["done"] else "⬜ net"
    owner = item.get("owner", "-")
    print(status, item["title"], owner) 
