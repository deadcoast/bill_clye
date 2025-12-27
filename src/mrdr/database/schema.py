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


class PlusrepLabel(str, Enum):
    """PLUSREP grade labels.

    Defines the valid labels for PLUSREP grades based on rating.
    """

    MAXIMUM = "MAXIMUM"  # rating +4
    GREAT = "GREAT"  # rating +2 or +3
    SLOPPY = "SLOPPY"  # rating 0
    REJECTED = "REJECTED"  # rating -2
    RESET = "RESET"  # rating -3


# Mapping from rating to valid label(s)
RATING_TO_LABELS: dict[int, list[PlusrepLabel]] = {
    4: [PlusrepLabel.MAXIMUM],
    3: [PlusrepLabel.GREAT],
    2: [PlusrepLabel.GREAT],
    1: [PlusrepLabel.GREAT],  # Not in spec but valid rating
    0: [PlusrepLabel.SLOPPY],
    -1: [PlusrepLabel.SLOPPY],  # Not in spec but valid rating
    -2: [PlusrepLabel.REJECTED],
}


def calculate_plusrep_rating(tokens: str) -> int:
    """Calculate PLUSREP rating from tokens.

    Rating = (count of '+') - 2, ranging from -2 to +4.

    Args:
        tokens: 6-character string of '+' and '.' characters.

    Returns:
        Integer rating from -2 to +4.
    """
    return tokens.count("+") - 2


def get_label_for_rating(rating: int) -> PlusrepLabel:
    """Get the appropriate label for a rating.

    Args:
        rating: Integer rating from -2 to +4.

    Returns:
        The appropriate PlusrepLabel for the rating.
    """
    if rating >= 4:
        return PlusrepLabel.MAXIMUM
    elif rating >= 1:
        return PlusrepLabel.GREAT
    elif rating >= -1:
        return PlusrepLabel.SLOPPY
    else:
        return PlusrepLabel.REJECTED


class PlusrepGrade(BaseModel):
    """PLUSREP quality grade.

    Represents a quality rating using the PLUSREP system with 6 tokens.
    The rating is calculated as (count of '+') - 2, ranging from -2 to +4.
    Labels are assigned based on rating:
    - MAXIMUM: +4
    - GREAT: +1 to +3
    - SLOPPY: -1 to 0
    - REJECTED: -2
    """

    tokens: str = Field(
        ..., pattern=r"^[\+\.]{6}$", description="6-char grade string of + and . chars"
    )
    rating: int = Field(..., ge=-2, le=4, description="Numeric rating: (count of +) - 2")
    label: str = Field(
        ..., description="Grade label (MAXIMUM, GREAT, SLOPPY, REJECTED)"
    )

    model_config = {"use_enum_values": True}

    @classmethod
    def validate_rating_matches_tokens(cls, rating: int, tokens: str) -> bool:
        """Validate that rating matches the token count formula.

        Args:
            rating: The rating value to validate.
            tokens: The token string to calculate expected rating from.

        Returns:
            True if rating matches expected calculation.
        """
        expected_rating = calculate_plusrep_rating(tokens)
        return rating == expected_rating

    @classmethod
    def validate_label_matches_rating(cls, label: str, rating: int) -> bool:
        """Validate that label is appropriate for the rating.

        Args:
            label: The label to validate.
            rating: The rating to check against.

        Returns:
            True if label is valid for the rating.
        """
        expected_label = get_label_for_rating(rating)
        return label == expected_label.value

    def model_post_init(self, __context) -> None:
        """Validate rating and label consistency after initialization."""
        # Validate rating matches tokens
        expected_rating = calculate_plusrep_rating(self.tokens)
        if self.rating != expected_rating:
            raise ValueError(
                f"Rating {self.rating} does not match expected {expected_rating} "
                f"for tokens '{self.tokens}' (formula: count('+') - 2)"
            )

        # Validate label matches rating
        expected_label = get_label_for_rating(self.rating)
        if self.label != expected_label.value:
            raise ValueError(
                f"Label '{self.label}' does not match expected '{expected_label.value}' "
                f"for rating {self.rating}"
            )


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
