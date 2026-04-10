import json
import os
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

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
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def list_internships(data):
    table = Table(title="Internship Hunt Tracker")
    table.add_column("ID", style="cyan")
    table.add_column("Company", style="bold white")
    table.add_column("Position")
    table.add_column("Status", justify="center")

    sorted_data = sorted(data, key=lambda x: x["status"])

    for i, item in enumerate(sorted_data):
        status_color = (
            "green"
            if "OFFER" in item["status"]
            else "red"
            if "DENIED" in item["status"]
            else "yellow"
            if "SENT" in item["status"]
            else "blue"
        )

        table.add_row(
            str(i),
            item["company"],
            item["position"],
            f"[{status_color}]{item['status']}[/{status_color}]",
        )

    console.print(table)


def add_internship(data):
    company = console.input("[bold green]Company name:[/bold green] ")
    pos = console.input("[bold green]Position:[/bold green] ")
    console.print("Statuses: " + " | ".join([f"{k}: {v}" for k, v in STATUSES.items()]))
    choice = console.input("Choose status (default 1): ") or "1"

    data.append({
        "company": company,
        "position": pos,
        "status": STATUSES.get(choice, STATUSES["1"]),
    })
    save_data(data)
    console.print("[bold cyan]Added![/bold cyan]")


def main():
    data = load_data()
    while True:
        console.clear()
        list_internships(data)
        console.print("\n[bold]Actions:[/bold] (a)dd | (u)pdate | (d)elete | (q)uit")
        cmd = console.input(">>> ").lower()

        if cmd == "a":
            add_internship(data)
        elif cmd == "u":
            idx = int(console.input("Enter ID to update: "))
            console.print(
                "New statuses: "
                + " | ".join([f"{k}: {v}" for k, v in STATUSES.items()])
            )
            choice = console.input("New status: ")
            data[idx]["status"] = STATUSES.get(choice, data[idx]["status"])
            save_data(data)
        elif cmd == "d":
            idx = int(console.input("Enter ID to delete: "))
            data.pop(idx)
            save_data(data)
        elif cmd == "q":
            break


if __name__ == "__main__":
    main()
