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
            "cohesive personality. Return the response as a valid JSON object. "
            "For any field whose type is 'string', output a plain string, "
            "even if characteristics are listed. Do not output nested objects "
            "for string fields."
        )

        # Create the user message with schema and prompt
        user_message = f"Schema:\n{self.schema}\n"
        if prompt:
            user_message += f"\nAdditional context: {prompt}\n"
        user_message += (
            "\nGenerate a persona that matches this schema. "
            "Remember: for fields of type 'string', output a plain string, "
            "not an object."
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
        print("Schema fields:", list(self.schema["fields"].keys()))
        if not self.schema:
            return False

        def validate_field(
            field_name: str, field_schema: Dict[str, Any], data: Any
        ) -> bool:
            """Helper function to validate a field and its nested fields."""
            # Check if field is required
            if field_schema.get("required", True):
                if field_name not in data:
                    print(f"Missing required field: {field_name}")
                    return False

                value = data[field_name]
                expected_type = field_schema.get("type")

                # Type validation
                if expected_type:
                    if expected_type == "string" and not isinstance(value, str):
                        print(
                            f"Field {field_name} should be a string, "
                            f"got {type(value)}"
                        )
                        return False
                    elif expected_type == "number" and not isinstance(
                        value, (int, float)
                    ):
                        print(
                            f"Field {field_name} should be a number, "
                            f"got {type(value)}"
                        )
                        return False
                    elif expected_type == "object":
                        if not isinstance(value, dict):
                            print(
                                f"Field {field_name} should be an object, "
                                f"got {type(value)}"
                            )
                            return False
                        # Validate nested fields
                        if "fields" in field_schema:
                            for subfield, subfield_schema in field_schema[
                                "fields"
                            ].items():
                                if not validate_field(subfield, subfield_schema, value):
                                    return False
                    elif expected_type == "array":
                        if not isinstance(value, list):
                            print(
                                f"Field {field_name} should be an array, "
                                f"got {type(value)}"
                            )
                            return False
                        # Validate array items if they are objects
                        if (
                            "items" in field_schema
                            and field_schema["items"].get("type") == "object"
                        ):
                            for item in value:
                                if not isinstance(item, dict):
                                    print(
                                        f"Item in {field_name} should be an object, "
                                        f"got {type(item)}"
                                    )
                                    return False
                                if "fields" in field_schema["items"]:
                                    for subfield, subfield_schema in field_schema[
                                        "items"
                                    ]["fields"].items():
                                        if not validate_field(
                                            subfield, subfield_schema, item
                                        ):
                                            return False
            return True

        # Validate all fields in the schema
        for field, field_schema in self.schema["fields"].items():
            if not validate_field(field, field_schema, persona):
                return False

        return True
