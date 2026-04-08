---
tags:
    - Api
    - Reaction
icon: lucide/zap
---

# Reaction

## Overview

The `Reaction` class represents a chemical reaction in JAFF, containing reactants, products, rate expressions, and temperature ranges. Reactions are the core building blocks of chemical networks.

```python
from jaff import Network

net = Network("networks/react_COthin")

# Access reactions
for rxn in net.reactions:
    print(f"{rxn.verbatim}")
    print(f"  Rate: {rxn.rate}")
    print(f"  Type: {rxn.guess_type()}")
```

## Class Definition

```python
class Reaction:
    def __init__(self, reactants, products, rate, tmin, tmax, dE, original_string, errors=False):
        """
        Initialize a reaction.

        Args:
            reactants: List of Species objects consumed
            products: List of Species objects produced
            rate: Sympy expression or string for reaction rate
            tmin: Minimum temperature (K) or None
            tmax: Maximum temperature (K) or None
            dE: Energy change or activation energy
            original_string: Original reaction string from file
            errors: If True, exit on conservation errors
        """
```

## Attributes

| Attribute             | Type              | Description                                       |
| --------------------- | ----------------- | ------------------------------------------------- |
| `reactants`           | list              | List of Species objects consumed in the reaction  |
| `products`            | list              | List of Species objects produced in the reaction  |
| `rate`                | sympy.Expr or str | Symbolic expression for reaction rate coefficient |
| `tmin`                | float or None     | Minimum valid temperature (K)                     |
| `tmax`                | float or None     | Maximum valid temperature (K)                     |
| `dE`                  | float             | Energy change or activation energy                |
| `original_string`     | str               | Original reaction string from input file          |
| `verbatim`            | str               | Human-readable equation (e.g., "H + H -> H2")     |
| `serialized`          | str               | Serialized form using species names               |
| `serialized_exploded` | str               | Serialized form using atomic composition          |
| `xsecs`               | dict or None      | Cross-section data for photochemical reactions    |

## Accessing Reactions

### By Index

```python
# Get first reaction
rxn = net.reactions[0]
print(rxn.verbatim)  # "H + H -> H2"

# Iterate over all reactions
for i, rxn in enumerate(net.reactions):
    print(f"{i}: {rxn.verbatim}")
```

### Total Count

```python
nreact = len(net.reactions)
print(f"Network has {nreact} reactions")
```

## Core Methods

### `__repr__()`

Returns the verbatim string representation.

```python
rxn = net.reactions[0]
print(rxn)  # Calls __repr__, outputs: "H + H -> H2"
```

### `guess_type()`

Guess the reaction type based on the rate expression.

```python
rxn_type = rxn.guess_type()
# Returns: "photo", "cosmic_ray", "photo_av", "3_body", or "unknown"

# Example usage
for rxn in net.reactions:
    rtype = rxn.guess_type()
    if rtype == "photo":
        print(f"Photochemical: {rxn.verbatim}")
```

**Reaction Types:**

- `"photo"` - Photochemical reaction (rate contains `photorates` function)
- `"cosmic_ray"` - Cosmic ray induced (rate contains `crate` variable)
- `"photo_av"` - Photo-reaction with extinction (rate contains `av` variable)
- `"3_body"` - Three-body reaction (rate contains `ntot` variable)
- `"unknown"` - Thermal or other type

### `is_same()`

Check if two reactions are identical.

```python
if rxn1.is_same(rxn2):
    print("Reactions are identical")
```

Compares serialized forms (reactants and products).

### `is_isomer_version()`

Check if reaction is an isomer version of another.

```python
if rxn1.is_isomer_version(rxn2):
    print("Same composition, different species names")
```

Returns True if reactions have same atomic composition but different species names (e.g., H2O+ vs OH2+).

## Conservation Checks

### `check_mass()`

Check if mass is conserved.

```python
if not rxn.check_mass():
    print(f"WARNING: Mass not conserved in {rxn.verbatim}")
```

Returns True if mass difference is less than electron mass tolerance.

### `check_charge()`

Check if charge is conserved.

```python
if not rxn.check_charge():
    print(f"WARNING: Charge not conserved in {rxn.verbatim}")
```

Returns True if total charge of reactants equals total charge of products.

### `check()`

Run both mass and charge checks.

```python
rxn.check(errors=True)  # Exit on error
rxn.check(errors=False)  # Only print warnings
```

## String Representations

### `get_verbatim()`

Get human-readable equation string.

```python
equation = rxn.get_verbatim()
# Returns: "H + H -> H2"
```

### `get_latex()`

Get LaTeX formatted equation.

```python
latex_eq = rxn.get_latex()
# Returns: "${\rm H} + {\rm H} \to {\rm H_{2}}$"

# Use in Jupyter notebooks
from IPython.display import display, Latex
display(Latex(rxn.get_latex()))
```

### `serialize()` and `serialize_exploded()`

Get serialized forms for comparison.

```python
# Serialize using species names
ser = rxn.serialize()
# Returns: "H_H__H2" (format: reactants__products)

# Serialize using atomic composition
ser_exp = rxn.serialize_exploded()
# Returns: "H/H__H/H" (sorted atomic elements)
```

