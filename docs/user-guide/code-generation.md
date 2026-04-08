---
tags:
    - User-guide
    - Code-generation
icon: lucide/file-code-corner
---

# Advanced Code Generation

## Overview

In case the [Template Syntax](template-syntax.md) is not sufficient to generate code, jaff provides the ability to completely generate custom code using the **`Codegen`** and
**`Preprocessor`** classes

For template-based generation, see the [Template Syntax](template-syntax.md) guide.

## Quick Start

### Basic Example

```python
from jaff import Network, Codegen
from jaff.preprocessor import Preprocessor

# Load network
net = Network("networks/react_COthin")

# Create code generator for C++
cg = Codegen(network=net, lang="cxx")

# Generate code strings
commons = cg.get_commons()
rates = cg.get_rates_str(use_cse=True)
odes = cg.get_ode_str(use_cse=True)

# Create preprocessor
p = Preprocessor()

# Process template files
p.preprocess(
    path="templates/",
    fnames=["chemistry.cpp"],
    dictionaries=[{
        "COMMONS": commons,
        "RATES": rates,
        "ODES": odes
    }],
    comment="//",
    path_build="generated/"
)
```

## The Codegen Class

The `Codegen` class generates code strings for rates, ODEs, Jacobians, and more.

### Initialization

```python
from jaff import Network, Codegen

net = Network("networks/react_COthin")
cg = Codegen(network=net, lang="cxx")
```

**Supported Languages:**

| Language | Alias Options                 |
| -------- | ----------------------------- |
| C        | `"c"`                         |
| C++      | `"cxx"`, `"cpp"`, `"c++"`     |
| Fortran  | `"fortran"`, `"f90"`, `"f95"` |
| Python   | `"python"`, `"py"`            |
| Rust     | `"rust"`, `"rs"`              |
| Julia    | `"julia"`, `"jl"`             |
| R        | `"r"`                         |

### Key Methods

#### 1. `get_commons()`

Generate species indices and network constants.

```python
commons = cg.get_commons(
    idx_offset=0,              # Start index (0 for C/C++, 1 for Fortran)
    idx_prefix="",             # Prefix for index variables
    definition_prefix="const " # Variable declaration prefix
)
```

**Example Output (C++):**

```cpp
const int idx_h = 0;
const int idx_h2 = 1;
const int idx_o = 2;
const int nspecs = 35;
const int nreactions = 127;
```

**Example Output (Fortran):**

```fortran
commons = cg.get_commons(
    idx_offset=1,
    definition_prefix="integer, parameter :: "
)
# Output:
# integer, parameter :: idx_h = 1
# integer, parameter :: idx_h2 = 2
```

#### 2. `get_rates_str()`

Generate reaction rate coefficient calculations.

```python
rates = cg.get_rates_str(
    idx_offset=0,
    rate_variable="k",
    use_cse=True  # Enable Common Subexpression Elimination
)
```

**Example Output:**

```cpp
// Common subexpressions
const double x0 = sqrt(tgas);
const double x1 = pow(tgas/300.0, 0.5);

// Rate coefficients
k[0] = 1.2e-10 * x1;
k[1] = 3.4e-11 * x0 * exp(-500.0/tgas);
k[2] = 5.6e-12 * x0 * x1;
```

#### 3. `get_ode_str()`

Generate complete ODE system (dydt = f(y, t)).

```python
odes = cg.get_ode_str(
    idx_offset=0,
    use_cse=True,
    include_dedt=False  # Exclude energy equation
)
```

**Example Output:**

```cpp
// Common subexpressions
const double x0 = k[0] * y[0];

// ODE equations
dydt[0] = -x0 - k[1]*y[0]*y[1];
dydt[1] = x0 - k[2]*y[1];
dydt[2] = k[1]*y[0]*y[1] + k[2]*y[1];
```

#### 4. `get_jacobian_str()`

Generate analytical Jacobian matrix.

```python
jacobian = cg.get_jacobian_str(
    idx_offset=0,
    use_cse=True,
    include_dedt=False
)
```

**Example Output:**

```cpp
// Jacobian elements
jac[0, 0] = -k[0] - k[1]*y[1];
jac[1, 0] = -k[1]*y[0];
jac[1, 1] = k[0];
```

#### 5. Other Methods

```python
# Get flux expressions (production - destruction for each reaction)
flux = cg.get_flux_expressions_str()

# Get only ODE expressions (without assignments)
ode_expr = cg.get_ode_expressions_str()

# Get indexed versions (return data structures instead of strings)
indexed_rates = cg.get_indexed_rates(use_cse=True)
indexed_odes = cg.get_indexed_odes(use_cse=True)
```

## The Preprocessor Class

The `Preprocessor` class replaces pragma directives in template files with generated code.

### Pragma Format

Templates use pragma comments to mark replacement points:

```cpp
// C++ template
void compute_rates(double* k, double tgas) {
    // PREPROCESS_RATES

    // PREPROCESS_END
}
```

```fortran
! Fortran template
subroutine compute_rates(k, tgas)
    !! PREPROCESS_RATES

    !! PREPROCESS_END
end subroutine
```

### Basic Usage

```python
from jaff.preprocessor import Preprocessor

p = Preprocessor()

# Generate code
rates_code = cg.get_rates_str(use_cse=True)

# Process template
p.preprocess_file(
    fname="template.cpp",
    dictionary={"RATES": rates_code},
    comment="//",
    add_header=True,
    path_build="generated/"
)
```

