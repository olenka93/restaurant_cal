## Setup

1. Create and activate your Python virtual environment:

```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```

### Install Dependencies

Install all required Python packages with:

```bash
pip install -r requirements.txt
```

## Running the Flask App and Tests

This project uses a `Makefile` to simplify common commands.

### Run the Flask App

Start the Flask development server with:

```bash
make run
```

### RUN TESTS

```bash
make test
```
