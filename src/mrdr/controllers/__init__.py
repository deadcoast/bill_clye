"""Controllers module for MRDR.

This module provides the controller layer for the MRDR CLI:
- HydeController: Back-end data correlation controller
"""

from mrdr.controllers.base import Controller
from mrdr.controllers.hyde import HydeController

__all__ = ["Controller", "HydeController"]
