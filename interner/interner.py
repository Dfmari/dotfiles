import json
import os
import sys
from rich.console import Console
from rich.table import Table

# ФИКС КОДИРОВКИ ДЛЯ WSL + PYTHON 3.14
# Мы заставляем систему жрать UTF-8 и заменять битые байты вместо краша
if hasattr(sys.stdin, "reconfigure"):
    sys.stdin.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

console = Console()
DATA_FILE = "internships.json"

STATUSES = {
    "1": "WIP ",
    "2": "SENT ",
    "3": "DENIED 󰯆",
    "4": "OFFER ",
    "5": "NOT OPENED ",
}


def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, UnicodeDecodeError):
            return []
    return []


def save_data(data):
    # Санитайзер: убираем суррогаты перед записью в JSON
    clean_data = []
    for item in data:
        clean_item = {}
        for k, v in item.items():
            if isinstance(v, str):
                # replace уберет битые символы, которые могли проскочить при вводе
                clean_item[k] = v.encode("utf-8", "replace").decode("utf-8")
            else:
                clean_item[k] = v
        clean_data.append(clean_item)

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(clean_data, f, indent=4, ensure_ascii=False)


def list_internships(data):
    if not data:
        console.print("[yellow]No internships in the database yet.[/yellow]")
        return

    table = Table(title="Internship Hunt Tracker")
    table.add_column("ID", style="cyan")
    table.add_column("Company", style="bold white")
    table.add_column("Position")
    table.add_column("Status", justify="center")

    # Сортировка по статусу
    sorted_data = sorted(data, key=lambda x: x["status"])

    for i, item in enumerate(sorted_data):
        st = item["status"]
        color = "white"
        if "OFFER" in st:
            color = "green"
        elif "DENIED" in st:
            color = "red"
        elif "SENT" in st:
            color = "yellow"
        elif "WIP" in st:
            color = "blue"

        table.add_row(
            str(i), item["company"], item["position"], f"[{color}]{st}[/{color}]"
        )

    console.print(table)


def add_internship(data):
    # Юзаем обычный input как fallback, если rich.console.input будет выделываться
    try:
        console.print("[bold green]Company name:[/bold green]", end=" ")
        company = sys.stdin.readline().strip()

        console.print("[bold green]Position:[/bold green]", end=" ")
        pos = sys.stdin.readline().strip()

        console.print(
            "Statuses: " + " | ".join([f"{k}: {v}" for k, v in STATUSES.items()])
        )
        console.print("Choose status (default 1):", end=" ")
        choice = sys.stdin.readline().strip() or "1"

        data.append({
            "company": company,
            "position": pos,
            "status": STATUSES.get(choice, STATUSES["1"]),
        })
        save_data(data)
        console.print("[bold cyan]Success! Added.[/bold cyan]")
    except Exception as e:
        console.print(f"[red]Error during input: {e}[/red]")


def main():
    data = load_data()
    while True:
        console.clear()
        list_internships(data)
        console.print("\n[bold]Actions:[/bold] (a)dd | (u)pdate | (d)elete | (q)uit")
        console.print(">>>", end=" ")

        try:
            cmd = sys.stdin.readline().strip().lower()
        except EOFError:
            break

        if cmd == "a":
            add_internship(data)
        elif cmd == "u":
            if not data:
                continue
            console.print("Enter ID to update:", end=" ")
            try:
                idx = int(sys.stdin.readline().strip())
                console.print(
                    "New statuses: "
                    + " | ".join([f"{k}: {v}" for k, v in STATUSES.items()])
                )
                choice = sys.stdin.readline().strip()
                data[idx]["status"] = STATUSES.get(choice, data[idx]["status"])
                save_data(data)
            except (ValueError, IndexError):
                console.print("[red]Invalid ID[/red]")
        elif cmd == "d":
            if not data:
                continue
            console.print("Enter ID to delete:", end=" ")
            try:
                idx = int(sys.stdin.readline().strip())
                data.pop(idx)
                save_data(data)
            except (ValueError, IndexError):
                console.print("[red]Invalid ID[/red]")
        elif cmd == "q":
            break


if __name__ == "__main__":
    main()
