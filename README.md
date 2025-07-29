# todoish

![Python](https://img.shields.io/badge/python-3.12+-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

**todoish** is a minimalist, command-line task manager written in pure Python. It was built to serve as a clear and practical example of clean software architecture for a technical talk on coding principles.

The primary goal of this project is not to be the most feature-rich to-do app, but to demonstrate how separating an application's concerns into distinct layers makes it more robust, maintainable, and easy to extend.

## The Core Philosophy: Scalable by Design

This project is intentionally architected into three layers to illustrate the **separation of concerns**. This design pattern is fundamental to building scalable software.

```
todoish/
├── main.py          # Presentation Layer (Handles user interaction)
├── task_manager.py  # Business Logic Layer (Defines application rules)
├── storage.py       # Data Layer (Handles reading/writing data)
└── tasks.json       # Data file (created automatically)
```

1.  **Presentation Layer (`main.py`):** This is the user-facing part of the application. Its only job is to parse commands from the terminal and display information back to the user. It knows *nothing* about how tasks are created or stored.

2.  **Business Logic Layer (`task_manager.py`):** This is the "brain" of the application. It contains all the rules about what a "task" is and what can be done with it (e.g., a task must have an ID, a description, and a status). It doesn't interact with the user or the persitence system directly.

3.  **Data Layer (`storage.py`):** This layer's sole responsibility is to handle data persistence. It provides simple functions to `load_tasks()` and `save_tasks()`. It doesn't know or care what the data represents.


## Core Functionality

*   **Task Creation:** Add new tasks to your to-do list. Each task is assigned a unique ID and a "pending" status by default.
*   **Task Viewing:** List all tasks, clearly displaying their ID, status (pending/completed), and description.
*   **Task Completion:** Mark any existing task as "completed" using its ID, allowing you to track your progress.
*   **Task Deletion:** Permanently remove a task from the list.
*   **Automatic Persistence:** All tasks are automatically saved to a local `tasks.json` file, ensuring your data is safe between sessions.

## Getting Started

### Prerequisites

*   Python 3.12 or higher
*   [uv](https://docs.astral.sh/uv/) - Python package and project manager

### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/farmisen/todoish.git
   cd todoish
   ```

2. Set up the development environment:
   ```sh
   ./make.sh setup
   ```
   This will:
   - Install `uv` if not already installed
   - Create a Python 3.12 virtual environment

3. Activate the virtual environment:
   ```sh
   # On Unix/macOS:
   source .venv/bin/activate
   
   # On Windows:
   .venv\Scripts\activate
   ```

4. Install the project with development dependencies:
   ```sh
   ./make.sh install-deps
   ```

5. Run the application:
   ```sh
   python main.py
   ```

## Development Tools

This project includes a comprehensive set of development tools accessible through `make.sh` (a wrapper around Make to ensure proper execution). All commands should be run from the project root.

### Available Commands

```bash
# Setup
./make.sh setup        # Install uv and create Python 3.12 virtual environment

# Install project with dev dependencies
./make.sh install-deps

# Code quality checks
./make.sh lint         # Run Ruff linter
./make.sh format       # Format code with Ruff
./make.sh format-check # Check code formatting without modifying files
./make.sh fix          # Auto-fix code issues (format + safe linting fixes)
./make.sh type-check   # Run Pyright type checker
./make.sh dev-check    # Run all checks (format-check, lint, type-check)

# Testing
./make.sh test         # Run pytest tests

# Cleanup
./make.sh clean        # Remove cache files
```

### Development Workflow

1. Make your changes
2. Run `./make.sh fix` to auto-fix formatting and linting issues
3. Run `./make.sh dev-check` to ensure all checks pass
4. Run `./make.sh test` to verify tests pass
5. Commit your changes

### Development Dependencies

The project uses the following development tools (installed automatically with `./make.sh install`):

- **Ruff**: Fast Python linter and formatter
- **Pyright**: Static type checker for Python
- **Pytest**: Testing framework
- **Pytest-cov**: Coverage plugin for pytest
- **Pydantic v2**: Data validation using Python type annotations

## License

This project is licensed under the MIT License.
