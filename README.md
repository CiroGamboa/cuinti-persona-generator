# Persona Generator

A powerful and flexible tool for generating detailed, consistent, and diverse personas using AI models. The system is designed with a schema-based approach that allows for highly customizable persona generation while maintaining consistency through a centralized characteristics catalog.

## Table of Contents
- [Quick Start](#quick-start)
- [Key Features](#key-features)
- [Usage Guide](#usage-guide)
- [Schema System](#schema-system)
- [Characteristics Catalog](#characteristics-catalog)
- [Generator System](#generator-system)
- [Development Guide](#development-guide)

## Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/CiroGamboa/persona-generator.git
   cd persona-generator
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your environment:
   ```bash
   # Create a .env file in the project root
   echo "OPENAI_API_KEY=your_api_key_here" > .env
   ```

5. Generate your first persona:
   ```bash
   python main.py
   ```

## Key Features

- **Flexible Schema System**: Define custom persona structures using YAML schemas
- **Centralized Characteristics Catalog**: Single source of truth for persona traits and attributes
- **Type-Safe Generation**: Strict validation of data types and constraints
- **Diverse Output**: AI-powered generation of unique and varied personas
- **Extensible Design**: Easy to add new characteristics and schema definitions
- **Multiple AI Models**: Support for different AI models through a plugin system

## Usage Guide

### Basic Usage

Generate a single persona using the default schema:
```bash
python main.py
```

### Command Line Arguments

The generator supports several command-line arguments:

- `-n, --num-personas`: Number of personas to generate (default: 1)
- `-s, --schema`: Path to schema file (default: schemas/default_schema.yaml)
- `-c, --config`: Path to generator config file (default: src/generators/config/generator_config.yaml)
- `-f, --format`: Output format - json or yaml (default: json)
- `-o, --output-dir`: Directory for exported files (default: export)

### Usage Examples

1. Generate multiple personas:
```bash
python main.py --num-personas 3
```

2. Use a custom schema:
```bash
python main.py --schema schemas/example_schema.yaml
```

3. Export in YAML format:
```bash
python main.py --format yaml
```

4. Specify custom output directory:
```bash
python main.py --output-dir my_personas
```

5. Combine multiple options:
```bash
python main.py --num-personas 2 --schema schemas/example_schema.yaml --format yaml
```

### Example Output

The generator creates personas with rich, diverse characteristics. Here's an example output in JSON format:

```json
{
    "personas": [
        {
            "id": "P10423",
            "first_name": "Leonardo",
            "last_name": "Gomez",
            "age": "42",
            "gender": "Male",
            "job_title": "Fine Art Curator",
            "bio": "Born and raised in Spain, Leonardo moved to the US for further studies. Despite being an ardent Catholic, he appreciates all cultures and religions. Passionate about art history, he loves to explore art museums in his spare time. Leonardo's goal is to make art accessible to all and not just a privileged few. He's a single dad of one daughter whom he loves dearly and constantly draws inspiration from.",
            "visual_description": "Leonardo is of average height with a slender build. He's always seen in his signature casual look - faded jeans paired with a button-up shirt. Known for his expressive eyes and distinctive beard."
        }
    ]
}
```

## Schema System

The schema system is the core of the persona generator, allowing you to define exactly what fields and characteristics your personas should have. Each schema is defined in YAML and can include:

- Basic field definitions with types and constraints
- Required vs optional fields
- Field descriptions and validation rules
- Integration with the characteristics catalog

### Schema Structure

```yaml
name: "My Custom Schema"
description: "A custom schema for specific persona needs"
version: "1.0.0"
fields:
  field_name:
    type: string  # or number, boolean, array, object
    required: true
    description: "Field description"
    characteristics:  # Optional list of characteristics to incorporate
      - category.characteristic_name
```

### Field Types and Constraints

- **String**: Text fields with optional length constraints
- **Number**: Numeric values
- **Boolean**: True/false values
- **Array**: Lists of values
- **Object**: Nested structures

### Creating Custom Schemas

1. Start with the default schema or create a new YAML file
2. Define your fields and their types
3. Add characteristics from the catalog as needed
4. Use the schema with the generator

Example custom schema:
```yaml
name: "Professional Persona"
description: "Schema focused on professional attributes"
version: "1.0.0"
fields:
  name:
    type: string
    required: true
  role:
    type: string
    required: true
    characteristics:
      - professional.career_path
      - professional.industry
  skills:
    type: array
    required: true
    characteristics:
      - professional.technical_skills
      - professional.soft_skills
```

## Characteristics Catalog

The `characteristics.yaml` file serves as a single source of truth for all possible persona traits. It's organized into categories:

- **Personal**: Cultural background, family situation, religion
- **Professional**: Career path, education level, industry
- **Physical**: Height, body type, fashion style
- **Personality**: Life goals, personal values, hobbies

Each characteristic includes:
- Description of what it represents
- Example values or expressions
- Category grouping

### Using Characteristics

Characteristics can be referenced in schemas using dot notation:
```yaml
fields:
  bio:
    type: string
    characteristics:
      - personal.cultural_background
      - personality.life_goals
```

## Generator System

The persona generator system is designed with extensibility in mind, allowing you to easily add support for different AI models. The system uses a base generator class that defines the interface and common functionality, while specific implementations handle the interaction with different AI models.

### Architecture

The generator system consists of:

1. **BaseGenerator**: Abstract base class that defines:
   - Schema loading and validation
   - Configuration management
   - Common validation logic
   - Export functionality

2. **Model-Specific Generators**: Concrete implementations for different AI models:
   - OpenAIGenerator: Uses OpenAI's GPT models
   - (Your custom generator here)

### Adding a New AI Model

To add support for a new AI model:

1. Create a new generator class that inherits from `BaseGenerator`:
```python
from src.generators.base_generator import BaseGenerator

class MyCustomGenerator(BaseGenerator):
    def __init__(self, schema_path=None, config_path=None, **model_specific_params):
        super().__init__(schema_path, config_path)
        # Initialize your model-specific client/configuration
        
    def generate(self, prompt=None):
        # Implement the generation logic using your AI model
        # Return a dictionary matching the schema structure
```

2. Implement the required methods:
   - `generate()`: Core method that generates personas using your AI model
   - `validate()`: Optional override if you need custom validation

3. Add model-specific configuration:
```yaml
# config/my_model_config.yaml
prompts:
  system: |
    Your system prompt for the model
  user: |
    Your user prompt template
response:
  format: json
validation:
  strict_mode: true
```

### Best Practices

When implementing a new generator:

1. **Schema Compliance**: Ensure your generator always returns data that matches the schema structure
2. **Error Handling**: Implement robust error handling for API calls and response parsing
3. **Validation**: Use the base class validation or implement custom validation if needed
4. **Configuration**: Make your generator configurable through YAML config files
5. **Documentation**: Document any model-specific parameters and requirements

## Development Guide

### Project Structure

```
.
├── schemas/              # YAML schema definitions
│   ├── default_schema.yaml    # Default persona structure
│   ├── example_schema.yaml    # Example alternative schema
│   └── characteristics.yaml   # Master characteristics catalog
├── src/                 # Source code
│   ├── generators/      # AI model generators
│   ├── models/         # Data models
│   └── schemas/        # Schema handling
├── tests/              # Test suite
└── requirements.txt    # Project dependencies
```

### Development Requirements

- Python 3.8+
- YAML for schema definitions
- pytest for testing

### Running Tests

```bash
pytest tests/
```

## License

MIT License
