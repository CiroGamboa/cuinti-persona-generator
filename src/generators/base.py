# Base generator implementation will be added later

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class BaseGenerator(ABC):
    """
    Abstract base class for persona generators.
    Defines the core interface for generating personas using different AI models.
    """

    @abstractmethod
    def generate_personas(self, count: int) -> List[Dict[str, Any]]:
        """
        Generate a specified number of personas.

        Args:
            count: Number of personas to generate

        Returns:
            List of generated personas
        """
        pass

    @abstractmethod
    def validate_persona(self, persona: Dict[str, Any]) -> bool:
        """
        Validate if a generated persona meets requirements.

        Args:
            persona: The persona data to validate

        Returns:
            True if valid, False otherwise
        """
        pass

    @abstractmethod
    def get_supported_characteristics(self) -> List[str]:
        """
        Get a list of characteristics that this generator supports.

        Returns:
            List of characteristic names that can be used with this generator
        """
        pass
