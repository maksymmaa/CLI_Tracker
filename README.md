# CLI Task Tracker

A command-line interface application built in Python for managing daily tasks, tracking strict deadlines, and analyzing personal productivity over time.

## Features
* **Task Logging:** Log completed tasks with their exact start and finish times.
* **Deadline Management:** Set active deadlines and automatically calculate the remaining time (e.g., `2d 5h 30m`).
* **Productivity Analytics (Smart Summary):** Automatically analyzes tasks from the past 7 days to determine the most productive day of the week based on total task duration.
* **Formatted Data Display:** Outputs data in clean, dynamically spaced ASCII tables for high readability in the console.
* **JSON Persistence:** Safely stores all task histories and active deadlines in local `.json` files to maintain state across sessions.

## Project Structure
The application logic is decoupled into manageable tools and separated from the data storage layer:

```text
CLI Tracker/
├── json_files/
│   ├── completed_tasks.json     # Local database for finished tasks (git-ignored)
│   └── deadline_tasks.json      # Local database for active deadlines (git-ignored)
├── tools/
│   ├── __init__.py              # Package initializer
│   ├── return_save.py           # Handles secure reading and loading of JSON data
│   └── tasks_tools.py           # Core logic for logging, time calculations, and table rendering
├── .gitignore                   # Safe-keeping rules for personal data and system files
├── LICENSE                      # Project distribution permissions
├── main.py                      # Central application controller and user interface loop
└── README.md                    # Project documentation
```

## Date Format Requirement
When entering dates into the console, strictly use the following format:
YYYY-MM-DD HH:MM:SS (e.g., 2026-06-03 14:30:00)

## Prerequisites
Python 3.10 or higher is required (uses match/case statements and advanced type hinting).

## How to Run
Clone the repository, navigate to the root directory, ensure the json_files directory exists, and execute:

```Bash
python main.py
