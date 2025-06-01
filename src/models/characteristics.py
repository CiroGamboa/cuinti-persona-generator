from typing import Dict, List

from pydantic import BaseModel, Field, RootModel


class Characteristic(BaseModel):
    """Model for a single characteristic."""

    description: str = Field(..., description="Description of the characteristic")
    examples: List[str] = Field(..., description="Example values")


class CharacteristicCategory(RootModel[Dict[str, "Characteristic"]]):
    """Model for a category of characteristics (root model)."""

    pass


class Characteristics(BaseModel):
    """Model for all characteristics."""

    personal: Dict[str, Characteristic] = Field(
        ..., description="Personal characteristics"
    )
    professional: Dict[str, Characteristic] = Field(
        ..., description="Professional characteristics"
    )
    physical: Dict[str, Characteristic] = Field(
        ..., description="Physical characteristics"
    )
    personality: Dict[str, Characteristic] = Field(
        ..., description="Personality characteristics"
    )
