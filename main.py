from pathlib import Path

from dotenv import load_dotenv

from src.exporters.persona_exporter import PersonaExporter
from src.generators.openai import OpenAIGenerator


def load_environment():
    """Load environment variables from .env file."""
    env_path = Path(".env")
    if not env_path.exists():
        raise FileNotFoundError(".env file not found in the project root")
    load_dotenv(env_path)


def main():
    """Main application workflow."""
    try:
        # Step 1: Load environment variables
        print("Loading environment variables...")
        load_environment()

        # Step 2: Initialize generator and verify connection
        print("Initializing OpenAI generator...")
        generator = OpenAIGenerator(schema_path="schemas/default_schema.yaml")
        if not generator.verify_access():
            raise ConnectionError("Failed to connect to OpenAI API")
        print("✅ OpenAI connection verified!")

        # Step 3: Generate persona
        print("Generating persona...")
        persona = generator.generate()
        print("✅ Persona generated successfully!")

        # Step 4: Export persona
        exporter = PersonaExporter()
        exporter.export(persona)

        print("\nApplication workflow completed successfully!")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return


if __name__ == "__main__":
    main()
