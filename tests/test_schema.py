from pathlib import Path
from typing import Any

from src.schemas.loader import SchemaLoader


def load_schema(schema_path: str) -> Any:
    """Load a YAML schema file."""
    schema_dir = str(Path(schema_path).parent)
    schema_name = Path(schema_path).stem
    loader = SchemaLoader(schema_dir=schema_dir)
    return loader.load_schema(schema_name)


def load_characteristics() -> Any:
    """Load the characteristics schema."""
    return load_schema("schemas/characteristics.yaml")


def load_default_schema() -> Any:
    """Load the default persona schema."""
    return load_schema("schemas/default_schema.yaml")


class TestSchemaValidation:
    """Test suite for schema validation."""

    def test_schema_structure(self):
        """Test that the schema has the correct structure."""
        schema = load_default_schema()
        required_fields = [
            "id",
            "first_name",
            "last_name",
            "age",
            "gender",
            "job_title",
            "bio",
            "visual_description",
        ]

        # Check top-level structure
        assert schema.name, "Schema name missing"
        assert schema.description, "Schema description missing"
        assert schema.version, "Schema version missing"
        assert schema.fields, "Fields dictionary missing"

        # Check required fields
        for field in required_fields:
            assert field in schema.fields, f"Required field {field} missing"
            assert schema.fields[field].type, f"Type missing for {field}"
            assert (
                schema.fields[field].required is not None
            ), f"Required flag missing for {field}"
            assert schema.fields[field].description, f"Description missing for {field}"

    def test_characteristics_mapping(self):
        """Test that all characteristics referenced in schema exist."""
        schema = load_default_schema()
        characteristics = load_characteristics()

        for field, field_data in schema.fields.items():
            if field_data.characteristics:
                for char_path in field_data.characteristics:
                    category, char = char_path.split(".")
                    msg = f"Category {category} not found in " "characteristics"
                    assert hasattr(characteristics, category), msg
                    category_chars = getattr(characteristics, category)
                    msg = f"Characteristic {char} not found in " f"{category}"
                    assert char in category_chars, msg

    def test_required_fields(self):
        """Test that required fields are properly marked."""
        schema = load_default_schema()
        required_fields = [
            "id",
            "first_name",
            "last_name",
            "age",
            "gender",
            "job_title",
            "bio",
            "visual_description",
        ]

        for field in required_fields:
            assert (
                schema.fields[field].required is True
            ), f"Field {field} should be required"

    def test_data_types(self):
        """Test that all fields have valid data types."""
        schema = load_default_schema()
        valid_types = ["string", "number", "boolean", "array", "object"]

        for field, field_data in schema.fields.items():
            msg = f"Invalid type {field_data.type} for field {field}"
            assert field_data.type in valid_types, msg

    def test_characteristic_examples(self):
        """Test that all characteristics have examples."""
        characteristics = load_characteristics()

        for category in ["personal", "professional", "physical", "personality"]:
            category_chars = getattr(characteristics, category)
            for char_name, char_data in category_chars.items():
                msg = f"Examples missing for {category}." f"{char_name}"
                assert char_data.examples, msg
                msg = f"No examples provided for {category}." f"{char_name}"
                assert len(char_data.examples) > 0, msg

    def test_characteristic_descriptions(self):
        """Test that all characteristics have descriptions."""
        characteristics = load_characteristics()

        for category in ["personal", "professional", "physical", "personality"]:
            category_chars = getattr(characteristics, category)
            for char_name, char_data in category_chars.items():
                msg = f"Description missing for {category}." f"{char_name}"
                assert char_data.description, msg
                msg = f"Empty description for {category}." f"{char_name}"
                assert len(char_data.description) > 0, msg

    def test_schema_characteristic_incorporation(self):
        """Test that characteristics are properly incorporated into fields."""
        schema = load_default_schema()

        # Test job_title characteristics
        assert schema.fields["job_title"].characteristics
        job_chars = schema.fields["job_title"].characteristics
        assert "professional.career_path" in job_chars
        assert "professional.education_level" in job_chars
        assert "professional.industry" in job_chars

        # Test bio characteristics
        assert schema.fields["bio"].characteristics
        bio_chars = schema.fields["bio"].characteristics
        assert "personal.religion" in bio_chars
        assert "personal.cultural_background" in bio_chars
        assert "personal.family_situation" in bio_chars
        assert "personality.life_goals" in bio_chars
        assert "personality.personal_values" in bio_chars
        assert "personality.hobbies" in bio_chars

        # Test visual_description characteristics
        assert schema.fields["visual_description"].characteristics
        visual_chars = schema.fields["visual_description"].characteristics
        assert "physical.height" in visual_chars
        assert "physical.body_type" in visual_chars
        assert "physical.fashion_style" in visual_chars
