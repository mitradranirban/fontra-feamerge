"""
Fontra plugin registration and metadata
"""

from .backend import FeamergeBackend


def registerFontraPlugin():
    """
    Entry point for Fontra plugin registration.

    Returns a dictionary with plugin metadata and configuration.
    """
    return {
        "name": "feamerge",
        "displayName": "Feature File Merger",
        "version": "0.1.0",
        "description": "Merge multiple Adobe feature files into variable feature files",
        "backend": FeamergeBackend,
        "fileTypes": [".designspace"],
        "actions": [
            {
                "id": "break-kerning-groups",
                "label": "Break Kerning Groups",
                "description": "Expand kerning groups into individual glyph pairs",
                "handler": "breakKerningGroups",
                "icon": "expand",
            },
            {
                "id": "break-mark-groups",
                "label": "Break Mark Positioning Groups",
                "description": "Expand mark positioning groups into individual glyphs",
                "handler": "breakMarkGroups",
                "icon": "expand",
            },
            {
                "id": "merge-features",
                "label": "Merge Variable Features",
                "description": "Combine all feature files into variable feature syntax",
                "handler": "mergeFeatures",
                "icon": "merge",
            },
            {
                "id": "process-all",
                "label": "Process All (Break Groups + Merge)",
                "description": "Break all groups and merge features in one operation",
                "handler": "processAll",
                "icon": "play",
            },
        ],
        "settings": {
            "outputPath": {
                "type": "string",
                "default": "variable_features.fea",
                "label": "Output Feature File Name",
                "description": "Name of the merged feature file to generate",
            },
            "preserveComments": {
                "type": "boolean",
                "default": True,
                "label": "Preserve Comments",
                "description": "Keep comments from source feature files",
            },
            "expandAllGroups": {
                "type": "boolean",
                "default": False,
                "label": "Auto-expand Groups",
                "description": "Automatically expand groups before merging",
            },
        },
    }
