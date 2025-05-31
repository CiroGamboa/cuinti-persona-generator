# Cuinti Persona Generator

A tool for generating detailed and consistent personas using AI models.

## Project Structure

```
.
├── schemas/              # YAML schema definitions
│   ├── default_schema.yaml
│   ├── example_schema.yaml
│   └── characteristics.yaml
├── src/                 # Source code
│   ├── generators/      # AI model generators
│   ├── models/         # Data models
│   └── characteristics/ # Characteristic definitions
├── tests/              # Test suite
└── requirements.txt    # Project dependencies
```

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Development

This project uses:
- Python 3.8+
- YAML for schema definitions
- pytest for testing

## License

MIT License
