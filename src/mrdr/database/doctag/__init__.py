"""Doctag database module for MRDR.

This module provides access to the doctag definitions from docs/doctags.md,
including delimiters (DDL), grammar (GRM), inter-document commands (IDC),
and formatting rules (FMT).
"""

from mrdr.database.doctag.loader import DoctagLoader
from mrdr.database.doctag.schema import (
    DOCTAG_DATABASE,
    DoctagCategory,
    DoctagDefinition,
)

__all__ = [
    "DoctagLoader",
    "DoctagDefinition",
    "DoctagCategory",
    "DOCTAG_DATABASE",
]
