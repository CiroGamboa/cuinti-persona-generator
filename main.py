from pathlib import Path

from dotenv import load_dotenv

from src.generators.openai import OpenAIGenerator
from src.schema_loader import SchemaLoader


def load_environment():
    """Load environment variables from .env file."""
    env_path = Path(".env")
    if not env_path.exists():
        raise FileNotFoundError(".env file not found in the project root")
    load_dotenv(env_path)


def test_openai_connection() -> bool:
    """Test the connection to OpenAI API."""
    print("Testing OpenAI connection...")
    generator = OpenAIGenerator()

    if generator.verify_access():
        print("✅ Successfully connected to OpenAI API!")
        return True
    else:
        print("❌ Failed to connect to OpenAI API")
        return False


def load_and_validate_schema(schema_name: str) -> dict:
    """Load and validate a schema.

    Args:
        schema_name: Name of the schema to load

    Returns:
        Validated schema data
    """
    print(f"Loading schema: {schema_name}...")
    schema_loader = SchemaLoader()
    try:
        schema = schema_loader.load_schema(schema_name)
        print("✅ Schema loaded and validated successfully!")
        return schema.dict()
    except Exception as e:
        print(f"❌ Failed to load schema: {str(e)}")
        raise


def generate_persona(schema: dict) -> dict:
    """Generate a persona using the provided schema.

    Args:
        schema: Validated schema data

    Returns:
        Generated persona data
    """
    print("Generating persona...")
    generator = OpenAIGenerator()
    try:
        persona = generator.generate_persona(schema)
        print("✅ Persona generated successfully!")
        return persona
    except Exception as e:
        print(f"❌ Failed to generate persona: {str(e)}")
        raise


def export_persona(persona: dict, output_format: str = "json") -> None:
    """Export the generated persona to a file.

    Args:
        persona: Generated persona data
        output_format: Output format (json or yaml)
    """
    output_path = Path("persona.json" if output_format == "json" else "persona.yaml")
    print(f"Exporting persona to {output_path}...")

    try:
        if output_format == "json":
            import json

            with open(output_path, "w") as f:
                json.dump(persona, f, indent=2)
        else:
            import yaml

            with open(output_path, "w") as f:
                yaml.safe_dump(persona, f, default_flow_style=False)
        print(f"✅ Persona exported successfully to {output_path}!")
    except Exception as e:
        print(f"❌ Failed to export persona: {str(e)}")
        raise


def main():
    """Main application workflow."""
    try:
        # Step 1: Load environment variables
        print("Loading environment variables...")
        load_environment()

        # Step 2: Test OpenAI connection
        if not test_openai_connection():
            print("Exiting due to connection failure...")
            return

        # Step 3: Load schema
        schema = load_and_validate_schema("default_schema")

        # Step 4: Generate persona
        persona = generate_persona(schema)

        # Step 5: Export persona
        export_persona(persona)

        print("\nApplication workflow completed successfully!")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return


if __name__ == "__main__":
    main()
