import os
from typing import Any, Dict, Optional

from openai import OpenAI

from src.generators.base_generator import BaseGenerator


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
            "cohesive personality. Return the response as a valid JSON object. "
            "For any field whose type is 'string', output a plain string, "
            "even if characteristics are listed. Do not output nested objects "
            "for string fields. "
            "IMPORTANT: The 'bio' field must not exceed 500 characters."
        )

        # Create the user message with schema and prompt
        user_message = f"Schema:\n{self.schema.model_dump_json()}\n"
        if prompt:
            user_message += f"\nAdditional context: {prompt}\n"
        user_message += (
            "\nGenerate a persona that matches this schema. "
            "Remember: for fields of type 'string', output a plain string, "
            "not an object. "
            "IMPORTANT: The 'bio' field must not exceed 500 characters."
        )

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
