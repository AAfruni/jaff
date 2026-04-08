---
tags:
    - User-guide
    - Network
icon: lucide/arrow-up-from-line
---

# Loading Networks

## Overview

JAFF can load chemical reaction networks from multiple file formats commonly used in astrochemistry. The `Network` class automatically detects the format and parses the file appropriately.

```python
from jaff import Network

# Load a network - format is auto-detected
net = Network("networks/react_COthin")
```

## Basic Loading

### Simple Loading

The simplest way to load a network:

```python
from jaff import Network

# Load network from file
net = Network("path/to/network.dat")

# Access network properties
print(f"Loaded: {net.label}")
print(f"Species: {len(net.species)}")
print(f"Reactions: {len(net.reactions)}")
```

### With Error Checking

Enable validation to catch issues:

```python
# Enable error checking
net = Network("mynetwork.dat", errors=True)
```

This will raise exceptions if the network has:

- Species that only appear as reactants (sinks)
- Species that only appear as products (sources)
- Duplicate reactions
- Isomer issues
- Invalid reaction formatting

### Custom Labels

Specify a custom label for the network:

```python
# Default label is the filename
net1 = Network("networks/react_COthin")
print(net1.label)  # "react_COthin"

# Custom label
net2 = Network("networks/react_COthin", label="CO_chemistry")
print(net2.label)  # "CO_chemistry"
```

## Supported Formats

JAFF automatically detects and parses multiple network file formats.

### KROME Format

KROME network files with format specification:

```text
@format:idx,R,R,R,P,P,P,P,tmin,tmax,rate
1,H,O,,,OH,,,0,1e4,1.2e-10*(tgas/300)**0.5
2,H2,O,,,OH,H,,0,1e4,3.4e-11*exp(-500/Tgas)

# Variables
@var:te=tgas*8.617343e-5
@var:invtgas=1.0/tgas
```

### KIDA Format

Kinetic Database for Astrochemistry format:

```text
H + O -> OH : 1.2e-10 : 0.5 : 0.0
H2 + O -> OH + H : 3.4e-11 : 0.0 : 500.0
```

**Format:** `Reactants -> Products : α : β : γ`

Where rate = $\alpha \left(\frac{T}{300}\right)^\beta e^{\left(-\frac{\gamma}{T}\right)}$

### UDFA Format

UMIST Database for Astrochemistry format:

```text
H:O:OH:1.2e-10:0.5:0.0:0:1e4
H2:O:OH:H:3.4e-11:0.0:500.0:0:1e4
```

### PRIZMO Format

PRIZMO format with variable blocks:

```text
VARIABLES{
    k1 = 1.2e-10
    k2 = 3.4e-11
    sqrtt = sqrt(tgas)
}

H + O -> OH, k1 * sqrtt
H2 + O -> OH + H, k2 * exp(-500/tgas)
```

### UCLCHEM Format

UCL_CHEM format with NAN placeholders:

```text
H,O,NAN,OH,NAN,NAN,1.2e-10,0.5,0.0
H2,O,NAN,OH,H,NAN,3.4e-11,0.0,500.0
```

## Advanced Loading

### Auxiliary Function Files

Use custom rate function definitions:

```python
# Load with auxiliary functions
net = Network(
    "network.dat",
    funcfile="aux_functions.txt"
)
```

Auxiliary function file format:

```text
# Define custom functions
@function function_name(arg1, arg2)
expression # Eg: arg1 + arg2
return expression
```

JAFF also detects ausilary function files automatically if the file name extension ends with `_functions`
**Example**: `network.dat` will have a network file as `network.dat_functions`

### Hydrogen Nuclei Replacement

Control replacement of hydrogen nuclei density symbol with the total computed abundance over species:

```python
# Enable replacement (default)
net = Network("network.dat", replace_nH=True)

# Disable replacement
net = Network("network.dat", replace_nH=False)
```

### JAFF Binary Format

For faster loading of large networks, save to JAFF binary format:

```python
# First load and save
net = Network("large_network.dat")
net.to_jaff_file("large_network.jaff")

# Future loads are much faster
net = Network("large_network.jaff")
```

<!--
**Performance comparison:**

- Text format: ~10-30 seconds for large networks
- JAFF format: <1 second
-->

## Error Handling

### Validation Warnings

When `errors=False` (default), validation issues produce warnings:

```python
net = Network("network.dat", errors=False)
# Output:
# WARNING: Species 'X' only appears as reactant
# WARNING: Duplicate reaction found: H + O -> OH
```

## See Also

- [Network Formats](network-formats.md) - Detailed format specifications
- [Network API](../api/network.md) - Network class reference

---

**Next:** Learn about [Network File Formats](network-formats.md) in detail.
