from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Optional

import yaml

from src.schemas.loader import SchemaLoader


class BaseGenerator(ABC):
    """
    Base interface for AI-powered persona generation.
    Uses schemas to define the structure and constraints of personas to
    generate.
    """

    def __init__(self, schema_path: Optional[str] = None):
        """
        Initialize the generator with a schema path.

        Args:
            schema_path (Optional[str]): Path to the schema file that
                defines the persona structure
        """
        self.schema_path = schema_path
        self.schema = self._load_schema() if schema_path else None

    def _load_schema(self) -> Dict[str, Any]:
        """
        Load the YAML schema from the specified path.

        Returns:
            Dict[str, Any]: The loaded schema

        Raises:
            FileNotFoundError: If the schema file doesn't exist
            ValueError: If schema validation fails
        """
        if not self.schema_path:
            raise ValueError("Schema path not provided")

        schema_dir = str(Path(self.schema_path).parent)
        schema_name = Path(self.schema_path).stem
        loader = SchemaLoader(schema_dir=schema_dir)
        return loader.load_schema(schema_name)

    @abstractmethod
    def generate(self, prompt: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate a persona based on the schema and optional prompt.

        Args:
            prompt (Optional[str]): Additional context or requirements for
                the persona generation

        Returns:
            Dict[str, Any]: The generated persona data

        Raises:
            NotImplementedError: Must be implemented by concrete classes
        """
        raise NotImplementedError("Subclasses must implement generate()")

    @abstractmethod
    def validate(self, persona: Dict[str, Any]) -> bool:
        """
        Validate a generated persona against the schema.

        Args:
            persona (Dict[str, Any]): The persona data to validate

        Returns:
            bool: True if the persona is valid, False otherwise

        Raises:
            NotImplementedError: Must be implemented by concrete classes
        """
        raise NotImplementedError("Subclasses must implement validate()")

    def export(self, persona: Dict[str, Any], format: str = "json") -> str:
        """
        Export the generated persona in the specified format.

        Args:
            persona (Dict[str, Any]): The persona data to export
            format (str): The export format ('json' or 'yaml')

        Returns:
            str: The exported persona data

        Raises:
            ValueError: If the format is not supported
        """
        if format == "json":
            return yaml.dump(persona, indent=2)
        else:
            raise ValueError(f"Unsupported export format: {format}")
