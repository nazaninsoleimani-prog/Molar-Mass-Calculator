"""
Molar mass calculator.

Supports simple formulas (H2O, H2SO4), parentheses (Ca(OH)2, Al2(SO4)3),
and reports total molar mass plus per-element mass percent.
"""

from __future__ import annotations

import re
from typing import Dict, List, Tuple

from periodic_table import atomic_masses

# Matches an element symbol and optional count: H, H2, Cl, Cl2, ...
_ELEMENT_RE = re.compile(r"([A-Z][a-z]?)(\d*)")
# Matches the innermost parenthesized group and optional multiplier
_PAREN_RE = re.compile(r"\(([A-Za-z0-9]+)\)(\d*)")
# Allowed characters in a formula (after strip)
_FORMULA_CHARS_RE = re.compile(r"^[A-Za-z0-9()]+$")


def expand_parentheses(formula: str) -> str:
    """Expand groups like (OH)2 into O2H2 until no parentheses remain.

    Handles nested groups by always expanding the innermost match first.
    Example: Al2(SO4)3 -> Al2S3O12
    """
    while True:
        match = _PAREN_RE.search(formula)
        if not match:
            break
        group, mult_str = match.group(1), match.group(2)
        mult = int(mult_str) if mult_str else 1
        parts = _ELEMENT_RE.findall(group)
        expanded = "".join(
            f"{element}{int(count or 1) * mult}" for element, count in parts
        )
        formula = formula[: match.start()] + expanded + formula[match.end() :]
    if "(" in formula or ")" in formula:
        raise ValueError(
            "Unbalanced or invalid parentheses in formula "
            f"(remaining: {formula!r})."
        )
    return formula


def parse_formula(formula: str) -> Dict[str, int]:
    """Parse a chemical formula into {element: total_count}.

    Combines repeated elements (e.g. CH3COOH -> C:2, H:4, O:2).
    Supports parentheses via expand_parentheses.
    """
    formula = formula.strip()
    if not formula:
        raise ValueError("Please enter a formula (e.g. H2O or Ca(OH)2).")
    if not _FORMULA_CHARS_RE.fullmatch(formula):
        raise ValueError(
            "Invalid characters in formula. "
            "Use element symbols, digits, and parentheses only."
        )

    expanded = expand_parentheses(formula)
    parts = _ELEMENT_RE.findall(expanded)
    if not parts:
        raise ValueError(f"Could not parse formula: {formula!r}")

    counts: Dict[str, int] = {}
    for element, number in parts:
        if element not in atomic_masses:
            raise ValueError(f"Unknown element: {element}")
        count = int(number) if number else 1
        counts[element] = counts.get(element, 0) + count
    return counts


def molar_mass(formula: str) -> float:
    """Return the molar mass of the formula in g/mol."""
    counts = parse_formula(formula)
    return sum(atomic_masses[el] * n for el, n in counts.items())


def mass_percent(formula: str) -> Dict[str, float]:
    """Return mass percent for each element in the formula."""
    counts = parse_formula(formula)
    total = sum(atomic_masses[el] * n for el, n in counts.items())
    if total <= 0:
        raise ValueError("Total mass is zero; check the formula.")
    return {
        el: atomic_masses[el] * n / total * 100 for el, n in counts.items()
    }


def breakdown(formula: str) -> List[Tuple[str, int, float, float, float]]:
    """Return rows: (element, count, atomic_mass, contribution, percent)."""
    counts = parse_formula(formula)
    total = sum(atomic_masses[el] * n for el, n in counts.items())
    rows: List[Tuple[str, int, float, float, float]] = []
    for el, n in counts.items():
        am = atomic_masses[el]
        contrib = am * n
        pct = contrib / total * 100
        rows.append((el, n, am, contrib, pct))
    return rows


def print_breakdown(formula: str) -> float:
    """Print a table of element contributions and return total molar mass."""
    rows = breakdown(formula)
    total = sum(row[3] for row in rows)

    print(f"Formula: {formula}")
    print(f"{'Element':<10}{'Count':>8}{'Atomic mass':>14}{'Contribution':>14}{'%':>10}")
    print("-" * 56)
    for el, count, am, contrib, pct in rows:
        print(f"{el:<10}{count:>8}{am:>14.3f}{contrib:>14.3f}{pct:>9.2f}%")
    print("-" * 56)
    print(f"{'Total':<10}{'':>8}{'':>14}{total:>14.3f}{'100.00':>10}%")
    print(f"\nMolar mass = {total:.3f} g/mol")
    return total


def analyze(formula: str) -> None:
    """Interactive-friendly entry: print breakdown or a clear error."""
    try:
        print_breakdown(formula)
    except ValueError as exc:
        print(f"Error: {exc}")


if __name__ == "__main__":
    user_formula = input("Enter chemical formula: ").strip()
    analyze(user_formula)
