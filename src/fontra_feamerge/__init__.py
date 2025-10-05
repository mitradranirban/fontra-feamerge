"""
Fontra Feamerge Plugin - Variable Feature File Merger

A Fontra plugin for merging multiple Adobe feature files from a designspace
into a single variable feature file, with support for breaking kerning and
mark positioning groups.
"""

__version__ = "0.1.0"
__author__ = "Anirban Mitra"

from .backend import FeamergeBackend
from .plugin import registerFontraPlugin

__all__ = ["FeamergeBackend", "registerFontraPlugin", "__version__"]

