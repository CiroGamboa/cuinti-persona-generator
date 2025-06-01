import json
import os
import tempfile
from pathlib import Path

import pytest
import yaml

from src.exporters.persona_exporter import PersonaExporter


@pytest.fixture
def sample_persona():
    """Sample persona data for testing."""
    return {
        "name": "John Doe",
        "age": 30,
        "occupation": "Software Engineer",
        "interests": ["coding", "reading", "hiking"],
        "location": {"city": "San Francisco", "country": "USA"},
    }


@pytest.fixture
def sample_personas():
    """Sample multiple personas data for testing."""
    return [
        {
            "name": "John Doe",
            "age": 30,
            "occupation": "Software Engineer",
            "interests": ["coding", "reading", "hiking"],
            "location": {"city": "San Francisco", "country": "USA"},
        },
        {
            "name": "Jane Smith",
            "age": 28,
            "occupation": "Data Scientist",
            "interests": ["machine learning", "yoga", "cooking"],
            "location": {"city": "New York", "country": "USA"},
        },
    ]


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test outputs."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield tmp_dir


@pytest.fixture
def expected_json_output():
    """Load expected JSON output from fixture file."""
    fixture_path = Path(__file__).parent / "fixtures" / "outputs" / "persona.json"
    with open(fixture_path) as f:
        return f.read()


@pytest.fixture
def expected_yaml_output():
    """Load expected YAML output from fixture file."""
    fixture_path = Path(__file__).parent / "fixtures" / "outputs" / "persona.yaml"
    with open(fixture_path) as f:
        return f.read()


def test_export_json(sample_persona, temp_dir):
    """Test exporting single persona to JSON format."""
    exporter = PersonaExporter(output_dir=temp_dir)
    output_path = exporter.export(sample_persona, "json")

    assert output_path.exists()
    assert output_path.suffix == ".json"

    with open(output_path) as f:
        data = json.load(f)
        assert "personas" in data
        assert len(data["personas"]) == 1
        assert data["personas"][0] == sample_persona


def test_export_multiple_json(sample_personas, temp_dir):
    """Test exporting multiple personas to JSON format."""
    exporter = PersonaExporter(output_dir=temp_dir)
    output_path = exporter.export_multiple(sample_personas, "json")

    assert output_path.exists()
    assert output_path.suffix == ".json"

    with open(output_path) as f:
        data = json.load(f)
        assert "personas" in data
        assert len(data["personas"]) == 2
        assert data["personas"] == sample_personas


def test_export_yaml(sample_persona, temp_dir):
    """Test exporting single persona to YAML format."""
    exporter = PersonaExporter(output_dir=temp_dir)
    output_path = exporter.export(sample_persona, "yaml")

    assert output_path.exists()
    assert output_path.suffix == ".yaml"

    with open(output_path) as f:
        data = yaml.safe_load(f)
        assert "personas" in data
        assert len(data["personas"]) == 1
        assert data["personas"][0] == sample_persona


def test_export_multiple_yaml(sample_personas, temp_dir):
    """Test exporting multiple personas to YAML format."""
    exporter = PersonaExporter(output_dir=temp_dir)
    output_path = exporter.export_multiple(sample_personas, "yaml")

    assert output_path.exists()
    assert output_path.suffix == ".yaml"

    with open(output_path) as f:
        data = yaml.safe_load(f)
        assert "personas" in data
        assert len(data["personas"]) == 2
        assert data["personas"] == sample_personas


def test_invalid_output_format(sample_persona, temp_dir):
    """Test that invalid output format raises ValueError."""
    exporter = PersonaExporter(output_dir=temp_dir)
    with pytest.raises(
        ValueError, match="Output format must be either 'json' or 'yaml'"
    ):
        exporter.export(sample_persona, "invalid_format")


def test_default_output_format(sample_persona, temp_dir):
    """Test that default output format is JSON."""
    exporter = PersonaExporter(output_dir=temp_dir)
    output_path = exporter.export(sample_persona)

    assert output_path.exists()
    assert output_path.suffix == ".json"

    with open(output_path) as f:
        data = json.load(f)
        assert "personas" in data
        assert len(data["personas"]) == 1
        assert data["personas"][0] == sample_persona


def test_custom_output_directory(sample_persona):
    """Test exporting to a custom output directory."""
    with tempfile.TemporaryDirectory() as custom_dir:
        exporter = PersonaExporter(output_dir=custom_dir)
        output_path = exporter.export(sample_persona)

        assert output_path.parent == Path(custom_dir)
        assert output_path.exists()

        with open(output_path) as f:
            data = json.load(f)
            assert "personas" in data
            assert len(data["personas"]) == 1
            assert data["personas"][0] == sample_persona


def test_file_permission_error(sample_persona, temp_dir):
    """Test handling of file permission errors."""
    exporter = PersonaExporter(output_dir=temp_dir)

    # Create a file that we can't write to
    output_path = Path(temp_dir) / "personas.json"
    output_path.touch()
    os.chmod(output_path, 0o444)  # Read-only

    with pytest.raises(Exception):
        exporter.export(sample_persona)

    # Clean up
    os.chmod(output_path, 0o666)
    output_path.unlink()


def test_nested_data_export(
    sample_persona, temp_dir, expected_json_output, expected_yaml_output
):
    """Test exporting persona with nested data structures."""
    exporter = PersonaExporter(output_dir=temp_dir)

    # Test JSON export
    json_path = exporter.export(sample_persona, "json")
    with open(json_path) as f:
        data = json.load(f)
        assert "personas" in data
        assert len(data["personas"]) == 1
        exported_persona = data["personas"][0]
        assert exported_persona["location"]["city"] == "San Francisco"
        assert exported_persona["interests"] == ["coding", "reading", "hiking"]

    # Test YAML export
    yaml_path = exporter.export(sample_persona, "yaml")
    with open(yaml_path) as f:
        data = yaml.safe_load(f)
        assert "personas" in data
        assert len(data["personas"]) == 1
        exported_persona = data["personas"][0]
        assert exported_persona["location"]["city"] == "San Francisco"
        assert exported_persona["interests"] == ["coding", "reading", "hiking"]
