import os
from pathlib import Path
from typing import Any, List

import yaml

from src.schemas.validator import SchemaValidator


class SchemaLoader:
    """Loader for schema files."""

    def __init__(self, schema_dir: str = "schemas"):
        """Initialize the schema loader.

        Args:
            schema_dir (str): Directory containing schema files
        """
        self.schema_dir = schema_dir

    def load_schema(self, schema_name: str) -> Any:
        """Load a schema from a YAML file.

        Args:
            schema_name (str): Name of the schema file (without extension)

        Returns:
            Any: The loaded schema

        Raises:
            FileNotFoundError: If the schema file doesn't exist
            ValueError: If schema validation fails
        """
        schema_path = os.path.join(self.schema_dir, f"{schema_name}.yaml")
        if not os.path.exists(schema_path):
            raise FileNotFoundError(f"Schema file not found: {schema_path}")

        try:
            with open(schema_path, "r") as f:
                schema_data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML format: {e}")

        if schema_name == "characteristics":
            return SchemaValidator.validate_characteristics(schema_data)
        else:
            return SchemaValidator.validate_schema(schema_data)

    def list_schemas(self) -> List[str]:
        """List all available schema files.

        Returns:
            List[str]: List of schema names (without extension)
        """
        schemas = []
        for file in os.listdir(self.schema_dir):
            if file.endswith(".yaml"):
                schemas.append(Path(file).stem)
        return schemas
