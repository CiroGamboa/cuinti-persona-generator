import json
from pathlib import Path
from typing import Any, Dict, List

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
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def export(
        self, persona: Dict[str, Any], output_format: str = "json", filename: str = None
    ) -> Path:
        """
        Export a single persona to a file.

        Args:
            persona: Generated persona data
            output_format: Output format (json or yaml)
            filename: Custom filename for the output file (optional)

        Returns:
            Path: Path to the exported file

        Raises:
            ValueError: If output_format is not supported
        """
        return self.export_multiple([persona], output_format, filename)

    def export_multiple(
        self,
        personas: List[Dict[str, Any]],
        output_format: str = "json",
        filename: str = None,
    ) -> Path:
        """
        Export multiple personas to a single file.

        Args:
            personas: List of generated persona data
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
            filename = f"personas.{output_format}"
        elif not filename.endswith(f".{output_format}"):
            filename = f"{filename}.{output_format}"

        output_path = self.output_dir / filename
        print(f"Exporting {len(personas)} personas to {output_path}...")

        try:
            if output_format == "json":
                with open(output_path, "w") as f:
                    json.dump({"personas": personas}, f, indent=4)
            else:
                with open(output_path, "w") as f:
                    yaml.safe_dump(
                        {"personas": personas},
                        f,
                        default_flow_style=False,
                        sort_keys=False,
                        indent=2,
                    )
            print(f"✅ Personas exported successfully to {output_path}!")
            return output_path
        except Exception as e:
            print(f"❌ Failed to export personas: {str(e)}")
            raise
