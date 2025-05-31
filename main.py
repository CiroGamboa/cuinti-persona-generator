from pathlib import Path

from dotenv import load_dotenv

from src.generators.openai import OpenAIGenerator


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

        # TODO: Future workflow steps
        # Step 3: Load schema
        # Step 4: Generate persona
        # Step 5: Validate persona
        # Step 6: Export persona

        print("\nApplication workflow completed successfully!")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return


if __name__ == "__main__":
    main()
