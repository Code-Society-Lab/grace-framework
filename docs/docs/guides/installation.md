# Installation

## Prerequisites

Before beginning, ensure you have:

- Python 3.12+
- pip
- SQLite (default database, no setup needed)
    - PostgreSQL, MySQL, MariaDB, Oracle, and MS-SQL are also supported with configuration

## Virtual Environment

It is recommended to use a virtual environment to manage project dependencies.

### What is a Virtual Environment?

A virtual environment is an isolated Python environment that allows you to isolate the dependencies required by different projects from each other. This prevents version conflicts between projects and system tools.

### Create and Activate Your Virtual Environment

Using `venv`:

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

## Install Grace Framework

To install Grace Framework:

```bash
pip install grace-framework
```

### Installing from Source (For Development)

To install the development version:

=== "Linux/Windows"

    ```bash
    git clone https://github.com/Code-Society-Lab/grace-framework.git
    cd grace-framework
    pip install -e .[dev]
    ```

=== "macOS"

    ```bash
    git clone https://github.com/Code-Society-Lab/grace-framework.git
    cd grace-framework
    pip install -e ".[dev]"
    ```

## Next Steps

With Grace Framework installed, you're ready to [generate your first bot](creating-a-bot.md).
