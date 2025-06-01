import os
from typing import Dict, Optional

import yaml
from pydantic import BaseModel, Field


class PromptConfig(BaseModel):
    """Configuration for generator prompts."""

    system: str = Field(..., description="System prompt template")
    user: str = Field(..., description="User prompt template")


class ResponseConfig(BaseModel):
    """Configuration for response handling."""

    format: str = Field("json", description="Response format")
    ensure_valid_json: bool = Field(True, description="Ensure valid JSON")


class ValidationConfig(BaseModel):
    """Configuration for validation settings."""

    strict_mode: bool = Field(True, description="Enable strict validation")
    log_validation_errors: bool = Field(True, description="Log validation errors")


class GeneratorConfig(BaseModel):
    """Main configuration for generators."""

    prompts: PromptConfig
    response: ResponseConfig
    validation: ValidationConfig


class ConfigLoader:
    """Loader for generator configuration files."""

    def __init__(self, config_dir: str = "src/generators/config"):
        """Initialize the config loader.

        Args:
            config_dir (str): Directory containing configuration files
        """
        self.config_dir = config_dir

    def load_config(
        self, config_path: str = None, config_name: str = "generator_config"
    ) -> GeneratorConfig:
        """Load a configuration file.

        Args:
            config_path (str): Full path to the config file (optional)
            config_name (str): Name of the config file (without extension)

        Returns:
            GeneratorConfig: The loaded configuration

        Raises:
            FileNotFoundError: If the config file doesn't exist
            ValueError: If config validation fails
        """
        if config_path:
            path = config_path
        else:
            path = os.path.join(self.config_dir, f"{config_name}.yaml")
        if not os.path.exists(path):
            raise FileNotFoundError(f"Config file not found: {path}")

        try:
            with open(path, "r") as f:
                config_data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML format: {e}")

        try:
            return GeneratorConfig(**config_data)
        except Exception as e:
            raise ValueError(f"Config validation failed: {e}")

    def get_prompt(self, config: GeneratorConfig, prompt_type: str, **kwargs) -> str:
        """Get a formatted prompt from the configuration.

        Args:
            config (GeneratorConfig): The configuration to use
            prompt_type (str): Type of prompt to get ('system' or 'user')
            **kwargs: Variables to format into the prompt

        Returns:
            str: The formatted prompt

        Raises:
            ValueError: If the prompt type is invalid
        """
        if prompt_type == "system":
            return config.prompts.system
        elif prompt_type == "user":
            return config.prompts.user.format(**kwargs)
        else:
            raise ValueError(f"Invalid prompt type: {prompt_type}")
