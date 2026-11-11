"""Функции для работы со списком дел."""


def format_task(task: dict) -> str:
    status = "✅" if task["done"] else "⬜"
    owner = task.get("owner", "-")
    return f"{status} {task['title']} ({owner})"


def open_tasks(todo: list[dict]) -> list[str]:
    return [t["title"] for t in todo if not t["done"]]
    
def count_done(todo: list[dict]) -> int:
    """Считает, сколько задач выполнено."""
    count = 0
    for item in todo:
        if item["done"]:
            count += 1
    return count