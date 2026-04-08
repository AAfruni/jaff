---
tags:
    - User-guide
    - Code-generation
icon: lucide/terminal
---

# Jaffgen Command

## Overview

`jaffgen` is the command-line interface for JAFF code generation. It processes template files containing JAFF directives and generates code for chemical reaction networks in multiple programming languages.

## Basic Usage

```bash
jaffgen --network <network_file> [options]
```

### Required Arguments

| Argument    | Description                            |
| ----------- | -------------------------------------- |
| `--network` | Path to chemical reaction network file |

### Optional Arguments

| Argument     | Description                                                     | Default              |
| ------------ | --------------------------------------------------------------- | -------------------- |
| `--outdir`   | Output directory for generated files                            | `src/jaff/generated` |
| `--indir`    | Directory containing template files (Does recursive templating) | None                 |
| `--files`    | Individual template files to process                            | None                 |
| `--template` | Name of predefined template collection                          | None                 |
| `--lang`     | Default language for files without language detection           | Auto-detect          |

## Input Sources

You can combine multiple input sources in a single command:

### 1. Template Directory (`--indir`)

Process all files in a directory:

```bash
jaffgen --network networks/react_COthin --indir templates/ --outdir output/
```

### 2. Predefined Templates (`--template`)

Use built-in template collections from `jaff/templates/generator/`:

```bash
jaffgen --network networks/react_COthin --template kokkos_ode --outdir output/
```

**Available Templates:**

- `kokkos_ode` - Kokkos-based ODE solver templates
- `microphysics` - Microphysics integration templates
- `python_solve_ivp` - Simple initial value proble using python
- `fortran_dlsodes` - Fortran dlsodes template

### 3. Individual Files (`--files`)

Process specific template files:

```bash
jaffgen --network networks/test.dat --files rates.cpp odes.cpp --outdir output/
```

### 4. Combined Sources

Mix different input sources:

```bash
jaffgen --network networks/test.dat --template microphysics --indir templates/kokkos_ode --files custom.cpp --outdir output/
```

## Language Support

JAFF supports automatic language detection from file extensions. If a file extension is unsupported, you will need to specify the --lang option, the code will crash otherwise

### Supported Languages

| Language | Aliases             | File Extensions        |
| -------- | ------------------- | ---------------------- |
| C        | `c`                 | `.c`, `.h`             |
| C++      | `cxx`, `cpp`, `c++` | `.cpp`, `.cxx`, `.hpp` |
| Fortran  | `fortran`, `f90`    | `.f90`, `.F90`         |
| Python   | `python`, `py`      | `.py`                  |
| Rust     | `rust`, `rs`        | `.rs`                  |
| Julia    | `julia`, `jl`       | `.jl`                  |

> NOTE: The supported extensions are case independent

### Specifying Language

```bash
jaffgen --network networks/test.dat --files template.txt --lang rust --outdir output/
```

## Output

Generated files are written to the output directory with the same filename as the template:

```bash
jaffgen --network net.dat --files rates.cpp --outdir generated/
# Creates: generated/rates.cpp
```

**Output Directory Behavior:**

- If `--outdir` is not specified, files are generated in `jaff/generated/`
- The output directory is created if it doesn't exist
- Existing files are overwritten without warning

## See Also

- [Template Syntax](template-syntax.md) - Complete JAFF template command reference
- [Getting Started](../getting-started/quickstart.md) - Introduction to JAFF

---

**Next:** Learn about [Template Syntax](template-syntax.md) to create your own templates.
