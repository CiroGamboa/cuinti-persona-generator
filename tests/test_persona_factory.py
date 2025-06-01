import json
import tempfile
from pathlib import Path

import pytest
import yaml

from src.factories.persona_factory import PersonaFactory


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test outputs."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield tmp_dir


@pytest.fixture
def factory(temp_dir):
    """Create a PersonaFactory instance with test configuration."""
    return PersonaFactory(
        schema_path="tests/fixtures/schemas/test_schema.yaml", output_dir=temp_dir
    )


def test_factory_initialization(factory):
    """Test factory initialization with default parameters."""
    assert factory.schema_path == "tests/fixtures/schemas/test_schema.yaml"
    assert factory.output_format == "json"
    assert isinstance(factory.output_dir, Path)


def test_factory_initialization_with_custom_params(temp_dir):
    """Test factory initialization with custom parameters."""
    factory = PersonaFactory(
        schema_path="tests/fixtures/schemas/test_schema.yaml",
        output_format="yaml",
        output_dir=temp_dir,
    )
    assert factory.output_format == "yaml"
    assert factory.output_dir == Path(temp_dir)


def test_verify_connection(factory):
    """Test connection verification."""
    # This test might fail if OpenAI API key is not set
    # We'll mock this in integration tests
    assert isinstance(factory.verify_connection(), bool)


def test_generate_personas(factory):
    """Test persona generation."""
    num_personas = 2
    personas = factory.generate_personas(num_personas)

    assert len(personas) == num_personas
    for persona in personas:
        assert isinstance(persona, dict)
        # Check required fields from test schema
        assert "id" in persona
        assert "name" in persona
        assert "age" in persona
        assert "background" in persona
        assert "professional" in persona
        assert "appearance" in persona


def test_export_personas_json(factory):
    """Test exporting personas in JSON format."""
    personas = [
        {"id": "1", "name": "Test Person 1", "age": 30},
        {"id": "2", "name": "Test Person 2", "age": 25},
    ]

    output_path = factory.export_personas(personas, filename_prefix="test_persona")

    assert output_path.exists()
    assert output_path.suffix == ".json"
    with open(output_path) as f:
        data = json.load(f)
        assert "personas" in data
        assert len(data["personas"]) == 2
        assert data["personas"][0]["id"] == "1"
        assert data["personas"][1]["id"] == "2"


def test_export_personas_yaml(temp_dir):
    """Test exporting personas in YAML format."""
    factory = PersonaFactory(
        schema_path=("tests/fixtures/schemas/test_schema.yaml"),
        output_format="yaml",
        output_dir=temp_dir,
    )

    personas = [
        {"id": "1", "name": "Test Person 1", "age": 30},
        {"id": "2", "name": "Test Person 2", "age": 25},
    ]

    output_path = factory.export_personas(personas, filename_prefix="test_persona")

    assert output_path.exists()
    assert output_path.suffix == ".yaml"
    with open(output_path) as f:
        data = yaml.safe_load(f)
        assert "personas" in data
        assert len(data["personas"]) == 2
        assert data["personas"][0]["id"] == "1"
        assert data["personas"][1]["id"] == "2"


def test_generate_and_export(factory):
    """Test combined generation and export functionality."""
    num_personas = 2
    output_path = factory.generate_and_export(
        num_personas, filename_prefix="test_persona"
    )

    assert output_path.exists()
    with open(output_path) as f:
        data = json.load(f)
        assert "personas" in data
        assert len(data["personas"]) == num_personas
