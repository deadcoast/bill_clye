"""Pydantic data models for the MRDR database schema.

This module defines the core data models used for validating and
representing docstring syntax entries in the database.
"""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class SyntaxType(str, Enum):
    """Docstring syntax carrier types.

    Defines how the docstring is syntactically represented in the language.
    """

    LITERAL = "literal"
    BLOCK = "block"
    LINE_SUGARED = "line_sugared"
    PADDED_BRACKET = "padded_bracket"
    MODULE_ATTRIBUTE = "module_attribute"
    NESTABLE_BLOCK = "nestable_block"
    PREFIX_LITERAL = "prefix_literal"
    HADDOCK_BLOCK = "haddock_block"
    POSITIONAL = "positional"
    LEADING_LINE = "leading_line"
    XML_STRUCTURED = "xml_structured"
    ATTRIBUTE_COMMENT = "attribute_comment"
    ARGUMENT_METADATA = "argument_metadata"


class SyntaxLocation(str, Enum):
    """Docstring attachment location types.

    Defines where the docstring attaches relative to the documented element.
    """

    INTERNAL_FIRST_LINE = "internal_first_line"
    ABOVE_TARGET = "above_target"
    ANYWHERE = "anywhere"
    COLUMN_7 = "column_7"
    COLUMN_1 = "column_1"
    AFTER_NAME = "after_name"


class SyntaxSpec(BaseModel):
    """Docstring syntax specification.

    Defines the delimiters and structural properties of a docstring syntax.
    """

    start: str = Field(..., description="Opening delimiter")
    end: Optional[str] = Field(
        None, description="Closing delimiter (None for line-based)"
    )
    type: SyntaxType = Field(..., description="Syntax carrier type")
    location: SyntaxLocation = Field(..., description="Where docstring attaches")

    model_config = {"use_enum_values": True}


class PlusrepGrade(BaseModel):
    """PLUSREP quality grade.

    Represents a quality rating using the PLUSREP system with 6 tokens.
    """

    tokens: str = Field(
        ..., pattern=r"^[\+\.]{6}$", description="6-char grade string of + and . chars"
    )
    rating: int = Field(..., ge=-2, le=4, description="Numeric rating: (count of +) - 2")
    label: str = Field(
        ..., description="Grade label (MAXIMUM, GREAT, GOOD, FAIR, SLOPPY, RESET)"
    )

    model_config = {"use_enum_values": True}


class DocstringEntry(BaseModel):
    """Complete docstring database entry.

    Represents a single language's docstring syntax specification
    with all associated metadata.
    """

    language: str = Field(..., description="Programming language name")
    syntax: SyntaxSpec = Field(..., description="Syntax specification")
    tags: list[str] = Field(default_factory=list, description="Categorization tags")
    example_content: Optional[str] = Field(
        None, description="Example docstring content"
    )
    conflict_ref: Optional[str] = Field(
        None, description="Reference to conflicting syntax"
    )
    parsing_rule: Optional[str] = Field(
        None, description="Special parsing instructions"
    )
    metadata: Optional[str] = Field(None, description="Additional notes")
    plusrep: Optional[PlusrepGrade] = Field(None, description="Quality grade")

    model_config = {"use_enum_values": True}
