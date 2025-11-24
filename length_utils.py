#!/usr/bin/env python3
"""
Shared utilities for length calculation and formatting.

This module provides common functions used by both sum-lengths.py
and soulver-sum-lengths.py to avoid code duplication.
"""

import re
import shutil
import subprocess
from math import gcd
from typing import Optional


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
            capture_output=True,
            timeout=1.0
        )
        return True
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, OSError):
        return False


def format_fractional_inches(
    value_inches: float,
    denominator: int = 16
) -> str:
    """
    Format decimal inches as fractional inches.
    
    Examples:
        8.39 -> 8 3/8"
        8.5 -> 8 1/2"
        8.0 -> 8"
        0.5 -> 1/2"
    
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


def format_decimal_inches(value_inches: float, precision: int = 2) -> str:
    """
    Format decimal inches with specified precision.
    
    Args:
        value_inches: Value in inches
        precision: Number of decimal places
        
    Returns:
        Formatted string like '8.39"'
    """
    return f'{value_inches:.{precision}f}"'


def format_millimeters(value_inches: float, mm_per_inch: float = 25.4) -> str:
    """
    Convert inches to millimeters and format.
    
    Args:
        value_inches: Value in inches
        mm_per_inch: Conversion factor (default: 25.4)
        
    Returns:
        Formatted string like '213 mm'
    """
    mm_value = value_inches * mm_per_inch
    return f"{round(mm_value)} mm"


def split_input_terms(input_string: str) -> list:
    """
    Split input string on + or , separators.
    
    Args:
        input_string: Input like "2.5 + 3.5 + 4"
        
    Returns:
        List of terms: ["2.5", "3.5", "4"]
    """
    parts = [p.strip() for p in re.split(r'\s*[+,]\s*', input_string) if p.strip()]
    return parts if len(parts) > 1 else [input_string]


def normalize_unit_display(unit: str) -> str:
    """
    Normalize unit abbreviations for display.
    
    Args:
        unit: Unit abbreviation like 'in', 'ft', 'mm'
        
    Returns:
        Full unit name: 'inches', 'feet', 'millimeters'
    """
    unit_lower = unit.lower()
    
    unit_map = {
        'in': 'inches',
        'inch': 'inches',
        'ft': 'feet',
        'foot': 'feet',
        'mm': 'millimeters',
        'millimeter': 'millimeters',
        'cm': 'centimeters',
        'centimeter': 'centimeters',
        'm': 'meters',
        'meter': 'meters',
        '"': 'inches',
        '″': 'inches',
        "'": 'feet',
        '′': 'feet',
    }
    
    return unit_map.get(unit_lower, unit)


if __name__ == "__main__":
    # Quick tests
    print("Testing format_fractional_inches:")
    test_cases = [8.0, 8.5, 8.375, 8.0625, 0.5, -2.5]
    for val in test_cases:
        print(f"  {val} -> {format_fractional_inches(val)}")
    
    print("\nTesting format_decimal_inches:")
    print(f"  8.39 -> {format_decimal_inches(8.39)}")
    
    print("\nTesting format_millimeters:")
    print(f"  8.39 inches -> {format_millimeters(8.39)}")
    
    print("\nTesting split_input_terms:")
    print(f"  '2.5 + 3.5 + 4' -> {split_input_terms('2.5 + 3.5 + 4')}")
    
    print("\nTesting normalize_unit_display:")
    units = ['in', 'ft', 'mm', '"', "'"]
    for u in units:
        print(f"  {u} -> {normalize_unit_display(u)}")
