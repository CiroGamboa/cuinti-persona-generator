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
def temp_dir():
    """Create a temporary directory for test files."""
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


def test_export_json(sample_persona, temp_dir, expected_json_output):
    """Test exporting persona to JSON format."""
    exporter = PersonaExporter(output_dir=temp_dir)
    output_path = exporter.export(sample_persona, "json")

    assert output_path.exists()
    assert output_path.suffix == ".json"

    # Compare the actual output with the expected output
    with open(output_path) as f:
        actual_output = f.read()
        assert actual_output == expected_json_output

    # Also verify the data structure matches
    with open(output_path) as f:
        exported_data = json.load(f)
        assert exported_data == sample_persona


def test_export_yaml(sample_persona, temp_dir, expected_yaml_output):
    """Test exporting persona to YAML format."""
    exporter = PersonaExporter(output_dir=temp_dir)
    output_path = exporter.export(sample_persona, "yaml")

    assert output_path.exists()
    assert output_path.suffix == ".yaml"

    # Compare the actual output data structure with the expected output data structure
    with open(output_path) as f:
        exported_data = yaml.safe_load(f)
    fixture_path = Path(__file__).parent / "fixtures" / "outputs" / "persona.yaml"
    with open(fixture_path) as f:
        expected_data = yaml.safe_load(f)
    assert exported_data == expected_data
    assert exported_data == sample_persona


def test_invalid_output_format(sample_persona, temp_dir):
    """Test that invalid output format raises ValueError."""
    exporter = PersonaExporter(output_dir=temp_dir)
    with pytest.raises(
        ValueError, match="Output format must be either 'json' or 'yaml'"
    ):
        exporter.export(sample_persona, "invalid_format")


def test_default_output_format(sample_persona, temp_dir, expected_json_output):
    """Test that default output format is JSON."""
    exporter = PersonaExporter(output_dir=temp_dir)
    output_path = exporter.export(sample_persona)

    assert output_path.exists()
    assert output_path.suffix == ".json"

    # Verify the output matches the expected format
    with open(output_path) as f:
        actual_output = f.read()
        assert actual_output == expected_json_output


def test_custom_output_directory(sample_persona, expected_json_output):
    """Test exporting to a custom output directory."""
    with tempfile.TemporaryDirectory() as custom_dir:
        exporter = PersonaExporter(output_dir=custom_dir)
        output_path = exporter.export(sample_persona)

        assert output_path.parent == Path(custom_dir)
        assert output_path.exists()

        # Verify the output matches the expected format
        with open(output_path) as f:
            actual_output = f.read()
            assert actual_output == expected_json_output


def test_file_permission_error(sample_persona, temp_dir):
    """Test handling of file permission errors."""
    exporter = PersonaExporter(output_dir=temp_dir)

    # Create a file that we can't write to
    output_path = Path(temp_dir) / "persona.json"
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
        actual_json = f.read()
        assert actual_json == expected_json_output
    with open(json_path) as f:
        json_data = json.load(f)
        assert json_data["location"]["city"] == "San Francisco"
        assert json_data["interests"] == ["coding", "reading", "hiking"]

    # Test YAML export
    yaml_path = exporter.export(sample_persona, "yaml")
    with open(yaml_path) as f:
        exported_data = yaml.safe_load(f)
    fixture_path = Path(__file__).parent / "fixtures" / "outputs" / "persona.yaml"
    with open(fixture_path) as f:
        expected_data = yaml.safe_load(f)
    assert exported_data == expected_data
    assert exported_data["location"]["city"] == "San Francisco"
    assert exported_data["interests"] == ["coding", "reading", "hiking"]
