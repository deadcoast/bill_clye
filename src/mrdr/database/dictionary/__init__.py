"""Dictionary database module for MRDR.

This module provides access to the MRDR dictionary hierarchy
as defined in docs/dictionary.md.
"""

from mrdr.database.dictionary.schema import (
    DictionaryDatabase,
    DictionaryEntry,
    HierarchyLevel,
)

__all__ = [
    "DictionaryDatabase",
    "DictionaryEntry",
    "HierarchyLevel",
]
