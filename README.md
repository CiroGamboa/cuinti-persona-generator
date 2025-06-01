# Cuinti Persona Generator

A powerful and flexible tool for generating detailed, consistent, and diverse personas using AI models. The system is designed with a schema-based approach that allows for highly customizable persona generation while maintaining consistency through a centralized characteristics catalog.

## Key Features

- **Flexible Schema System**: Define custom persona structures using YAML schemas
- **Centralized Characteristics Catalog**: Single source of truth for persona traits and attributes
- **Type-Safe Generation**: Strict validation of data types and constraints
- **Diverse Output**: AI-powered generation of unique and varied personas
- **Extensible Design**: Easy to add new characteristics and schema definitions

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

## Project Structure

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

## Creating Custom Schemas

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

## Development

This project uses:
- Python 3.8+
- YAML for schema definitions
- pytest for testing

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

4. Use your new generator:
```python
from src.generators.my_custom_generator import MyCustomGenerator

generator = MyCustomGenerator(
    schema_path="schemas/my_schema.yaml",
    config_path="config/my_model_config.yaml",
    model_specific_param="value"
)

persona = generator.generate()
```

### Example: OpenAI Generator

The included OpenAI generator demonstrates how to implement a model-specific generator:

```python
class OpenAIGenerator(BaseGenerator):
    def __init__(self, schema_path=None, config_path=None, model="gpt-4"):
        super().__init__(schema_path, config_path)
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model

    def generate(self, prompt=None):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self._get_system_prompt()},
                {"role": "user", "content": self._get_user_prompt(prompt)}
            ]
        )
        return json.loads(response.choices[0].message.content)
```

### Best Practices

When implementing a new generator:

1. **Schema Compliance**: Ensure your generator always returns data that matches the schema structure
2. **Error Handling**: Implement robust error handling for API calls and response parsing
3. **Validation**: Use the base class validation or implement custom validation if needed
4. **Configuration**: Make your generator configurable through YAML config files
5. **Documentation**: Document any model-specific parameters and requirements

## License

MIT License