## Species Filtering

### `has_any_species()`

Check if species appears in reaction.

```python
if rxn.has_any_species("H2O"):
    print("H2O is involved")

# Multiple species
if rxn.has_any_species(["H2O", "OH"]):
    print("Water or hydroxyl involved")
```

### `has_reactant()`

Check if species is a reactant.

```python
if rxn.has_reactant("H2"):
    print("H2 is consumed")

# Multiple species
h2_consumers = [r for r in net.reactions if r.has_reactant(["H2", "H"])]
```

### `has_product()`

Check if species is a product.

```python
if rxn.has_product("H2O"):
    print("H2O is produced")

# Find all reactions producing water
water_makers = [r for r in net.reactions if r.has_product("H2O")]
```

## Code Generation

### `get_code()`

Generate code for the rate expression.

```python
# C++ code
cpp_code = rxn.get_code(lang="cxx")
# Returns: "2.5e-10*pow(tgas, 0.5)"

# Python code
py_code = rxn.get_code(lang="python")
# Returns: "2.5e-10*tgas**0.5"

# Fortran code
f_code = rxn.get_code(lang="fortran")

# Other supported languages: "c", "rust", "julia", "r"
```

**Supported Languages:**

- `"python"` - Python code
- `"c"` - C code
- `"cxx"` - C++ code
- `"fortran"` - Fortran code
- `"rust"` - Rust code
- `"julia"` - Julia code
- `"r"` - R code

### `get_flux_expression()`

Generate flux expression for ODE systems.

```python
flux = rxn.get_flux_expression(
    idx=0,
    rate_variable="k",
    species_variable="y",
    brackets="[]",
    idx_prefix=""
)
# Returns: "k[0] * y[idx_h] * y[idx_h]"

# Custom variables
flux = rxn.get_flux_expression(
    idx=5,
    rate_variable="rates",
    species_variable="conc",
    brackets="()",
    idx_prefix="n_"
)
```

**Parameters:**

- `idx` - Reaction index
- `rate_variable` - Name of rate array
- `species_variable` - Name of species array
- `brackets` - Bracket style: `"[]"`, `"()"`, or `"{}"`
- `idx_prefix` - Prefix for species indices

### `get_sympy()`

Get rate as sympy expression.

```python
import sympy

rate_expr = rxn.get_sympy()

# Symbolic manipulation
tgas = sympy.Symbol('tgas')
derivative = sympy.diff(rate_expr, tgas)

# Evaluate numerically
rate_func = sympy.lambdify(tgas, rate_expr, "numpy")
import numpy as np
temperatures = np.logspace(1, 4, 100)
rates = rate_func(temperatures)
```

## Visualization

### `plot()`

Plot reaction rate vs temperature.

```python
import matplotlib.pyplot as plt

# Single reaction
rxn.plot()

# Multiple reactions
fig, ax = plt.subplots()
for rxn in net.reactions[:5]:
    rxn.plot(ax=ax)
plt.legend([r.verbatim for r in net.reactions[:5]])
plt.show()
```

Uses temperature range from `tmin`/`tmax` if available, otherwise defaults to 2.73-1e6 K.

### `plot_xsecs()`

Plot photochemical cross-sections.

```python
# Plot in eV (default)
photo_rxn.plot_xsecs()

# Plot as wavelength in nanometers
photo_rxn.plot_xsecs(energy_unit="nm")

# Plot in micrometers with linear scales
photo_rxn.plot_xsecs(
    energy_unit="um",
    energy_log=False,
    xsecs_log=False
)
```

**Parameters:**

- `ax` - Matplotlib axis (optional)
- `energy_unit` - `"eV"`, `"erg"`, `"nm"`, or `"um"`/`"micron"`
- `energy_log` - Logarithmic energy axis (default: True)
- `xsecs_log` - Logarithmic cross-section axis (default: True)

Only works for reactions with `xsecs` data (photochemical reactions).

## Rate Expression Variables

Common variables in rate expressions:

| Variable               | Description                 | Units      |
| ---------------------- | --------------------------- | ---------- |
| `tgas`                 | Gas temperature             | K          |
| `av`                   | Visual extinction           | magnitudes |
| `ntot`                 | Total number density        | cm⁻³       |
| `crate`                | Cosmic ray ionization rate  | s⁻¹        |
| `photorates(idx, ...)` | Photochemical rate function | s⁻¹        |

## See Also

- [Species API](species.md) - Chemical species representation
- [Network API](network.md) - Reaction network container
- [Working with Reactions](../user-guide/reactions.md) - User guide

Notes

- Reactions are typically created by loading network files, not by direct instantiation
- Mass conservation checks allow for small numerical errors (electron mass tolerance)
- Charge conservation must be exact (integer charge values)
- Rate expressions are stored as sympy expressions for symbolic manipulation
- Cross-section data (`xsecs`) is only available for photochemical reactions
- Temperature ranges (`tmin`/`tmax`) are optional and used primarily for plotting
- The `serialized` forms are used internally for reaction comparison and duplicate detection
