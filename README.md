# Python Project

This is a Python project with a proper testing setup.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- On macOS/Linux:
```bash
source venv/bin/activate
```
- On Windows:
```bash
.\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running Tests

To run the tests:
```bash
pytest
```

To run tests with coverage:
```bash
pytest --cov=src tests/
```

## Project Structure

```
.
├── src/            # Source code
├── tests/          # Test files
├── requirements.txt # Project dependencies
└── README.md       # This file
``` 