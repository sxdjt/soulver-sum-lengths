# soulver-sum-lengths

Sum lengths in mixed units using either Soulver CLI or pure Python.

## Overview

Two implementations:
- **`sum-lengths.py`** - Pure Python, no dependencies (recommended)
- **`soulver-sum-lengths.py`** - Uses Soulver CLI (requires Soulver installation)

Both convert and sum measurements, outputting:
- Decimal inches (2 decimal places)
- Fractional inches (nearest 1/16″)
- Total in millimeters

## Features

- ✅ Accepts fractions: `3 1/2"`, `1/8"`
- ✅ Accepts feet-inch combos: `5' 3 1/2"` → 5 feet + 3.5 inches
- ✅ Accepts mixed units: `mm`, `cm`, `inches`, `feet`, `meters`
- ✅ Works interactively or from command-line args
- ✅ Shows the expression for validation
- ✅ Copies result to clipboard automatically (macOS with `pbcopy`)

## Installation

### Pure Python Version (Recommended)

No installation needed - uses Python 3.6+ standard library:

```bash
git clone https://github.com/sxdjt/soulver-sum-lengths.git
cd soulver-sum-lengths
chmod +x sum-lengths.py
```

### Soulver Version (Optional)

Requires [Soulver CLI](https://documentation.soulver.app/cli/):

```bash
brew install soulver-cli
```

## Usage

### Command-line Arguments

**Single expression:**
```bash
python3 sum-lengths.py '2 1/2" + 5.535" + 9mm'
```

Output:
```
Expression:
  sum (2 1/2 inches + 5.535 inches + 9 millimeters)

Result:
  8.39"
  8 3/8"
  213 mm
```

**Separate arguments:**
```bash
python3 sum-lengths.py 2.5 5.535 9mm
```

**With units:**
```bash
python3 sum-lengths.py 1ft 6in 25.4mm
```

### Interactive Mode

```bash
python3 sum-lengths.py
```

```
Enter lengths (e.g., 2 1/2", 5.535", 9mm). Empty line to finish.
> 2 1/2
> 5.535
> 9mm
> 

Expression:
  sum (2 1/2 inches + 5.535 inches + 9 millimeters)

Result:
  8.39"
  8 3/8"
  213 mm
```

### Make Executable (Optional)

```bash
chmod +x sum-lengths.py
./sum-lengths.py 2.5 5.535 9mm
```

## Supported Units

| Unit Type | Accepted Formats |
|-----------|------------------|
| Inches | `inch`, `inches`, `in`, `"`, `″` |
| Feet | `foot`, `feet`, `ft`, `'`, `′` |
| Millimeters | `millimeter`, `millimeters`, `mm` |
| Centimeters | `centimeter`, `centimeters`, `cm` |
| Meters | `meter`, `meters`, `m` |

**Note:** Bare numbers default to inches.

## Examples

```bash
# Mixed fractions
python3 sum-lengths.py '2 1/2" + 3 3/4"'
# Output: 6.25", 6 1/4", 159 mm

# Feet and inches
python3 sum-lengths.py "5' 3\"" 2.5
# Output: 65.50", 65 1/2", 1664 mm

# Metric and imperial
python3 sum-lengths.py 100mm 4in 5cm
# Output: 9.91", 9 7/8", 252 mm

# Decimal inputs
python3 sum-lengths.py 2.5 3.75 1.125
# Output: 7.38", 7 3/8", 187 mm
```

## Error Handling

The script validates inputs and provides helpful error messages:

```bash
python3 sum-lengths.py "5 furlongs"
# Error: Unsupported unit: furlongs

python3 sum-lengths.py "1/0"
# Error: Division by zero in fraction
```

## Requirements

- Python 3.6+
- macOS (for clipboard copy via `pbcopy`)

No external dependencies required for `sum-lengths.py`.

## Development

### Running Tests

```bash
python3 test_sum_lengths.py
```

Or with pytest:
```bash
pip install pytest
pytest test_sum_lengths.py -v
```

### Code Style

- PEP 8 compliant
- Type hints for public functions
- Docstrings for all modules and functions

## Why Two Versions?

- **`sum-lengths.py`**: Standalone, no dependencies, better error handling
- **`soulver-sum-lengths.py`**: Explores Soulver CLI capabilities, requires Soulver

The pure Python version is recommended for most users.

## Troubleshooting

**"No inputs provided"**
- Ensure you're passing arguments or using interactive mode

**"Cannot parse number"**
- Check fraction format: use `1/2` not `1\2`
- Ensure proper spacing: `2 1/2` not `21/2`

**Clipboard not working**
- Only works on macOS with `pbcopy`
- Results still display in terminal

## License

MIT License - do whatever you like, attribution appreciated.

## Contributing

Pull requests welcome! Please:
- Add tests for new features
- Follow existing code style
- Update README with examples
