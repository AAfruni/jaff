---
tags:
    - User-guide
    - Code-generation
icon: lucide/blocks
---

# Using the Builder

## Overview

The `Builder` class provides a high-level interface for generating complete simulation code using pre-existing templates from chemical reaction networks.

```python
from jaff import Network, Builder

# Load network
net = Network("networks/react_COthin")

# Build simulation code
builder = Builder(net)
output_dir = builder.build(template="python_solve_ivp")

print(f"Code generated in: {output_dir}")
```

## Basic Usage

### Creating a Builder

```python
from jaff import Network, Builder

# Load your network
net = Network("networks/react_COthin")

# Create builder
builder = Builder(net)
```

The builder holds a reference to your network and provides methods to generate code using different templates.

### Building with a Template

```python
# Build using default output directory (current working directory)
output_dir = builder.build(template="python_solve_ivp")

# Build to specific output directory
output_dir = builder.build(
    template="python_solve_ivp",
    output_dir="generated_code/"
)
```

## Available Templates

JAFF includes several predefined templates for common use cases:

### python_solve_ivp

Generate Python code using SciPy's `solve_ivp` for ODE integration.

```python
builder.build(template="python_solve_ivp", output_dir="python_code/")
```

**Generated files:**

- `commons.py` - Species indices and constants
- `rates.py` - Rate coefficient calculations
- `fluxes.py` - Reaction flux expressions
- `ode.py` - ODE system definition
- `main.py` - Example simulation script

**Use case:** Rapid prototyping, testing, small to medium networks

### kokkos_ode

Generate C++ code using Kokkos-kernels BDF solver.

```python
builder.build(template="kokkos_ode", output_dir="cpp_code/")
```

**Generated files:**

- `chemistry_ode.hpp` - Chemistry ODE class header
- `chemistry_ode.cpp` - Main executable
- `CMakeLists.txt` - CMake build configuration

**Use case:** High-performance computing, GPU acceleration, large networks

### fortran_dlsodes

Generate Fortran code using the DLSODES stiff ODE solver.

```python
builder.build(template="fortran_dlsodes", output_dir="fortran_code/")
```

**Generated files:**

- `chemistry_module.f90` - Chemistry module
- `solver.f90` - DLSODES integration
- `main.f90` - Main program

**Use case:** Legacy code integration, established Fortran workflows

### microphysics

Generate Fortran code compatible with AMReX microphysics framework.

```python
builder.build(template="microphysics", output_dir="microphysics_code/")
```

**Generated files:**

- Network-specific files for AMReX integration

**Use case:** Astrophysics simulations using AMReX

## Template Comparison

| Template           | Language | Solver         | Best For                |
| ------------------ | -------- | -------------- | ----------------------- |
| `python_solve_ivp` | Python   | BDF/LSODA      | Testing, prototyping    |
| `kokkos_ode`       | C++      | BDF (Kokkos)   | HPC, GPU, performance   |
| `fortran_dlsodes`  | Fortran  | DLSODES        | Legacy integration      |
| `microphysics`     | Fortran  | AMReX-specific | Astrophysics with AMReX |

## Working with Generated Code

### Python Template

```python
# Generate code
builder.build(template="python_solve_ivp", output_dir="output/")

# Use generated code
import sys
sys.path.insert(0, "output/")

from commons import nspecs, idx_h, idx_h2
from rates import get_rates
from ode import ode_system
import numpy as np

# Initial conditions
y0 = np.zeros(nspecs)
y0[idx_h] = 1.0e4
y0[idx_h2] = 1.0e3

# Compute rates
tgas = 300.0
crate = 1.3e-17
av = 1.0
k = get_rates(tgas, crate, av)

# Evaluate ODE
t = 0.0
dydt = ode_system(t, y0, k)

print(f"H destruction rate: {dydt[idx_h]}")
```

### C++ Template

```python
# Generate code
builder.build(template="kokkos_ode", output_dir="cpp_build/")
```

```bash
# Compile
cd cpp_build/
mkdir build && cd build
cmake ..


# Run
./chemistry_ode
```

### Fortran Template

```python
# Generate code
builder.build(template="fortran_dlsodes", output_dir="fortran_build/")
```

```bash
# Compile
cd fortran_build/
gfortran -o solver chemistry_module.f90 solver.f90 main.f90 -ldlsodes

# Run
./solver
```

**Available templates are listed from:**

```
src/jaff/templates/preprocessor/
├── python_solve_ivp/
├── kokkos_ode/
├── fortran_dlsodes/
└── microphysics/
```

## See Also

- [Code Generation](code-generation.md) - Detailed code generation guide
- [Working with Networks](loading-networks.md) - Loading network files
- [Codegen API](../api/codegen.md) - Low-level code generation

---

**Next:** Learn about [Code Generation](code-generation.md) internals.
