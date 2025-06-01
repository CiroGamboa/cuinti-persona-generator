import os
from typing import Any, Dict, Optional

from openai import OpenAI

from src.generators.base_generator import BaseGenerator


class OpenAIGenerator(BaseGenerator):
    """
    OpenAI-powered persona generator.
    Uses GPT models to generate realistic personas based on schemas.
    """

    def __init__(
        self,
        schema_path: Optional[str] = None,
        config_path: Optional[str] = None,
        model: str = "gpt-4",
        temperature: float = 0.7,
    ):
        """
        Initialize the OpenAI generator.

        Args:
            schema_path (Optional[str]): Path to the schema file
            config_path (Optional[str]): Path to the generator config file
            model (str): The OpenAI model to use
            temperature (float): Sampling temperature (0.0 to 1.0)
        """
        super().__init__(schema_path, config_path)
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model
        self.temperature = temperature

    def verify_access(self) -> bool:
        """
        Verify that we can access the OpenAI API.

        Returns:
            bool: True if access is successful, False otherwise
        """
        try:
            # Make a minimal API call to verify access
            self.client.models.list()
            return True
        except Exception as e:
            print(f"Error verifying OpenAI access: {str(e)}")
            return False

    def generate(self, prompt: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate a persona using OpenAI's API.

        Args:
            prompt (Optional[str]): Additional context for generation

        Returns:
            Dict[str, Any]: Generated persona data

        Raises:
            ValueError: If schema is not loaded
        """
        if not self.schema:
            raise ValueError("Schema not loaded. Please provide a schema path.")

        if not self.config:
            raise ValueError("Configuration not loaded")

        try:
            # Call the OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": self._get_system_prompt(),
                    },
                    {
                        "role": "user",
                        "content": self._get_user_prompt(prompt),
                    },
                ],
                temperature=self.temperature,
            )

            # Parse the response
            content = response.choices[0].message.content
            try:
                import json

                persona = json.loads(content)
            except json.JSONDecodeError:
                raise ValueError("Failed to parse persona as JSON")

            # Validate the generated persona
            if self.validate(persona):
                return persona
            else:
                raise ValueError("Generated persona failed validation")

        except Exception as e:
            raise Exception(f"Error generating persona: {str(e)}")

    def validate(self, persona: Dict[str, Any]) -> bool:
        """
        Validate a generated persona against the schema.

        Args:
            persona (Dict[str, Any]): The persona data to validate

        Returns:
            bool: True if the persona is valid, False otherwise
        """
        print("Validating persona:", persona)
        print("Schema fields:", list(self.schema.fields.keys()))

        # Check that all required fields are present
        for field_name, field_def in self.schema.fields.items():
            if field_def.required and field_name not in persona:
                print(f"Missing required field: {field_name}")
                return False

            # Check field type
            if field_name in persona:
                field_value = persona[field_name]
                if field_def.type == "string" and not isinstance(field_value, str):
                    print(f"Field {field_name} should be a string")
                    return False
                elif field_def.type == "number" and not isinstance(
                    field_value, (int, float)
                ):
                    print(f"Field {field_name} should be a number")
                    return False
                elif field_def.type == "boolean" and not isinstance(field_value, bool):
                    print(f"Field {field_name} should be a boolean")
                    return False
                elif field_def.type == "array" and not isinstance(field_value, list):
                    print(f"Field {field_name} should be an array")
                    return False
                elif field_def.type == "object" and not isinstance(field_value, dict):
                    print(f"Field {field_name} should be an object")
                    return False

                # Check string length constraints
                if field_def.type == "string" and isinstance(field_value, str):
                    if field_def.min_length and len(field_value) < field_def.min_length:
                        print(
                            f"Field {field_name} is too short "
                            f"(min length: {field_def.min_length})"
                        )
                        return False
                    if field_def.max_length and len(field_value) > field_def.max_length:
                        print(
                            f"Field {field_name} is too long "
                            f"(max length: {field_def.max_length})"
                        )
                        return False

                # Check options if specified
                if field_def.options and field_value not in field_def.options:
                    print(
                        f"Field {field_name} value '{field_value}' "
                        f"not in allowed options: {field_def.options}"
                    )
                    return False

        return True
