# --- Ошибка без обработки: программа падает ---
# number = int("abc")    # ValueError — раскомментируйте, чтобы увидеть


# --- try / except: «попробуй, а если ошибка — сделай вот это» ---
text = input("Сколько задач выполнено? ")

try:
    number = int(text)                     # пробуем превратить строку в число
    print(f"Отлично, выполнено: {number}")
except ValueError:                         # если не получилось — сюда
    print(f"'{text}' — это не число. Введите цифрами.")


# --- Несколько типов ошибок ---
task = {"title": "РОХ", "done": True}

try:
    print(task["owner"])                   # ключа нет → KeyError
except KeyError as error:                  # as error — сохранить ошибку в переменную
    print(f"Нет поля: {error}")


# --- else и finally ---
def safe_divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print("Делить на ноль нельзя")
        return None
    else:                                  # выполняется, если ошибки НЕ было
        return result
    finally:                               # выполняется ВСЕГДА
        print("Проверка деления завершена")
print(safe_divide(10, 2))
print("- - - - - - - - - - - - - - -- - - - - между вызовами")
print(safe_divide(10, 0))
print("- - - - - - - - - - - - - - -- - - - - после вызовов")

# --- Вызвать ошибку самому: raise ---
def set_owner(task: dict, owner: str) -> None:
    if owner not in ("Кир", "Шелл"):
        raise ValueError(f"Неизвестный ответственный: {owner}")
    task["owner"] = owner

try:
    set_owner(task, "Вася")
except ValueError as error:
    print(f"Ошибка: {error}")


print("- - - - - - - - - - - - - - -- - - - - ")
print("- - - - - - - - - - - - - - -- - - - - ")
print("- - - - - - - - - - - - - - -- - - - - ")


def ask_number() -> int:
    """Спрашивает число, пока пользователь не введёт его правильно."""
    while True:
        text = input("Введите число: ")
        try:
            return int(text)                  # получилось — return сразу выходит и из цикла, и из функции
        except ValueError:
            print("Это не число, попробуйте ещё раз.")


number = ask_number()
print(f"Вы ввели: {number}")