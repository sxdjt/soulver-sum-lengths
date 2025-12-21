#!/usr/bin/env python3
"""
Test suite for sum-lengths.py

Run with: python3 test_sum_lengths.py
Or with pytest: pytest test_sum_lengths.py -v
"""

import unittest

# Import functions from sum-lengths.py
import importlib.util
spec = importlib.util.spec_from_file_location("sum_lengths", "sum-lengths.py")
sum_lengths = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sum_lengths)

# Import the functions we need
parse_number = sum_lengths.parse_number
convert_to_inches = sum_lengths.convert_to_inches
format_fractional_inches = sum_lengths.format_fractional_inches
parse_input_args = sum_lengths.parse_input_args
MM_PER_INCH = sum_lengths.MM_PER_INCH

class TestNumberParsing(unittest.TestCase):
    """Test number parsing functionality."""

    def test_parse_integer(self):
        """Test parsing integers."""
        self.assertEqual(parse_number("5"), 5.0)
        self.assertEqual(parse_number("10"), 10.0)

    def test_parse_decimal(self):
        """Test parsing decimals."""
        self.assertEqual(parse_number("5.5"), 5.5)
        self.assertAlmostEqual(parse_number("2.75"), 2.75)

    def test_parse_simple_fraction(self):
        """Test parsing simple fractions."""
        self.assertEqual(parse_number("1/2"), 0.5)
        self.assertEqual(parse_number("1/4"), 0.25)
        self.assertEqual(parse_number("3/4"), 0.75)

    def test_parse_mixed_number(self):
        """Test parsing mixed numbers."""
        self.assertEqual(parse_number("2 1/2"), 2.5)
        self.assertEqual(parse_number("5 3/4"), 5.75)

    def test_parse_negative_number(self):
        """Test parsing negative numbers."""
        self.assertEqual(parse_number("-2 1/2"), -2.5)
        self.assertEqual(parse_number("-5"), -5.0)
        self.assertEqual(parse_number("-1/4"), -0.25)

    def test_parse_invalid_number(self):
        """Test that invalid numbers raise ValueError."""
        with self.assertRaises(ValueError):
            parse_number("abc")
        with self.assertRaises(ValueError):
            parse_number("")
        with self.assertRaises(ValueError):
            parse_number("1/0")  # Division by zero


class TestUnitConversion(unittest.TestCase):
    """Test unit conversion functionality."""

    def test_inches_default(self):
        """Test that bare numbers default to inches."""
        self.assertEqual(convert_to_inches("5"), 5.0)
        self.assertEqual(convert_to_inches("2.5"), 2.5)

    def test_feet_to_inches(self):
        """Test feet to inches conversion."""
        self.assertEqual(convert_to_inches("1 feet"), 12.0)
        self.assertEqual(convert_to_inches("2feet"), 24.0)
        self.assertEqual(convert_to_inches("1ft"), 12.0)

    def test_mm_to_inches(self):
        """Test millimeters to inches conversion."""
        self.assertAlmostEqual(convert_to_inches("25.4mm"), 1.0, places=5)
        self.assertAlmostEqual(convert_to_inches("50.8mm"), 2.0, places=5)

    def test_mixed_fraction_with_unit(self):
        """Test mixed fractions with units."""
        self.assertEqual(convert_to_inches('2 1/2"'), 2.5)
        self.assertEqual(convert_to_inches("2 1/2 inches"), 2.5)

    def test_unicode_quotes(self):
        """Test unicode quote marks."""
        self.assertEqual(convert_to_inches("5″"), 5.0)  # double prime for inches
        self.assertEqual(convert_to_inches("5′"), 60.0)  # single prime for feet


class TestFractionalFormatting(unittest.TestCase):
    """Test fractional inch formatting."""

    def test_whole_number(self):
        """Test formatting whole numbers."""
        self.assertEqual(format_fractional_inches(8.0), '8"')
        self.assertEqual(format_fractional_inches(10.0), '10"')

    def test_half_inch(self):
        """Test formatting half inch."""
        self.assertEqual(format_fractional_inches(8.5), '8 1/2"')
        self.assertEqual(format_fractional_inches(0.5), '1/2"')

    def test_eighth_inch(self):
        """Test formatting eighth inch."""
        self.assertEqual(format_fractional_inches(8.375), '8 3/8"')
        self.assertEqual(format_fractional_inches(8.625), '8 5/8"')

    def test_sixteenth_simplification(self):
        """Test that 8/16 simplifies to 1/2."""
        self.assertEqual(format_fractional_inches(8.5), '8 1/2"')  # not 8 8/16"
        self.assertEqual(format_fractional_inches(8.25), '8 1/4"')  # not 8 4/16"

    def test_rounding_up(self):
        """Test rounding up to next whole number."""
        # 8.96875 = 8 15/16" which should round to 9"
        self.assertEqual(format_fractional_inches(8.96875), '9"')


