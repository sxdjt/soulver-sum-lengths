#!/usr/bin/env python3

# The same as soulver-sum-lenghts.py, but not using Soulver

import re, sys, math, shutil, subprocess
from math import gcd

PBCOPY = shutil.which("pbcopy")

# ---------- parsing helpers ----------

RE_MIXED = re.compile(r"""
    ^\s*
    (?P<sign>[-+]?)\s*
    (?:
        (?P<whole>\d+)\s+(?P<num>\d+)\/(?P<den>\d+)
      | (?P<num2>\d+)\/(?P<den2>\d+)
      | (?P<float>\d+(?:\.\d+)?)
    )
    \s*$
""", re.X)

def parse_number(s: str) -> float:
    m = RE_MIXED.match(s)
    if not m:
        raise ValueError(f"bad number: {s!r}")
    sign = -1.0 if m.group("sign") == "-" else 1.0
    if m.group("whole"):
        return sign * (int(m.group("whole")) + int(m.group("num"))/int(m.group("den")))
    if m.group("num2"):
        return sign * (int(m.group("num2"))/int(m.group("den2")))
    return sign * float(m.group("float"))

UNIT_PAIR_RE = re.compile(r"""
    (?P<val>
        [-+]?\d+(?:\s+\d+/\d+)? | [-+]?\d*\.\d+ | [-+]?\d+/\d+
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

FACTOR_TO_INCH = {
    "inch": 1.0, "inches": 1.0, "in": 1.0, '"': 1.0, "″": 1.0,
    "foot": 12.0, "feet": 12.0, "ft": 12.0, "'": 12.0, "′": 12.0,
    "millimeter": 1.0/25.4, "millimeters": 1.0/25.4, "mm": 1.0/25.4,
    "centimeter": 1.0/2.54, "centimeters": 1.0/2.54, "cm": 1.0/2.54,
    "meter": 39.37007874015748, "meters": 39.37007874015748, "m": 39.37007874015748,
}

def term_to_inches(term: str) -> float:
    s = term.strip()
    inches = 0.0
    found = False
    for m in UNIT_PAIR_RE.finditer(s):
        found = True
        val = parse_number(m.group("val"))
        unit = m.group("unit").lower()
        if unit in ('"', '″'): unit = "inches"
        if unit in ("'", "′"): unit = "feet"
        factor = FACTOR_TO_INCH.get(unit)
        if factor is None:
            raise ValueError(f"unsupported unit: {unit}")
        inches += val * factor
    if not found:
        inches = parse_number(s)  # assume inches
    return inches

def pretty_term(term: str) -> str:
    t = term.strip()
    t = re.sub(r"[\"“”\u2033]", " inches", t)
    t = re.sub(r"[\'’\u2032]", " feet", t)
    t = re.sub(r"\b(in|inch|inches)\b", "inches", t, flags=re.I)
    t = re.sub(r"\b(ft|foot|feet)\b", "feet", t, flags=re.I)
    t = re.sub(r"\b(mm|millimeter[s]?)\b", "millimeters", t, flags=re.I)
    t = re.sub(r"\b(cm|centimeter[s]?)\b", "centimeters", t, flags=re.I)
    t = re.sub(r"\b(m|meter[s]?)\b", "meters", t, flags=re.I)
    t = re.sub(r"(\d)(?=\s?(inches|feet|millimeters|centimeters|meters)\b)", r"\1 ", t, flags=re.I)
    if not re.search(r"[A-Za-z]", t):
        t += " inches"
    return t

def frac_1_16(x_in: float) -> str:
    sign = "-" if x_in < 0 else ""
    x = abs(x_in)
    whole = int(x)
    num = round((x - whole) * 16)
    if num == 16:
        whole += 1
        num = 0
    if num == 0:
        return f'{sign}{whole}"'
    g = gcd(num, 16)
    return f'{sign}{whole} {num//g}/{16//g}"' if whole else f'{sign}{num//g}/{16//g}"'

def copy_to_clipboard(text: str):
    if PBCOPY:
        subprocess.run([PBCOPY], input=text, text=True)

def parse_items(argv):
    if argv:
        if len(argv) == 1:
            parts = [p.strip() for p in re.split(r"\s*[+,]\s*", argv[0]) if p.strip()]
            if len(parts) > 1:
                return parts
        return argv
    print('Enter lengths (e.g., 2 1/2", 5.535", 9mm). Empty line to finish.')
    vals = []
    while True:
        try:
            line = input("> ")
        except EOFError:
            break
        line = line.strip()
        if not line:
            break
        vals.append(line)
    return vals

def main():
    items_raw = parse_items(sys.argv[1:])
    if not items_raw:
        print("No inputs.")
        return

    total_in = 0.0
    pretty_items = []
    for t in items_raw:
        total_in += term_to_inches(t)
        pretty_items.append(pretty_term(t))

    total_mm = total_in * 25.4
    dec_in  = f'{total_in:.2f}"'
    frac_in = frac_1_16(total_in)
    mm_str  = f"{round(total_mm)} mm"

    print("\nExpression:")
    print("  sum (" + " + ".join(pretty_items) + ")")
    print("\nResult:")
    print(f"  {dec_in}")
    print(f"  {frac_in}")
    print(f"  {mm_str}")

    # Clipboard copy
    copy_to_clipboard(f"{dec_in}\n{frac_in}\n{mm_str}\n")

if __name__ == "__main__":
    main()
