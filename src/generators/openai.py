import os
from typing import Any, Dict, Optional

from openai import OpenAI

from .base_generator import BaseGenerator


class OpenAIGenerator(BaseGenerator):
    """
    OpenAI-powered persona generator.
    Uses GPT models to generate realistic personas based on schemas.
    """

    def __init__(self, schema_path: Optional[str] = None):
        """
        Initialize the OpenAI generator.

        Args:
            schema_path (Optional[str]): Path to the schema file
        """
        super().__init__(schema_path)
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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

        # Create the system message that explains the task
        system_message = (
            "You are a persona generator. Create a realistic persona based on "
            "the provided schema. The persona should be consistent and "
            "believable, with all characteristics working together to form a "
            "cohesive personality. Return the response as a valid JSON object."
        )

        # Create the user message with schema and prompt
        user_message = f"Schema:\n{self.schema}\n"
        if prompt:
            user_message += f"\nAdditional context: {prompt}\n"
        user_message += "\nGenerate a persona that matches this schema."

        try:
            # Call the OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-4",  # Using GPT-4 for better quality
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message},
                ],
                temperature=0.7,  # Add some randomness
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
        if not self.schema:
            return False

        # Check that all required fields from schema are present
        for field, field_schema in self.schema.items():
            # Default to required if not specified
            if field_schema.get("required", True):
                if field not in persona:
                    print(f"Missing required field: {field}")
                    return False

                # Check field type if specified
                expected_type = field_schema.get("type")
                if expected_type:
                    value = persona[field]
                    if expected_type == "string" and not isinstance(value, str):
                        print(f"Field {field} should be a string, got {type(value)}")
                        return False
                    elif expected_type == "number" and not isinstance(
                        value, (int, float)
                    ):
                        print(f"Field {field} should be a number, got {type(value)}")
                        return False

        return True
