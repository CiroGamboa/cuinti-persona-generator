import pytest
import yaml

from src.generators.openai import OpenAIGenerator


@pytest.fixture
def default_generator():
    """Create a generator instance with default schema for testing."""
    return OpenAIGenerator(schema_path="schemas/default_schema.yaml")


@pytest.fixture
def test_generator():
    """Create a generator instance with test schema for testing."""
    return OpenAIGenerator(schema_path="tests/schemas/test_schema.yaml")


def test_openai_connection(default_generator):
    """Test that we can connect to OpenAI API."""
    assert default_generator.verify_access(), "Failed to connect to OpenAI API"


def test_generate_persona_with_default_schema(default_generator):
    """Test persona generation with default schema."""
    persona = default_generator.generate(
        prompt="Create a professional persona in the technology industry"
    )

    # Load schema to validate against
    with open("schemas/default_schema.yaml", "r") as f:
        schema = yaml.safe_load(f)

    # Basic validation using schema structure
    assert isinstance(persona, dict), "Generated persona should be a dict"

    # Check required fields
    for field, field_spec in schema.items():
        if field_spec.get("required", False):
            assert field in persona, f"Persona should have {field}"


def test_generate_persona_with_test_schema(test_generator):
    """Test persona generation with test schema."""
    persona = test_generator.generate(
        prompt="Create a professional persona in the technology industry"
    )

    # Load schema to validate against
    with open("tests/schemas/test_schema.yaml", "r") as f:
        schema = yaml.safe_load(f)

    # Validate basic structure
    assert isinstance(persona, dict), "Generated persona should be a dict"

    # Check direct fields
    for field, field_spec in schema.items():
        is_required = field_spec.get("required", False)
        is_not_object = field_spec.get("type") != "object"
        if is_required and is_not_object:
            assert field in persona, f"Persona should have {field}"

    # Check section fields
    for section, section_spec in schema.items():
        if section_spec.get("type") == "object" and section_spec.get("required", False):
            assert section in persona, f"Persona should have {section} section"

            # Check fields within section
            if "fields" in section_spec:
                for field_name, field_spec in section_spec["fields"].items():
                    if field_spec.get("required", False):
                        assert (
                            field_name in persona[section]
                        ), f"Section {section} should have {field_name}"


def test_generate_without_schema():
    """Test that generator raises error without schema."""
    generator = OpenAIGenerator()
    with pytest.raises(ValueError, match="Schema not loaded"):
        generator.generate()


def test_validate_persona_with_default_schema(default_generator):
    """Test persona validation against default schema."""
    # Load schema to create valid persona
    with open("schemas/default_schema.yaml", "r") as f:
        schema = yaml.safe_load(f)

    # Create valid persona based on schema
    valid_persona = {
        field: "test_value"
        for field, field_spec in schema.items()
        if field_spec.get("required", False)
    }
    valid_persona["id"] = "test-123"  # Add ID if required

    assert default_generator.validate(
        valid_persona
    ), "Valid persona should pass validation"

    # Invalid persona (missing required fields)
    invalid_persona = {"first_name": "John"}
    assert not default_generator.validate(
        invalid_persona
    ), "Invalid persona should fail validation"


def test_validate_persona_with_test_schema(test_generator):
    """Test persona validation against test schema."""
    # Create valid persona based on test schema structure
    valid_persona = {
        "id": "test-123",
        "name": "John Doe",
        "age": 30,
        "background": "Test background",
        "professional": {
            "role": "Software Engineer",
            "education": "Bachelor's in Computer Science",
            "skills": ["Python", "JavaScript"],
        },
        "appearance": {"description": "Tall and athletic", "style": "Business casual"},
    }

    assert test_generator.validate(
        valid_persona
    ), "Valid persona should pass validation"

    # Invalid persona (missing required section)
    invalid_persona = {"id": "test-123", "name": "John Doe", "age": 30}
    assert not test_generator.validate(
        invalid_persona
    ), "Invalid persona should fail validation"


def test_schema_loading():
    """Test that generator can load different schema files."""
    # Test loading default schema
    schema_path = "schemas/default_schema.yaml"
    default_gen = OpenAIGenerator(schema_path=schema_path)
    assert default_gen.schema is not None, "Should load default schema"

    # Test loading test schema
    test_gen = OpenAIGenerator(schema_path="tests/schemas/test_schema.yaml")
    assert test_gen.schema is not None, "Should load test schema"

    # Test loading non-existent schema
    with pytest.raises(FileNotFoundError):
        OpenAIGenerator(schema_path="non_existent_schema.yaml")