**Input Template (`template.cpp`):**

```cpp
void compute_rates(double* k, double tgas) {
    // PREPROCESS_RATES

    // PREPROCESS_END
}
```

**Output (`generated/template.cpp`):**

```cpp
// This file was automatically generated by JAFF.
// This file could be overwritten.

void compute_rates(double* k, double tgas) {
    // PREPROCESS_RATES
    const double x0 = sqrt(tgas);
    k[0] = 1.2e-10 * x0;
    k[1] = 3.4e-11 * exp(-500.0/tgas);
    // PREPROCESS_END
}
```

### Processing Multiple Files

```python
p.preprocess(
    path="templates/",
    fnames=["chemistry.h", "chemistry.cpp", "rates.cpp"],
    dictionaries=[
        {"COMMONS": commons},
        {"RATES": rates, "ODES": odes},
        {"RATES": rates}
    ],
    comment="//",
    path_build="generated/"
)
```

**Features:**

- Each file can have its own dictionary
- Files not in `fnames` are copied unchanged
- Automatic header generation
- Preserves indentation

### Auto-Detecting Comment Style

Use `comment="auto"` to detect comment style from file extension:

```python
p.preprocess(
    path="templates/",
    fnames=["chemistry.cpp", "chemistry.f90", "CMakeLists.txt"],
    dictionaries=[dict_cpp, dict_fortran, dict_cmake],
    comment="auto",  # Auto-detect: //, !!, #
    path_build="generated/"
)
```

**Auto-detection mapping:**

| Extension                   | Comment Style |
| --------------------------- | ------------- |
| `.cpp`, `.hpp`, `.h`, `.cc` | `//`          |
| `.f90`, `.f`, `.F90`        | `!!`          |
| `.py`                       | `#`           |
| `.cmake`, `CMakeLists.txt`  | `#`           |

## Plugin Examples

JAFF includes several example plugins that demonstrate how to combine the Codegen and Preprocessor classes for different target languages and frameworks. These plugins are located in `src/jaff/plugins/` and include:

- **`python_solve_ivp/`** - Python code generation for scipy.integrate.solve_ivp
- **`kokkos_ode/`** - C++ code generation with Kokkos parallel computing support
- **`fortran_dlsodes/`** - Fortran code generation for DLSODES solver
- **`microphysics/`** - Microphysics framework integration

Each plugin directory contains:

- A `plugin.py` script that uses Codegen and Preprocessor to generate code
- Template files with preprocessor pragmas for code injection
- Example usage and documentation

Refer to these plugins for complete, working examples of advanced code generation workflows.

## Common Subexpression Elimination (CSE)

CSE optimizes generated code by identifying and extracting repeated subexpressions.

### Without CSE

```python
rates = cg.get_rates_str(use_cse=False)
```

**Output:**

```cpp
k[0] = 1.2e-10 * sqrt(tgas) * pow(tgas/300.0, 0.5);
k[1] = 3.4e-11 * sqrt(tgas) * exp(-500.0/tgas);
k[2] = 5.6e-12 * sqrt(tgas) * pow(tgas/300.0, 0.5);
```

### With CSE

```python
rates = cg.get_rates_str(use_cse=True)
```

**Output:**

```cpp
// Common subexpressions
const double x0 = sqrt(tgas);
const double x1 = pow(tgas/300.0, 0.5);

// Rate coefficients
k[0] = 1.2e-10 * x0 * x1;
k[1] = 3.4e-11 * x0 * exp(-500.0/tgas);
k[2] = 5.6e-12 * x0 * x1;
```

## Customization

### Custom Variable Names

```python
# Default: k[0], k[1], k[2]
rates = cg.get_rates_str(rate_variable="k")

# Custom: rate[0], rate[1], rate[2]
rates = cg.get_rates_str(rate_variable="rate")

# Custom: krate[0], krate[1], krate[2]
rates = cg.get_rates_str(rate_variable="krate")
```

### Custom Index Offsets

```python
# C/C++/Python: 0-based indexing
rates = cg.get_rates_str(idx_offset=0)
# Output: k[0] = ..., k[1] = ..., k[2] = ...

# Fortran: 1-based indexing
rates = cg.get_rates_str(idx_offset=1)
# Output: k(1) = ..., k(2) = ..., k(3) = ...

# Custom offset
rates = cg.get_rates_str(idx_offset=100)
# Output: k[100] = ..., k[101] = ..., k[102] = ...
```

### Language-Specific Formatting

The Codegen class automatically formats code for the target language:

```python
# C++ formatting
cg_cpp = Codegen(network=net, lang="cxx")
commons_cpp = cg_cpp.get_commons()
# const int idx_h = 0;

# Fortran formatting
cg_f90 = Codegen(network=net, lang="fortran")
commons_f90 = cg_f90.get_commons(idx_offset=1)
# integer :: idx_h = 1

# Python formatting
cg_py = Codegen(network=net, lang="python")
commons_py = cg_py.get_commons()
# idx_h = 0
```

### Advanced Usage

For comprehensive details on all `Codegen` methods, parameters, and advanced features, see the [Codegen API Reference](../api/codegen.md).

## See Also

- [Codegen API](../api/codegen.md) - Complete API reference
- [Template Syntax](template-syntax.md) - For simpler template-based generation
- [jaffgen Command](jaffgen-command.md) - Command-line template processing

---
