#!/usr/bin/env python3
"""
Sum lengths in mixed units without external dependencies.

Accepts fractions (3 1/2", 1/8"), feet-inches (5' 3 1/2"), 
and mixed units (mm, cm, inches, feet, meters).
Outputs decimal inches, fractional inches (1/16"), and millimeters.
"""

import re
import sys
import shutil
import subprocess
from math import gcd
from typing import List, Tuple, Optional


# Configuration constants
DECIMAL_PRECISION = 2
FRACTIONAL_DENOMINATOR = 16
MM_PER_INCH = 25.4

# Unit conversion factors to inches
UNIT_FACTORS = {
    "inch": 1.0, "inches": 1.0, "in": 1.0, '"': 1.0, "″": 1.0,
    "foot": 12.0, "feet": 12.0, "ft": 12.0, "'": 12.0, "′": 12.0,
    "millimeter": 1.0/MM_PER_INCH, "millimeters": 1.0/MM_PER_INCH, "mm": 1.0/MM_PER_INCH,
    "centimeter": 1.0/2.54, "centimeters": 1.0/2.54, "cm": 1.0/2.54,
    "meter": 39.37007874015748, "meters": 39.37007874015748, "m": 39.37007874015748,
}

# Regex patterns
MIXED_NUMBER_PATTERN = re.compile(r"""
    ^\s*
    (?P<sign>[-+]?)\s*
    (?:
        (?P<whole>\d+)\s+(?P<num>\d+)/(?P<den>\d+)      # 2 1/2
      | (?P<num2>\d+)/(?P<den2>\d+)                      # 1/2
      | (?P<float>\d+(?:\.\d+)?)                         # 2.5
    )
    \s*$
""", re.X)

UNIT_PAIR_PATTERN = re.compile(r"""
    (?P<val>
        [-+]?\d+(?:\s+\d+/\d+)? |                        # 2 1/2
        [-+]?\d*\.\d+ |                                  # 2.5
        [-+]?\d+/\d+                                     # 1/2
    )
    \s*
    (?P<unit>
        inches?|in|["\u2033]|
        feet?|ft|[\'\u2032]|
        millimeters?|mm|
        centimeters?|cm|
        meters?|m
    )
""", re.X | re.I)


def parse_number(value_str: str) -> float:
    """
    Parse a number that can be:
    - Integer: "5"
    - Decimal: "5.5"
    - Fraction: "1/2"
    - Mixed number: "2 1/2"
    - With sign: "-2 1/2"
    
    Args:
        value_str: String representation of number
        
    Returns:
        Float value
        
    Raises:
        ValueError: If string cannot be parsed
    """
    match = MIXED_NUMBER_PATTERN.match(value_str)
    if not match:
        raise ValueError(f"Cannot parse number: {value_str!r}")
    
    sign = -1.0 if match.group("sign") == "-" else 1.0
    
    # Mixed number: "2 1/2"
    if match.group("whole"):
        whole = int(match.group("whole"))
        numerator = int(match.group("num"))
        denominator = int(match.group("den"))
        if denominator == 0:
            raise ValueError(f"Division by zero in fraction: {value_str!r}")
        return sign * (whole + numerator / denominator)
    
    # Simple fraction: "1/2"
    if match.group("num2"):
        numerator = int(match.group("num2"))
        denominator = int(match.group("den2"))
        if denominator == 0:
            raise ValueError(f"Division by zero in fraction: {value_str!r}")
        return sign * (numerator / denominator)
    
    # Decimal or integer
    return sign * float(match.group("float"))


def convert_to_inches(term: str) -> float:
    """
    Convert a length term with optional unit to inches.
    
    Supports: 2.5", 5 feet, 9mm, 2 1/2", etc.
    Defaults to inches if no unit specified.
    
    Args:
        term: Length expression
        
    Returns:
        Length in inches
        
    Raises:
        ValueError: If term cannot be parsed or unit is unsupported
    """
    term = term.strip()
    total_inches = 0.0
    found_any_unit = False
    
    # Find all value+unit pairs in the term
    for match in UNIT_PAIR_PATTERN.finditer(term):
        found_any_unit = True
        value = parse_number(match.group("val"))
        unit = match.group("unit").lower()
        
        # Normalize unicode quote marks
        if unit in ('"', '″'):
            unit = "inches"
        if unit in ("'", "′"):
            unit = "feet"
        
        factor = UNIT_FACTORS.get(unit)
        if factor is None:
            raise ValueError(f"Unsupported unit: {unit}")
        
        total_inches += value * factor
    
    # If no units found, assume inches
    if not found_any_unit:
        total_inches = parse_number(term)
    
    return total_inches


