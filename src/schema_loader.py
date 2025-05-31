from pathlib import Path

import yaml

from src.models.schema import Schema


class SchemaLoader:
    """Handles loading and validating persona schemas."""

    def __init__(self, schema_dir: str = "schemas"):
        """Initialize the schema loader.

        Args:
            schema_dir: Directory containing schema files
        """
        self.schema_dir = Path(schema_dir)
        if not self.schema_dir.exists():
            raise FileNotFoundError(f"Schema directory not found: {schema_dir}")

    def load_schema(self, schema_name: str) -> Schema:
        """Load and validate a schema from a YAML file.

        Args:
            schema_name: Name of the schema file (without .yaml extension)

        Returns:
            Validated Schema object

        Raises:
            FileNotFoundError: If schema file doesn't exist
            ValueError: If schema validation fails
        """
        schema_path = self.schema_dir / f"{schema_name}.yaml"
        if not schema_path.exists():
            raise FileNotFoundError(f"Schema file not found: {schema_path}")

        try:
            with open(schema_path, "r") as f:
                schema_data = yaml.safe_load(f)

            # Validate schema using Pydantic model
            schema = Schema(**schema_data)
            return schema

        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML format in schema file: {e}")
        except Exception as e:
            raise ValueError(f"Schema validation failed: {e}")

    def list_available_schemas(self) -> list[str]:
        """List all available schema files.

        Returns:
            List of schema names (without .yaml extension)
        """
        return [f.stem for f in self.schema_dir.glob("*.yaml")]