class TestIntegration(unittest.TestCase):
    """Integration tests."""

    def test_example_from_readme(self):
        """Test the example from README."""
        # Input: 2 1/2", 5.535", 9mm
        inputs = ['2 1/2"', '5.535"', '9mm']
        total_inches = sum(convert_to_inches(inp) for inp in inputs)
        self.assertAlmostEqual(total_inches, 8.3897, places=3)
        self.assertEqual(format_fractional_inches(total_inches), '8 3/8"')
        total_mm = round(total_inches * MM_PER_INCH)
        self.assertEqual(total_mm, 213)

    def test_multiple_units(self):
        """Test summing multiple different units."""
        # Input: 1ft, 5inches, 25.4mm
        inputs = ['1ft', '5inches', '25.4mm']
        total_inches = sum(convert_to_inches(inp) for inp in inputs)
        self.assertAlmostEqual(total_inches, 18.0, places=3)
        total_mm = round(total_inches * MM_PER_INCH)
        self.assertEqual(total_mm, 457)

    def test_negative_value(self):
        """Test handling negative values."""
        result = convert_to_inches("-2.5")
        self.assertEqual(result, -2.5)
        formatted = format_fractional_inches(-2.5)
        self.assertEqual(formatted, '-2 1/2"')

    def test_zero_value(self):
        """Test handling zero."""
        self.assertEqual(convert_to_inches("0"), 0.0)
        self.assertEqual(format_fractional_inches(0.0), '0"')


class TestInputParsing(unittest.TestCase):
    """Test input parsing."""

    def test_single_quoted_string(self):
        """Test parsing single quoted string with + separator."""
        # Input: "2 1/2\" + 5.535\" + 9mm"
        result = parse_input_args(['2 1/2" + 5.535" + 9mm'])
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], '2 1/2"')
        self.assertEqual(result[1], '5.535"')
        self.assertEqual(result[2], '9mm')

    def test_multiple_args(self):
        """Test parsing multiple command-line arguments."""
        result = parse_input_args(["2.5", "5.535", "9mm"])
        self.assertEqual(len(result), 3)
        self.assertEqual(result, ["2.5", "5.535", "9mm"])

    def test_comma_separator(self):
        """Test comma as separator."""
        result = parse_input_args(["2.5, 5.535, 9mm"])
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], "2.5")
        self.assertEqual(result[1], "5.535")
        self.assertEqual(result[2], "9mm")


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error conditions."""

    def test_empty_input(self):
        """Test handling empty input."""
        result = parse_input_args([])
        self.assertEqual(result, [])

    def test_division_by_zero(self):
        """Test that division by zero raises error."""
        with self.assertRaises(ValueError):
            parse_number("1/0")

    def test_very_large_number(self):
        """Test handling very large numbers."""
        result = convert_to_inches("1000000")
        self.assertEqual(result, 1000000.0)
        formatted = format_fractional_inches(1000000.0)
        self.assertEqual(formatted, '1000000"')

    def test_very_small_number(self):
        """Test handling very small numbers."""
        result = convert_to_inches("0.001")
        self.assertAlmostEqual(result, 0.001)

    def test_invalid_unit(self):
        """Test that invalid units raise error."""
        with self.assertRaises(ValueError):
            convert_to_inches("5 furlongs")


def run_manual_tests():
    """
    Manual test examples that can be run visually.
    These match the README examples.
    """
    print("Manual Test Cases:")
    print("-" * 50)

    test_cases = [
        ('2 1/2" + 5.535" + 9mm', "Should output: 8.39\", 8 3/8\", 213 mm"),
        ('2.5 5.535 9mm', "Should output: 8.39\", 8 3/8\", 213 mm"),
        ('1 foot 6 inches', "Should output: 18\", 1 1/2 feet, 457 mm"),
        ('25.4mm', "Should output: 1\", 1\", 25 mm"),
    ]

    for test_input, expected in test_cases:
        print(f"\nInput: {test_input}")
        print(f"Expected: {expected}")
        print()


if __name__ == "__main__":
    # Run unit tests
    unittest.main()
