from rich.console import Console
from rich.table import Table

from todo_utils import open_tasks

todo = [
    {"title": "Военкомат", "done": False},
    {"title": "РОХ", "done": True},
    {"title": "Агенты", "done": False, "owner": "Кир"},
]

table = Table(title="Мои дела")
table.add_column("Статус")
table.add_column("Задача")
table.add_column("Ответственный")

for t in todo:
    table.add_row("✅" if t["done"] else "⬜", t["title"], t.get("owner", "-"))

console = Console()
console.print(table)
console.print(f"[bold red]Открытых задач: {len(open_tasks(todo))}[/bold red]")