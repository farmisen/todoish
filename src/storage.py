"""Data persistence layer for todoish task manager.

This module handles all file-based storage operations for tasks,
providing functions to load and save task data to JSON files.
"""

import json
from pathlib import Path
from typing import Any


def load_tasks() -> list[dict[str, Any]]:
    """Load tasks from the JSON file.

    Reads tasks from tasks.json in the application root directory.
    If the file doesn't exist, returns an empty list without raising an error.

    Returns:
        A list of task dictionaries. Each task contains:
        - id (int): Unique task identifier
        - description (str): Task description
        - status (str): Task status ("pending" or "completed")
    """
    tasks_file = Path("tasks.json")

    try:
        with open(tasks_file, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_tasks(tasks: list[dict[str, Any]]) -> None:
    """Save tasks to the JSON file.

    Writes the entire task list to tasks.json in the application root directory,
    overwriting any existing contents.

    Args:
        tasks: List of task dictionaries to save
    """
    tasks_file = Path("tasks.json")

    with open(tasks_file, "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=2, ensure_ascii=False)
