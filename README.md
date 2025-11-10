# ML Zoomcamp 2025 Midterm Project

## Setup

### Prerequisites
- Python 3.8 or higher
- uv (fast Python package installer)

### Install uv
If you don't have uv installed, install it using the official installer:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Initialize Virtual Environment
Create and activate a virtual environment using uv:

```bash
# Create a virtual environment
uv venv

# Activate the virtual environment
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate     # On Windows
```

### Install Dependencies
Install the project dependencies:

```bash
uv pip install -e .
```

