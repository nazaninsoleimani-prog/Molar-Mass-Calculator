# Molar Mass Calculator

Calculate the **molar mass** (g/mol) and **mass percent** of chemical compounds in Python.

**Author:** Nazanin Soleimani

## Features

- Simple formulas: `H2O`, `H2SO4`, `NaCl`, `CH3COOH`
- Parentheses / polyatomic groups: `Ca(OH)2`, `Al2(SO4)3`
- Unknown-element and invalid-input error messages
- Element-by-element breakdown table
- Full periodic table data in `periodic_table.py`

## Project layout

```
Molar-Mass-Calculator/
├── Molar-Mass-Calculator.ipynb   # Jupyter demo notebook
├── molar_mass.py                 # parse + calculate functions
├── periodic_table.py             # atomic masses (g/mol)
├── test_molar_mass.py            # unit tests
└── README.md
```

## How to run

### Jupyter notebook

1. Open Jupyter in this folder (or open the notebook from Jupyter Lab / VS Code).
2. Run all cells in `Molar-Mass-Calculator.ipynb`.
3. Enter a formula when prompted, or use the example cells.

### Command line

```bash
cd "C:\Users\nazan\Documents\Pyton Projects\Molar-Mass-Calculator"
python molar_mass.py
```

Or in Python:

```python
from molar_mass import molar_mass, mass_percent, print_breakdown

print(molar_mass("H2SO4"))
print(mass_percent("H2O"))
print_breakdown("Ca(OH)2")
```

### Tests

```bash
cd "C:\Users\nazan\Documents\Pyton Projects\Molar-Mass-Calculator"
python -m unittest test_molar_mass.py -v
```

## Examples

| Formula     | Approx. molar mass |
|-------------|--------------------|
| `H2O`       | 18.015 g/mol       |
| `H2SO4`     | 98.072 g/mol       |
| `NaCl`      | 58.44 g/mol        |
| `Ca(OH)2`   | 74.092 g/mol       |
| `Al2(SO4)3` | 342.132 g/mol      |

## Notes

- Element symbols are **case-sensitive** (`H2O` works; `h2o` does not).
- Atomic masses are standard relative atomic masses in g/mol.
- Nested parentheses are expanded from the inside out.
