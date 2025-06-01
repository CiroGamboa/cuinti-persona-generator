import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Optional

import yaml

from src.generators.config.config_loader import (
    ConfigLoader,
    GeneratorConfig,
    PromptConfig,
    ResponseConfig,
    ValidationConfig,
)
from src.schemas.loader import SchemaLoader


class BaseGenerator(ABC):
    """
    Base interface for AI-powered persona generation.
    Uses schemas to define the structure and constraints of personas to
    generate.
    """

    def __init__(
        self,
        schema_path: Optional[str] = None,
        config_path: Optional[str] = None,
    ):
        """
        Initialize the generator with a schema path.

        Args:
            schema_path (Optional[str]): Path to the schema file that
                defines the persona structure
            config_path (Optional[str]): Path to the generator config file
        """
        self.schema_path = schema_path
        self.schema = self._load_schema() if schema_path else None
        self.config = self._load_config(config_path) if config_path else None

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

    def _load_config(self, config_path: Optional[str] = None) -> GeneratorConfig:
        """
        Load the generator configuration.

        Args:
            config_path (Optional[str]): Path to the config file

        Returns:
            GeneratorConfig: The loaded configuration
        """
        loader = ConfigLoader()
        if config_path:
            # Convert to absolute path if relative
            if not os.path.isabs(config_path):
                config_path = os.path.abspath(config_path)
            return loader.load_config(config_path=config_path)
        else:
            # Try to load from default location
            default_path = os.path.join(
                os.path.dirname(__file__), "config", "generator_config.yaml"
            )
            if os.path.exists(default_path):
                return loader.load_config(config_path=default_path)
            else:
                # Create a default configuration if none exists
                return GeneratorConfig(
                    prompts=PromptConfig(
                        system=(
                            "You are a persona generator. Generate realistic "
                            "personas based on the provided schema."
                        ),
                        user=(
                            "Generate a persona following this schema:\n"
                            "{schema}\n{additional_context}"
                        ),
                    ),
                    response=ResponseConfig(),
                    validation=ValidationConfig(),
                )

    def _get_system_prompt(self) -> str:
        """
        Get the system prompt for persona generation.

        Returns:
            str: The system prompt
        """
        if not self.config:
            raise ValueError("Configuration not loaded")
        return self.config.prompts.system

    def _get_user_prompt(self, prompt: Optional[str] = None) -> str:
        """
        Get the user prompt for persona generation.

        Args:
            prompt (Optional[str]): Additional context for generation

        Returns:
            str: The user prompt
        """
        if not self.config:
            raise ValueError("Configuration not loaded")
        return self.config.prompts.user.format(
            schema=self.schema.model_dump_json(),
            additional_context=(f"Additional context: {prompt}\n" if prompt else ""),
        )

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

    def validate(self, persona: Dict[str, Any]) -> bool:
        """
        Validate a generated persona against the schema.

        Args:
            persona (Dict[str, Any]): The persona data to validate

        Returns:
            bool: True if the persona is valid, False otherwise
        """
        if not self.schema:
            raise ValueError("Schema not loaded. Please provide a schema path.")

        if not self.config:
            raise ValueError("Configuration not loaded")

        # Check that all required fields are present
        for field_name, field_def in self.schema.fields.items():
            if field_def.required and field_name not in persona:
                if self.config.validation.log_validation_errors:
                    print(f"Missing required field: {field_name}")
                return False

            # Check field type
            if field_name in persona:
                field_value = persona[field_name]
                if field_def.type == "string" and not isinstance(field_value, str):
                    if self.config.validation.log_validation_errors:
                        print(f"Field {field_name} should be a string")
                    return False
                elif field_def.type == "number" and not isinstance(
                    field_value, (int, float)
                ):
                    if self.config.validation.log_validation_errors:
                        print(f"Field {field_name} should be a number")
                    return False
                elif field_def.type == "boolean" and not isinstance(field_value, bool):
                    if self.config.validation.log_validation_errors:
                        print(f"Field {field_name} should be a boolean")
                    return False
                elif field_def.type == "array" and not isinstance(field_value, list):
                    if self.config.validation.log_validation_errors:
                        print(f"Field {field_name} should be an array")
                    return False
                elif field_def.type == "object" and not isinstance(field_value, dict):
                    if self.config.validation.log_validation_errors:
                        print(f"Field {field_name} should be an object")
                    return False

                # Check string length constraints
                if field_def.type == "string" and isinstance(field_value, str):
                    if field_def.min_length and len(field_value) < field_def.min_length:
                        if self.config.validation.log_validation_errors:
                            print(
                                f"Field {field_name} is too short "
                                f"(min length: {field_def.min_length})"
                            )
                        return False
                    if field_def.max_length and len(field_value) > field_def.max_length:
                        if self.config.validation.log_validation_errors:
                            print(
                                f"Field {field_name} is too long "
                                f"(max length: {field_def.max_length})"
                            )
                        return False

                # Check options if specified
                if field_def.options and field_value not in field_def.options:
                    if self.config.validation.log_validation_errors:
                        print(
                            f"Field {field_name} value '{field_value}' "
                            f"not in allowed options: {field_def.options}"
                        )
                    return False

        return True

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
        if not self.config:
            raise ValueError("Configuration not loaded")

        if format == self.config.response.format:
            return yaml.dump(persona, indent=2)
        else:
            raise ValueError(f"Unsupported export format: {format}")
