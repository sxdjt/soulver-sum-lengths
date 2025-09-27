# soulver-sum-lengths

A small Python wrapper around the [Soulver CLI](https://documentation.soulver.app/) for adding any number of lengths in mixed units.  
It converts and sums your inputs, then prints:

- Decimal inches (to 2 decimal places)
- Fractional inches (nearest 1/16″)
- Total in millimeters

Supports both **interactive mode** (prompt until blank line) and **command-line arguments**.

Defaults to inches unless otherwise specified.

---

## Example

```bash
python soulver-sum-lengths.py '2 1/2" + 5.535" + 9mm'
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

You can also pass separate arguments (shell-friendly):

```bash
python soulver-sum-lengths.py 2.5 5.535 9mm
```

Or run interactively:

```bash
python soulver-sum-lengths.py
Enter lengths (e.g., 2 1/2", 5.535", 9mm). Empty line to finish.
> 2 1/2
> 5.535
> 9mm
>
```

---

## Features

- Accepts fractions (`3 1/2"`, `1/8"`)
- Accepts feet-inch combos (`5' 3 1/2"` → `5 feet + 3 1/2 inches`)
- Accepts mixed units (`mm`, `cm`, `inches`, `feet`)
- Works interactively or from command-line args
- Shows the exact expression sent to Soulver for validation
- Copies result to clipboard automatically on macOS (if `pbcopy` exists)

---

## Requirements

- [Soulver CLI](https://documentation.soulver.app/cli/) installed and on `PATH`

  ```bash
  brew install soulver-cli
  ```

---

## Installation

Clone and run directly:

```bash
git clone https://github.com/sxdjt/soulver-sum.git
cd soulver-sum
python3 soulver-sum-lengths.py 2in 3in 4mm
```

(Optional) make executable:

```bash
chmod +x soulver-sum-lengths.py
./soulver-sum-lengths.py 2in 3in 4mm
```

---

## Why

Soulver handles parsing and unit conversion, but summing multiple measurements from the CLI is clunky.  
This script collects multiple entries, normalizes them, and calls Soulver once for a clean result.

---

## License

MIT – do whatever you like, but attribution appreciated.
