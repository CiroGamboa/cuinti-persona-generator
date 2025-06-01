from pathlib import Path

import pytest

from src.generators.openai import OpenAIGenerator


@pytest.fixture
def default_generator():
    """Create a generator instance with default schema for testing."""
    return OpenAIGenerator(schema_path="schemas/default_schema.yaml")


@pytest.fixture
def test_generator():
    """Create a generator instance with test schema for testing."""
    schema_path = Path("tests/fixtures/schemas/test_schema.yaml")
    return OpenAIGenerator(schema_path=str(schema_path))


def test_openai_connection():
    """Test that we can connect to OpenAI API."""
    generator = OpenAIGenerator()
    assert generator.verify_access()


def test_generate_persona_with_default_schema():
    """Test generating a persona with the default schema."""
    generator = OpenAIGenerator(schema_path="schemas/default_schema.yaml")
    persona = generator.generate()
    assert persona is not None
    assert generator.validate(persona)


def test_generate_persona_with_test_schema(test_generator):
    """Test generating a persona with the test schema."""
    persona = test_generator.generate()
    assert persona is not None
    assert test_generator.validate(persona)


def test_generate_without_schema():
    """Test that generating without a schema raises an error."""
    generator = OpenAIGenerator()
    with pytest.raises(ValueError):
        generator.generate()


def test_validate_persona_with_default_schema():
    """Test validating a persona against the default schema."""
    generator = OpenAIGenerator(schema_path="schemas/default_schema.yaml")
    persona = generator.generate()
    assert generator.validate(persona)


def test_validate_persona_with_test_schema(test_generator):
    """Test validating a persona against the test schema."""
    persona = test_generator.generate()
    assert test_generator.validate(persona)


def test_schema_loading():
    """Test that generator can load different schema files."""
    # Test loading default schema
    schema_path = "schemas/default_schema.yaml"
    default_gen = OpenAIGenerator(schema_path=schema_path)
    assert default_gen.schema is not None, "Should load default schema"

    # Test loading test schema
    test_path = "tests/fixtures/schemas/test_schema.yaml"
    test_gen = OpenAIGenerator(schema_path=test_path)
    assert test_gen.schema is not None, "Should load test schema"

    # Test loading non-existent schema
    with pytest.raises(FileNotFoundError):
        OpenAIGenerator(schema_path="non_existent_schema.yaml")