def normalize_term_display(term: str) -> str:
    """
    Normalize a term for display by expanding abbreviations.
    
    Examples:
        '2.5"' -> '2.5 inches'
        "5'" -> '5 feet'
        '9mm' -> '9 millimeters'
    
    Args:
        term: Original term
        
    Returns:
        Normalized display string
    """
    normalized = term.strip()
    
    # Replace unicode quotes with word equivalents
    normalized = re.sub(r'[""″]', ' inches', normalized)
    normalized = re.sub(r"['\'′]", ' feet', normalized)
    
    # Expand abbreviations
    normalized = re.sub(r'\b(in|inch|inches)\b', 'inches', normalized, flags=re.I)
    normalized = re.sub(r'\b(ft|foot|feet)\b', 'feet', normalized, flags=re.I)
    normalized = re.sub(r'\b(mm|millimeter[s]?)\b', 'millimeters', normalized, flags=re.I)
    normalized = re.sub(r'\b(cm|centimeter[s]?)\b', 'centimeters', normalized, flags=re.I)
    normalized = re.sub(r'\b(m|meter[s]?)\b', 'meters', normalized, flags=re.I)
    
    # Ensure space between number and unit
    normalized = re.sub(
        r'(\d)(?=\s?(inches|feet|millimeters|centimeters|meters)\b)',
        r'\1 ',
        normalized,
        flags=re.I
    )
    
    # If no unit found, default to inches
    if not re.search(r'[A-Za-z]', normalized):
        normalized += ' inches'
    
    return normalized


def format_fractional_inches(value_inches: float, denominator: int = 16) -> str:
    """
    Format decimal inches as fractional inches.
    
    Examples:
        8.39 -> 8 3/8"
        8.5 -> 8 1/2"
        8.0 -> 8"
    
    Args:
        value_inches: Decimal inches
        denominator: Denominator for fraction (default: 16 for 1/16")
        
    Returns:
        Formatted fractional string
    """
    sign = "-" if value_inches < 0 else ""
    abs_value = abs(value_inches)
    
    whole = int(abs_value)
    numerator = round((abs_value - whole) * denominator)
    
    # Handle rounding up to next whole number
    if numerator == denominator:
        whole += 1
        numerator = 0
    
    # No fraction needed
    if numerator == 0:
        return f'{sign}{whole}"'
    
    # Simplify fraction
    divisor = gcd(numerator, denominator)
    simplified_num = numerator // divisor
    simplified_den = denominator // divisor
    
    # Format based on whether we have a whole number
    if whole:
        return f'{sign}{whole} {simplified_num}/{simplified_den}"'
    else:
        return f'{sign}{simplified_num}/{simplified_den}"'


def copy_to_clipboard(text: str) -> bool:
    """
    Copy text to system clipboard (macOS only).
    
    Args:
        text: Text to copy
        
    Returns:
        True if successful, False otherwise
    """
    pbcopy_path = shutil.which("pbcopy")
    if not pbcopy_path:
        return False
    
    try:
        subprocess.run(
            [pbcopy_path],
            input=text,
            text=True,
            check=True,
            capture_output=True
        )
        return True
    except (subprocess.CalledProcessError, OSError):
        return False


def parse_input_args(args: List[str]) -> List[str]:
    """
    Parse command-line arguments or prompt for interactive input.
    
    Args:
        args: Command-line arguments (sys.argv[1:])
        
    Returns:
        List of length terms to sum
    """
    # Command-line arguments provided
    if args:
        # Single argument: try splitting on + or ,
        if len(args) == 1:
            parts = [p.strip() for p in re.split(r'\s*[+,]\s*', args[0]) if p.strip()]
            if len(parts) > 1:
                return parts
        return args
    
    # Interactive mode
    print('Enter lengths (e.g., 2 1/2", 5.535", 9mm). Empty line to finish.')
    values = []
    
    while True:
        try:
            line = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()  # New line after Ctrl+D/Ctrl+C
            break
        
        if not line:
            break
        
        values.append(line)
    
    return values


def main():
    """Main entry point."""
    try:
        # Parse inputs
        input_terms = parse_input_args(sys.argv[1:])
        
        if not input_terms:
            print("No inputs provided.")
            sys.exit(0)
        
        # Convert all terms to inches and sum
        total_inches = 0.0
        normalized_terms = []
        
        for term in input_terms:
            try:
                total_inches += convert_to_inches(term)
                normalized_terms.append(normalize_term_display(term))
            except ValueError as e:
                print(f"Error parsing '{term}': {e}", file=sys.stderr)
                sys.exit(1)
        
        # Calculate outputs
        total_mm = total_inches * MM_PER_INCH
        decimal_str = f'{total_inches:.{DECIMAL_PRECISION}f}"'
        fractional_str = format_fractional_inches(total_inches, FRACTIONAL_DENOMINATOR)
        mm_str = f"{round(total_mm)} mm"
        
        # Display results
        print("\nExpression:")
        print("  sum (" + " + ".join(normalized_terms) + ")")
        print("\nResult:")
        print(f"  {decimal_str}")
        print(f"  {fractional_str}")
        print(f"  {mm_str}")
        
        # Copy to clipboard
        clipboard_text = f"{decimal_str}\n{fractional_str}\n{mm_str}\n"
        if copy_to_clipboard(clipboard_text):
            # Don't announce - just silently copy
            pass
        
    except KeyboardInterrupt:
        print("\nInterrupted.")
        sys.exit(130)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
