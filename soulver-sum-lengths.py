#!/usr/bin/env python3
import re, shutil, subprocess, sys
from math import gcd

SOULVER = shutil.which("soulver") or sys.exit("soulver CLI not found. brew install soulver-cli")
PBCOPY  = shutil.which("pbcopy")

# Precompiled patterns
RE_NUM   = re.compile(r"-?\d+(?:\.\d+)?")
RE_HAS_L = re.compile(r"[A-Za-z]")                 # any letter → has unit tokens
RE_FT    = re.compile(r"['\u2032]")                # ' or ′
RE_IN    = re.compile(r'["\u2033]')                # " or ″
RE_FT_IN = re.compile(r"\b(\d+)\s*feet?\s*(\d+(?:\s+\d+/\d+|\.\d+)?)\s*inches?\b", re.I)

# Unit token normalization map
UNIT_MAP = {
    r"\bft\b": "feet",
    r"\bfeet\b": "feet",
    r"\bin\b": "inches", r"\binch\b": "inches", r"\binches\b": "inches",
    r"\bmm\b": "millimeters", r"\bmillimeter(s)?\b": "millimeters",
    r"\bcm\b": "centimeters", r"\bcentimeter(s)?\b": "centimeters",
}

def norm_units(s: str) -> str:
    s = s.strip()
    if not s:
        return s
    # Convert marks to words first
    s = RE_FT.sub(" feet", s)
    s = RE_IN.sub(" inches", s)
    # Collapse feet-inches combos like "5 feet 3 1/2 inches" → "5 feet + 3 1/2 inches"
    s = RE_FT_IN.sub(r"\1 feet + \2 inches", s)
    # Normalize unit tokens
    for pat, repl in UNIT_MAP.items():
        s = re.sub(pat, repl, s, flags=re.I)
    # Ensure a space between number and unit (e.g., 9mm → 9 millimeters)
    s = re.sub(r"(\d)(?=(?:\s)?(millimeters|centimeters|inches|feet)\b)", r"\1 ", s)
    # Default to inches if no letters present (plain number)
    if not RE_HAS_L.search(s):
        s += " inches"
    return s.strip()

def parse_argv(argv):
    if not argv:
        return []
    if len(argv) == 1:
        # Single expression like: 2" + 5.535" + 9mm
        parts = [p.strip() for p in re.split(r"\s*[+,]\s*", argv[0]) if p.strip()]
        if len(parts) > 1:
            return [norm_units(p) for p in parts]
    # Multiple args: treat each as a term
    return [norm_units(a) for a in argv]

def soulver_mm_sum(items):
    expr_core = " + ".join(items)
    soulver_expr = "convert (" + expr_core + ") to millimeters"
    p = subprocess.run([SOULVER], input=soulver_expr + "\n", capture_output=True, text=True)
    if p.returncode != 0:
        sys.exit(f"Soulver error:\n{p.stderr.strip() or p.stdout.strip()}")
    out = (p.stdout or "").strip().replace("\u2009"," ").replace("\u00a0"," ")
    m = RE_NUM.search(out)
    if not m:
        sys.exit(f"Could not parse number from Soulver output: {out!r}")
    # return numeric + simplified display string
    return float(m.group(0)), f"sum ({expr_core})"


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

def read_items_interactive():
    print('Enter lengths (e.g., 2 1/2", 5.535", 9mm, or 5\' 3 1/2"). Empty line to finish.')
    vals = []
    while True:
        try:
            line = input("> ")
        except EOFError:
            break
        line = line.strip()
        if not line:
            break
        vals.append(norm_units(line))
    return vals

def main():
    items = parse_argv(sys.argv[1:]) if len(sys.argv) > 1 else read_items_interactive()
    if not items:
        print("No inputs.")
        return

    total_mm, expr = soulver_mm_sum(items)
    total_in = total_mm / 25.4
    dec_in  = f'{total_in:.2f}"'
    frac_in = frac_1_16(total_in)
    mm_str  = f"{round(total_mm)} mm"

    print("\nExpression:")
    print(f"  {expr}")
    print("\nResult:")
    print(f"  {dec_in}\n  {frac_in}\n  {mm_str}")

    if PBCOPY:
        subprocess.run([PBCOPY], input=f"{dec_in}\n{frac_in}\n{mm_str}\n", text=True)

if __name__ == "__main__":
    main()
