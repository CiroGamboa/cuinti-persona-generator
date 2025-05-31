import json
from pathlib import Path
from typing import Any, Dict

import yaml


class PersonaExporter:
    """Handles exporting persona data to different file formats."""

    def __init__(self, output_dir: str = "."):
        """
        Initialize the persona exporter.

        Args:
            output_dir: Directory where exported files will be saved
        """
        self.output_dir = Path(output_dir)

    def export(
        self, persona: Dict[str, Any], output_format: str = "json", filename: str = None
    ) -> Path:
        """
        Export the persona to a file.

        Args:
            persona: Generated persona data
            output_format: Output format (json or yaml)
            filename: Custom filename for the output file (optional)

        Returns:
            Path: Path to the exported file

        Raises:
            ValueError: If output_format is not supported
        """
        if output_format not in ["json", "yaml"]:
            raise ValueError("Output format must be either 'json' or 'yaml'")

        if filename is None:
            filename = f"persona.{output_format}"
        elif not filename.endswith(f".{output_format}"):
            filename = f"{filename}.{output_format}"

        output_path = self.output_dir / filename
        print(f"Exporting persona to {output_path}...")

        try:
            if output_format == "json":
                with open(output_path, "w") as f:
                    json.dump(persona, f, indent=4)
            else:
                with open(output_path, "w") as f:
                    yaml.safe_dump(
                        persona,
                        f,
                        default_flow_style=False,
                        sort_keys=False,
                        indent=2,
                    )
            print(f"✅ Persona exported successfully to {output_path}!")
            return output_path
        except Exception as e:
            print(f"❌ Failed to export persona: {str(e)}")
            raise
