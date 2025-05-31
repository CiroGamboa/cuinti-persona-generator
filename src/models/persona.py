import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import yaml


@dataclass
class Persona:
    """
    Represents a generated persona with dynamic attributes based on a YAML
    schema.
    """

    schema: Dict[str, Any]
    data: Dict[str, Any] = field(default_factory=dict)
    _characteristics: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_schema_file(
        cls, schema_path: str, characteristics_path: Optional[str] = None
    ) -> "Persona":
        """
        Create a Persona instance from a YAML schema file.

        Args:
            schema_path: Path to the YAML schema file
            characteristics_path: Optional path to characteristics definition file

        Returns:
            Persona instance
        """
        if not schema_path.endswith((".yaml", ".yml")):
            raise ValueError("Schema file must be YAML (.yaml or .yml)")

        with open(schema_path, "r") as f:
            schema = yaml.safe_load(f)

        instance = cls(schema=schema)

        if characteristics_path:
            instance.load_characteristics(characteristics_path)

        return instance

    def load_characteristics(self, characteristics_path: str) -> None:
        """
        Load characteristics from a YAML file.

        Args:
            characteristics_path: Path to the characteristics definition file
        """
        if not characteristics_path.endswith((".yaml", ".yml")):
            raise ValueError("Characteristics file must be YAML")

        with open(characteristics_path, "r") as f:
            self._characteristics = yaml.safe_load(f)

    def to_dict(self) -> dict:
        """
        Convert the persona to a dictionary format.

        Returns:
            Dictionary representation of the persona
        """
        return self.data

    @classmethod
    def from_dict(
        cls, data: dict, schema: Optional[Dict[str, Any]] = None
    ) -> "Persona":
        """
        Create a Persona instance from a dictionary.

        Args:
            data: Dictionary containing persona data
            schema: Optional schema to validate against

        Returns:
            Persona instance
        """
        if schema is None:
            # Load default schema from file
            default_schema_path = os.path.join(
                os.path.dirname(__file__), "..", "..", "schemas", "default_schema.yaml"
            )
            with open(default_schema_path, "r") as f:
                schema = yaml.safe_load(f)

        return cls(schema=schema, data=data)

    def validate(self) -> bool:
        """
        Validate if the persona data matches the schema requirements.

        Returns:
            True if valid, False otherwise
        """
        for field_name, field_schema in self.schema.items():
            # Check required fields
            if field_schema.get("required", False):
                if field_name not in self.data or not self.data[field_name]:
                    return False

            # Check field type if specified
            if "type" in field_schema:
                field_type = field_schema["type"]
                if field_name in self.data:
                    if field_type == "string" and not isinstance(
                        self.data[field_name], str
                    ):
                        return False
                    elif field_type == "number" and not isinstance(
                        self.data[field_name], (int, float)
                    ):
                        return False

        return True

    def get_required_fields(self) -> List[str]:
        """
        Get list of required fields from the schema.

        Returns:
            List of required field names
        """
        return [
            field_name
            for field_name, field_schema in self.schema.items()
            if field_schema.get("required", False)
        ]

    def get_field_characteristics(self, field_name: str) -> List[Dict[str, Any]]:
        """
        Get the characteristics that should be incorporated into a field.

        Args:
            field_name: Name of the field to get characteristics for

        Returns:
            List of characteristic definitions
        """
        field_schema = self.schema.get(field_name, {})
        characteristic_refs = field_schema.get("characteristics", [])

        characteristics = []
        for ref in characteristic_refs:
            category, name = ref.split(".")
            if (
                category in self._characteristics
                and name in self._characteristics[category]
            ):
                characteristics.append(self._characteristics[category][name])

        return characteristics

    def get_all_characteristics(self) -> Dict[str, Any]:
        """
        Get all characteristics defined in the characteristics file.

        Returns:
            Dictionary of all characteristics
        """
        return self._characteristics

    def get_fields_for_characteristic(self, category: str, name: str) -> List[str]:
        """
        Get all fields that should incorporate a specific characteristic.

        Args:
            category: Category of the characteristic
            name: Name of the characteristic

        Returns:
            List of field names that should include this characteristic
        """
        characteristic_ref = f"{category}.{name}"
        return [
            field_name
            for field_name, field_schema in self.schema.items()
            if "characteristics" in field_schema
            and characteristic_ref in field_schema["characteristics"]
        ]
