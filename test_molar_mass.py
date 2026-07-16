"""Simple tests for the molar mass calculator."""

import unittest

from molar_mass import (
    breakdown,
    expand_parentheses,
    mass_percent,
    molar_mass,
    parse_formula,
)


class TestExpandParentheses(unittest.TestCase):
    def test_simple_group(self):
        self.assertEqual(expand_parentheses("Ca(OH)2"), "CaO2H2")

    def test_multiple_in_group(self):
        self.assertEqual(expand_parentheses("Al2(SO4)3"), "Al2S3O12")

    def test_no_parentheses(self):
        self.assertEqual(expand_parentheses("H2SO4"), "H2SO4")


class TestParseFormula(unittest.TestCase):
    def test_water(self):
        self.assertEqual(parse_formula("H2O"), {"H": 2, "O": 1})

    def test_sulfuric_acid(self):
        self.assertEqual(parse_formula("H2SO4"), {"H": 2, "S": 1, "O": 4})

    def test_repeated_elements(self):
        # Acetic acid written as CH3COOH
        self.assertEqual(parse_formula("CH3COOH"), {"C": 2, "H": 4, "O": 2})

    def test_parentheses(self):
        self.assertEqual(parse_formula("Ca(OH)2"), {"Ca": 1, "O": 2, "H": 2})

    def test_empty_raises(self):
        with self.assertRaises(ValueError):
            parse_formula("")

    def test_unknown_element_raises(self):
        with self.assertRaises(ValueError) as ctx:
            parse_formula("Xx2")
        self.assertIn("Unknown element", str(ctx.exception))

    def test_invalid_characters_raises(self):
        with self.assertRaises(ValueError):
            parse_formula("H2O!")


class TestMolarMass(unittest.TestCase):
    def test_water(self):
        self.assertAlmostEqual(molar_mass("H2O"), 18.015, places=3)

    def test_sulfuric_acid(self):
        self.assertAlmostEqual(molar_mass("H2SO4"), 98.072, places=3)

    def test_nacl(self):
        # Na 22.990 + Cl 35.45
        self.assertAlmostEqual(molar_mass("NaCl"), 58.44, places=2)

    def test_caoh2(self):
        # Ca 40.078 + 2*O 15.999 + 2*H 1.008 = 74.092
        self.assertAlmostEqual(molar_mass("Ca(OH)2"), 74.092, places=3)

    def test_al2so43(self):
        # Al2 2*26.982 + S3 3*32.06 + O12 12*15.999 = 342.132
        self.assertAlmostEqual(molar_mass("Al2(SO4)3"), 342.132, places=3)


class TestMassPercent(unittest.TestCase):
    def test_water_percents(self):
        pct = mass_percent("H2O")
        self.assertAlmostEqual(pct["H"], 11.19, places=1)
        self.assertAlmostEqual(pct["O"], 88.81, places=1)
        self.assertAlmostEqual(sum(pct.values()), 100.0, places=5)


class TestBreakdown(unittest.TestCase):
    def test_row_count(self):
        rows = breakdown("H2SO4")
        elements = {row[0] for row in rows}
        self.assertEqual(elements, {"H", "S", "O"})
        total = sum(row[3] for row in rows)
        self.assertAlmostEqual(total, molar_mass("H2SO4"), places=5)


if __name__ == "__main__":
    unittest.main()
