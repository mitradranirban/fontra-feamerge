# Fontra Feamerge Plugin
[![PyPI version](https://badge.fury.io/py/fontra-feamerge.svg)](https://pypi.org/project/fontra-feamerge/)
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

* Open a `.designspace` file in Fontra
* Access the **Plugin Manager** from the menu
* Select **Feature File Merger** plugin
* Choose from available actions:

    - **Break Kerning Groups**: Expand kerning groups

     - **Break Mark Positioning Groups**: Expand mark positioning3

    - **Merge Variable Features**: Combine all features

     - **Process All**: Run all operations in sequence

### Command Line (Standalone Scripts)

The original standalone scripts are still available:

#### Break kerning groups
`python src/fontra_feamerge/break_groups_in_fea.py path/to/font.ufo`

#### Break mark positioning groups
`python src/fontra_feamerge/break_groups_in_mark_pos.py path/to/font.ufo`
#### Merge features
`python src/fontra_feamerge/combine_features.py MyFont.designspace output.fea`

## Requirements

- Python 3.10+
- fontra >= 0.20.0
- fonttools[ufo] >= 4.50.0

## Development

### Running Tests
`pytest tests/ -v`
### Code Formatting
```
black src tests
isort src tests
```
### Type Checking

`mypy src`

## How It Works

### Designspace Integration

The plugin uses `fontTools.designspaceLib` to read designspace files and extract all UFO source references, handling both absolute and relative paths.

### UFO Feature Reading

Using `fontTools.ufoLib2`, the plugin opens each UFO and reads the `features.fea` content, providing access to complete feature definitions from each master.

### Variable Font Syntax Generation

The plugin generates variable font positioning syntax with:
- Combined glyph classes from all masters
- Positioning rules with coordinate:value pairs
- Support for both regular and enum positioning statements

Example output:
`pos A A (wdth=100,wght=400:10 wdth=100,wght=900:20)`

## License

GPL-3.0-or-later

## Author

Anirban Mitra 

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## References

- [FontTools UFOLib Documentation](https://fonttools.readthedocs.io/en/latest/ufoLib/)
- [Designspace Specification](https://fonttools.readthedocs.io/en/latest/designspaceLib/)
- [FontTools FeaLib Documentation](https://fonttools.readthedocs.io/en/latest/feaLib/)
- [Fontra Documentation](https://docs.fontra.xyz/)
