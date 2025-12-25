"""UDL (User Defined Language) module for MRDR.

This module provides support for custom docstring format definitions,
allowing users to create and manage their own docstring syntax patterns.
"""

from mrdr.database.udl.schema import (
    DOLPHIN_OPERATOR,
    WALRUS_OPERATOR,
    UDLDefinition,
    UDLEntry,
    UDLOperator,
)
from mrdr.database.udl.loader import UDLLoader
from mrdr.database.udl.validator import UDLValidator

__all__ = [
    "DOLPHIN_OPERATOR",
    "UDLDefinition",
    "UDLEntry",
    "UDLLoader",
    "UDLOperator",
    "UDLValidator",
    "WALRUS_OPERATOR",
]
