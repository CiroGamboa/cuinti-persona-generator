import argparse
from pathlib import Path

from dotenv import load_dotenv

from src.factories.persona_factory import PersonaFactory


def load_environment():
    """Load environment variables from .env file."""
    env_path = Path(".env")
    if not env_path.exists():
        raise FileNotFoundError(".env file not found in the project root")
    load_dotenv(env_path)


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Generate personas using OpenAI")
    parser.add_argument(
        "-n",
        "--num-personas",
        type=int,
        default=1,
        help="Number of personas to generate (default: 1)",
    )
    parser.add_argument(
        "-s",
        "--schema",
        type=str,
        default="schemas/default_schema.yaml",
        help=("Path to schema file " "(default: schemas/default_schema.yaml)"),
    )
    parser.add_argument(
        "-c",
        "--config",
        type=str,
        default="src/generators/config/generator_config.yaml",
        help=(
            "Path to generator config file "
            "(default: src/generators/config/generator_config.yaml)"
        ),
    )
    parser.add_argument(
        "-f",
        "--format",
        type=str,
        choices=["json", "yaml"],
        default="json",
        help="Output format (default: json)",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=str,
        default="export",
        help="Directory where exported files will be saved (default: export)",
    )
    return parser.parse_args()


def main():
    """Main application workflow."""
    try:
        # Parse command line arguments
        args = parse_arguments()

        # Step 1: Load environment variables
        print("Loading environment variables...")
        load_environment()

        # Step 2: Initialize factory and verify connection
        print("Initializing persona factory...")
        factory = PersonaFactory(
            schema_path=args.schema,
            output_format=args.format,
            config_path=args.config,
            output_dir=args.output_dir,
        )
        if not factory.verify_connection():
            raise ConnectionError("Failed to connect to OpenAI API")
        print("✅ OpenAI connection verified!")

        # Step 3: Generate and export personas
        print(f"Generating {args.num_personas} persona(s)...")
        factory.generate_and_export(args.num_personas)

        print("\nApplication workflow completed successfully!")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return


if __name__ == "__main__":
    main()
