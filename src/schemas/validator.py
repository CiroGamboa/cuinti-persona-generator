from typing import Any, Dict

from src.models.characteristics import Characteristics
from src.models.schema import Schema


class SchemaValidator:
    """Validator for schema data."""

    @staticmethod
    def validate_schema(schema_data: Dict[str, Any]) -> Schema:
        """Validate schema data against the Schema model.

        Args:
            schema_data: Dictionary containing schema data

        Returns:
            Validated Schema object

        Raises:
            ValueError: If schema validation fails
        """
        try:
            return Schema(**schema_data)
        except Exception as e:
            raise ValueError(f"Schema validation failed: {e}")

    @staticmethod
    def validate_characteristics(
        characteristics_data: Dict[str, Any],
    ) -> Characteristics:
        """Validate characteristics data against the Characteristics model.

        Args:
            characteristics_data: Dictionary containing characteristics data

        Returns:
            Validated Characteristics object

        Raises:
            ValueError: If characteristics validation fails
        """
        try:
            return Characteristics(**characteristics_data)
        except Exception as e:
            raise ValueError(f"Characteristics validation failed: {e}")

    @staticmethod
    def validate_field_definition(field_data: Dict[str, Any]) -> bool:
        """Validate a field definition.

        Args:
            field_data: Dictionary containing field definition

        Returns:
            bool: True if the field definition is valid, False otherwise
        """
        required_keys = ["description", "type"]
        for key in required_keys:
            if key not in field_data:
                return False

        valid_types = ["string", "number", "boolean", "array", "object"]
        if field_data["type"] not in valid_types:
            return False

        return True
