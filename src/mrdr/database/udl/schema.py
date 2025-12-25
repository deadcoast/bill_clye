"""Pydantic data models for the UDL (User Defined Language) system.

This module defines the core data models for custom docstring format
definitions, including operators, delimiters, and complete UDL entries.
"""

from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class UDLOperator(BaseModel):
    """UDL operator definition.

    An operator is a two-character delimiter pair that provides
    additional functionality beyond single-character delimiters.

    Attributes:
        name: Operator name (e.g., 'dolphin', 'walrus').
        open: Opening delimiter (exactly 2 characters).
        close: Closing delimiter (exactly 2 characters).
    """

    name: str = Field(..., description="Operator name (e.g., 'dolphin', 'walrus')")
    open: str = Field(..., min_length=2, max_length=2, description="Opening delimiter")
    close: str = Field(..., min_length=2, max_length=2, description="Closing delimiter")

    @field_validator("open", "close")
    @classmethod
    def validate_two_chars(cls, v: str) -> str:
        """Validate that operator delimiters are exactly 2 characters."""
        if len(v) != 2:
            raise ValueError("Operator delimiter must be exactly 2 characters")
        return v


class UDLDefinition(BaseModel):
    """User Defined Language docstring definition.

    Defines the structure and delimiters for a custom docstring format.

    Attributes:
        title: UDL title/name.
        description: UDL description.
        language: Target language (defaults to 'UDL').
        delimiter_open: Opening delimiter (single character).
        delimiter_close: Closing delimiter (single character).
        bracket_open: Opening bracket (defaults to '(').
        bracket_close: Closing bracket (defaults to ')').
        operators: List of custom operators.
    """

    title: str = Field(..., description="UDL title")
    description: str = Field(..., alias="descr", description="UDL description")
    language: str = Field(default="UDL", alias="lang", description="Target language")
    delimiter_open: str = Field(
        ..., min_length=1, max_length=1, description="Opening delimiter"
    )
    delimiter_close: str = Field(
        ..., min_length=1, max_length=1, description="Closing delimiter"
    )
    bracket_open: str = Field(default="(", description="Opening bracket")
    bracket_close: str = Field(default=")", description="Closing bracket")
    operators: list[UDLOperator] = Field(
        default_factory=list, description="Custom operators"
    )

    model_config = {"populate_by_name": True}

    @field_validator("delimiter_open", "delimiter_close")
    @classmethod
    def validate_single_char(cls, v: str) -> str:
        """Validate that delimiters are exactly 1 character."""
        if len(v) != 1:
            raise ValueError("Delimiter must be exactly 1 character")
        return v


class UDLEntry(BaseModel):
    """Complete UDL database entry.

    Represents a stored UDL definition with metadata.

    Attributes:
        name: UDL identifier name.
        definition: The UDL definition.
        examples: Example usages.
        created_at: Creation timestamp.
    """

    name: str = Field(..., description="UDL identifier name")
    definition: UDLDefinition = Field(..., description="UDL definition")
    examples: list[str] = Field(default_factory=list, description="Example usages")
    created_at: str = Field(
        default_factory=lambda: datetime.now().isoformat(),
        description="Creation timestamp",
    )

    model_config = {"use_enum_values": True}


# Predefined operators
DOLPHIN_OPERATOR = UDLOperator(name="dolphin", open="<:", close=":>")
WALRUS_OPERATOR = UDLOperator(name="walrus", open=":=", close="=:")
