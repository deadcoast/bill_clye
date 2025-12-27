"""Conflict database module for MRDR.

This module provides access to syntax conflict definitions
documenting delimiter collisions between programming languages.
"""

from mrdr.database.conflict.schema import (
    ConflictDatabase,
    ConflictEntry,
)

__all__ = [
    "ConflictDatabase",
    "ConflictEntry",
]
