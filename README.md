# Fontra Feamerge Plugin

A comprehensive Fontra plugin for merging multiple Adobe feature files from a designspace into a single variable feature file, with support for breaking kerning and mark positioning groups.

## Features

- **Variable Feature Merging**: Combines OpenType feature files from all designspace sources into variable font syntax
- **Kerning Group Expansion**: Breaks kerning groups into individual glyph-to-glyph pairs
- **Mark Positioning Group Expansion**: Expands mark/abvm/blwm positioning groups
- **Async Operations**: Non-blocking operations with progress reporting
- **Fontra Integration**: Seamless integration with Fontra's plugin system

## Installation

### As a Fontra Plugin
```
pip install fontra-feamerge
```

The plugin will be automatically discovered by Fontra through the plugin system.

### For Development

```
git clone https://github.com/mitradranirban/feamerge.git
cd feamerge
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
pip install -e ".[dev]"
```

## Usage

### Within Fontra

1. Open a `.designspace` file in Fontra
2. Access the **Plugin Manager** from the menu
3. Select **Feature File Merger** plugin
4. Choose from available actions:
   - **Merge Variable Features**: Combine all features
   - **Break Kerning Groups**: Expand kerning groups
   - **Break Mark Positioning Groups**: Expand mark positioning
   - **Process All**: Run all operations in sequence

### Command Line (Standalone Scripts)

The original standalone scripts are still available:

#### Break kerning groups
`python src/fontra_feamerge/break_groups_in_fea.py path/to/font.ufo`

#### Break mark positioning groups
`python src/fontra_feamerge/break_groups_in_mark_pos.py path/to/font.ufo`
#### Merge features
`python src/fontra_feamerge/combine_features.py MyFont.designspace output.fea`
