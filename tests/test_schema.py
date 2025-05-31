from typing import Any, Dict

import yaml


def load_schema(schema_path: str) -> Dict[str, Any]:
    """Load a YAML schema file."""
    with open(schema_path, "r") as f:
        return yaml.safe_load(f)


def load_characteristics() -> Dict[str, Any]:
    """Load the characteristics schema."""
    return load_schema("schemas/characteristics.yaml")


def load_default_schema() -> Dict[str, Any]:
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

        for field in required_fields:
            assert field in schema, f"Required field {field} missing"
            assert "type" in schema[field], f"Type missing for {field}"
            assert "required" in schema[field], f"Required flag missing for {field}"
            assert "description" in schema[field], f"Description missing for {field}"

    def test_characteristics_mapping(self):
        """Test that all characteristics referenced in schema exist."""
        schema = load_default_schema()
        characteristics = load_characteristics()

        for field, field_data in schema.items():
            if "characteristics" in field_data:
                for char_path in field_data["characteristics"]:
                    category, char = char_path.split(".")
                    msg = f"Category {category} not found in characteristics"
                    assert category in characteristics, msg
                    msg = f"Characteristic {char} not found in {category}"
                    assert char in characteristics[category], msg

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
                schema[field]["required"] is True
            ), f"Field {field} should be required"

    def test_data_types(self):
        """Test that all fields have valid data types."""
        schema = load_default_schema()
        valid_types = ["string", "number", "boolean", "array", "object"]

        for field, field_data in schema.items():
            msg = f"Invalid type {field_data['type']} for field {field}"
            assert field_data["type"] in valid_types, msg

    def test_characteristic_examples(self):
        """Test that all characteristics have examples."""
        characteristics = load_characteristics()

        for category, chars in characteristics.items():
            for char_name, char_data in chars.items():
                msg = f"Examples missing for {category}.{char_name}"
                assert "examples" in char_data, msg
                msg = f"No examples provided for {category}.{char_name}"
                assert len(char_data["examples"]) > 0, msg

    def test_characteristic_descriptions(self):
        """Test that all characteristics have descriptions."""
        characteristics = load_characteristics()

        for category, chars in characteristics.items():
            for char_name, char_data in chars.items():
                msg = f"Description missing for {category}.{char_name}"
                assert "description" in char_data, msg
                msg = f"Empty description for {category}.{char_name}"
                assert len(char_data["description"]) > 0, msg

    def test_schema_characteristic_incorporation(self):
        """Test that characteristics are properly incorporated into fields."""
        schema = load_default_schema()

        # Test job_title characteristics
        assert "characteristics" in schema["job_title"]
        job_chars = schema["job_title"]["characteristics"]
        assert "professional.career_path" in job_chars
        assert "professional.education_level" in job_chars
        assert "professional.industry" in job_chars

        # Test bio characteristics
        assert "characteristics" in schema["bio"]
        bio_chars = schema["bio"]["characteristics"]
        assert "personal.religion" in bio_chars
        assert "personal.cultural_background" in bio_chars
        assert "personal.family_situation" in bio_chars
        assert "personality.life_goals" in bio_chars
        assert "personality.personal_values" in bio_chars
        assert "personality.hobbies" in bio_chars

        # Test visual_description characteristics
        assert "characteristics" in schema["visual_description"]
        visual_chars = schema["visual_description"]["characteristics"]
        assert "physical.height" in visual_chars
        assert "physical.body_type" in visual_chars
        assert "physical.fashion_style" in visual_chars
