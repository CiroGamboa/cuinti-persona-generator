from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class FieldDefinition(BaseModel):
    """Model for a single field in the schema."""

    description: str
    type: str = "string"
    required: bool = True
    options: Optional[List[str]] = None
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    characteristics: Optional[List[str]] = None


class Schema(BaseModel):
    """Model for the complete persona schema."""

    name: str = Field(..., description="Name of the schema")
    description: str = Field(..., description="Description of the schema")
    version: str = Field(..., description="Schema version")
    fields: Dict[str, FieldDefinition] = Field(..., description="Dictionary of fields")

    class Config:
        """Pydantic model configuration."""

        extra = "forbid"  # Prevent extra fields
