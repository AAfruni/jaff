# ABOUTME: Entry point for the JAFF package
# ABOUTME: Exports main classes and functions for chemical network parsing

"""JAFF - Just Another Fancy Format

An astrochemical network parser for various reaction network formats.
"""

__version__ = "0.1.0"

from .network import Network
from .reaction import Reaction
from .species import Species

__all__ = ["Network", "Reaction", "Species"]
