from pathlib import Path
from typing import Any, Dict, List

from src.exporters.persona_exporter import PersonaExporter
from src.generators.openai import OpenAIGenerator


class PersonaFactory:
    """Factory class for generating and exporting multiple personas."""

    def __init__(
        self, schema_path: str, output_format: str = "json", output_dir: str = "."
    ):
        """
        Initialize the persona factory.

        Args:
            schema_path: Path to the schema file
            output_format: Output format (json or yaml)
            output_dir: Directory where exported files will be saved
        """
        self.schema_path = schema_path
        self.output_format = output_format
        self.output_dir = Path(output_dir)
        self.generator = OpenAIGenerator(schema_path=schema_path)
        self.exporter = PersonaExporter(output_dir=output_dir)

    def verify_connection(self) -> bool:
        """
        Verify the connection to OpenAI API.

        Returns:
            bool: True if connection is successful, False otherwise
        """
        return self.generator.verify_access()

    def generate_personas(self, num_personas: int) -> List[Dict[str, Any]]:
        """
        Generate multiple personas.

        Args:
            num_personas: Number of personas to generate

        Returns:
            List[Dict[str, Any]]: List of generated personas
        """
        personas = []
        for i in range(num_personas):
            print(f"\nGenerating persona {i + 1}/{num_personas}...")
            persona = self.generator.generate()
            personas.append(persona)
            print(f"✅ Persona {i + 1} generated successfully!")
        return personas

    def export_personas(
        self, personas: List[Dict[str, Any]], filename_prefix: str = "persona"
    ) -> List[Path]:
        """
        Export multiple personas to files.

        Args:
            personas: List of personas to export
            filename_prefix: Prefix for the output filenames

        Returns:
            List[Path]: List of paths to the exported files
        """
        exported_paths = []
        for i, persona in enumerate(personas):
            filename = f"{filename_prefix}_{i + 1}.{self.output_format}"
            output_path = self.exporter.export(
                persona, output_format=self.output_format, filename=filename
            )
            print(f"✅ Persona {i + 1} exported to {output_path}")
            exported_paths.append(output_path)
        return exported_paths

    def generate_and_export(
        self, num_personas: int, filename_prefix: str = "persona"
    ) -> List[Path]:
        """
        Generate and export multiple personas in one operation.

        Args:
            num_personas: Number of personas to generate
            filename_prefix: Prefix for the output filenames

        Returns:
            List[Path]: List of paths to the exported files
        """
        personas = self.generate_personas(num_personas)
        return self.export_personas(personas, filename_prefix)
