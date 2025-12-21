# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Python utility for summing lengths in mixed units (imperial and metric). Converts inputs to inches, then outputs decimal inches, fractional inches (1/16"), and millimeters. Designed for macOS with automatic clipboard copying via pbcopy.

Two implementations:
- **sum-lengths.py** - Pure Python, standalone (recommended)
- **soulver-sum-lengths.py** - Uses Soulver CLI (requires external dependency)

Both share utility functions from **length_utils.py** for formatting and clipboard operations.

## Development Commands

### Running Tests
```bash
python3 test_sum_lengths.py
```

With pytest:
```bash
pytest test_sum_lengths.py -v
```

### Running the Main Script
```bash
# Interactive mode
python3 sum-lengths.py

# Command-line arguments
python3 sum-lengths.py '2 1/2" + 5.535" + 9mm'
python3 sum-lengths.py 2.5 5.535 9mm

# Make executable
chmod +x sum-lengths.py
./sum-lengths.py 2.5 5.535 9mm
```

## Code Architecture

### Core Parsing Logic (sum-lengths.py)

The parsing system uses two main regex patterns:

1. **MIXED_NUMBER_PATTERN** - Parses numeric values:
   - Mixed numbers: `2 1/2`
   - Simple fractions: `1/2`
   - Decimals: `2.5`
   - With signs: `-2 1/2`

2. **UNIT_PAIR_PATTERN** - Extracts value+unit pairs from input:
   - Matches numbers followed by unit abbreviations
   - Handles unicode quote marks (″ for inches, ′ for feet)
   - Case-insensitive unit matching

### Conversion Pipeline

Input → parse_number() → convert_to_inches() → sum → format output

1. **parse_number()** - Converts string to float (handles fractions)
2. **convert_to_inches()** - Applies unit conversion using UNIT_FACTORS dict
3. **format_fractional_inches()** - Converts decimal to simplified fraction using GCD
4. **normalize_term_display()** - Expands abbreviations for output display

### Shared Utilities (length_utils.py)

Provides common functions to avoid duplication between implementations:
- **copy_to_clipboard()** - macOS pbcopy integration with timeout
- **format_fractional_inches()** - Fraction formatting with GCD simplification
- **format_decimal_inches()** - Decimal formatting with configurable precision
- **format_millimeters()** - Inch-to-mm conversion
- **normalize_unit_display()** - Unit abbreviation expansion

### Configuration Constants

All in sum-lengths.py:
- DECIMAL_PRECISION = 2
- FRACTIONAL_DENOMINATOR = 16 (for 1/16" precision)
- MM_PER_INCH = 25.4
- UNIT_FACTORS dict maps all unit variants to inch conversion factors

### Test Structure (test_sum_lengths.py)

Currently a skeleton with test case outlines. Tests are organized by functionality:
- Number parsing (integers, decimals, fractions, mixed numbers)
- Unit conversion (feet, mm, cm, meters to inches)
- Fractional formatting (whole numbers, simplification, rounding)
- Integration tests (README examples, edge cases)
- Input parsing (CLI args, separators)

Note: Tests contain docstrings showing what should be tested but implementations are placeholder `pass` statements.

## Supported Unit Variations

The UNIT_FACTORS dict normalizes all these variants:
- Inches: `inch`, `inches`, `in`, `"`, `″` (unicode)
- Feet: `foot`, `feet`, `ft`, `'`, `′` (unicode)
- Millimeters: `millimeter`, `millimeters`, `mm`
- Centimeters: `centimeter`, `centimeters`, `cm`
- Meters: `meter`, `meters`, `m`

Bare numbers default to inches.

## Key Implementation Details

### Fraction Simplification
Uses math.gcd() to reduce fractions to lowest terms (8/16 → 1/2). Handles rounding when result equals denominator (15/16 rounds to next whole number).

### Input Parsing Modes
- Single arg with `+` or `,` separators → split into multiple terms
- Multiple args → each treated as separate term
- No args → interactive mode with prompt loop

### Clipboard Behavior
Silently copies results to clipboard if pbcopy available. No error messages if unavailable (graceful degradation).

### Unicode Handling
Regex patterns explicitly match unicode quote marks (U+2033 double prime, U+2032 prime) for copy-paste compatibility.
