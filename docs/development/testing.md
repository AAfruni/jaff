---
tags:
    - Development
    - Testing
icon: lucide/bug
---

# Testing

## Overview

JAFF uses pytest for testing. This guide covers how to write, run, and organize tests.

## Running Tests

### Basic Commands

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_network.py

# Run specific test
pytest tests/test_network.py::test_load_network

# Run tests matching pattern
pytest -k "network"
```

### Coverage

```bash
# Run with coverage
pytest --cov=jaff

# Generate HTML coverage report
pytest --cov=jaff --cov-report=html

# View report
open htmlcov/index.html
```

### Markers

> NOTE: Markers have not yet been added

```bash
# Run only fast tests
pytest -m "not slow"

# Run only slow tests
pytest -m slow

# Run only unit tests
pytest -m unit
```

## Test Organization

### Directory Structure

```
tests/
├── __init__.py
├── conftest.py              # Shared fixtures
├── test_network.py          # Network class tests
├── test_codegen.py          # Codegen class tests
├── test_file_parser.py      # File parser tests
├── test_elements.py         # Elements class tests
├── test_cli.py              # CLI tests
└── fixtures/                # Test data
    ├── networks/
    │   ├── test_small.dat
    │   └── test_krome.dat
    └── templates/
        └── test_template.cpp
```

> NOTE: `networks` and `templates` folder bifurcation will be done once templating tests are added to the test suite

### Test File Structure

```python
"""Tests for Network class."""

import pytest
from jaff import Network


class TestNetwork:
    """Network class tests."""

    def test_load_basic_network(self):
        """Test loading basic network."""
        net = Network("tests/fixtures/networks/test_small.dat")
        assert len(net.species) > 0
        assert len(net.reactions) > 0

    def test_load_krome_format(self):
        """Test loading KROME format."""
        net = Network("tests/fixtures/networks/test_krome.dat")
        assert net.label is not None


class TestNetworkValidation:
    """Network validation tests."""

    def test_duplicate_reactions(self):
        """Test detection of duplicate reactions."""
        # Test implementation
        pass
```

## Writing Tests

### Basic Test

```python
def test_network_species_count():
    """Test species count is correct."""
    net = Network("tests/fixtures/networks/test.dat")
    assert len(net.species) == 35
    assert net.get_number_of_species() == 35
```

### Testing Exceptions

```python
def test_invalid_network_raises_error():
    """Test that invalid network raises error."""
    with pytest.raises(FileNotFoundError):
        Network("nonexistent.dat")

def test_negative_temperature_raises_error():
    """Test negative temperature raises ValueError."""
    net = Network("tests/fixtures/networks/test.dat")
    with pytest.raises(ValueError, match="Temperature must be positive"):
        net.calculate_rates(-100)
```

### Parametrized Tests

```python
@pytest.mark.parametrize("lang,expected_bracket", [
    ("c++", "["),
    ("c", "["),
    ("fortran", "("),
    ("python", "["),
])
def test_codegen_brackets(lang, expected_bracket):
    """Test bracket style for each language."""
    net = Network("tests/fixtures/networks/test.dat")
    cg = Codegen(network=net, lang=lang)
    assert cg.lb == expected_bracket
```

### Parametrized with Multiple Arguments

```python
@pytest.mark.parametrize("filename,expected_species,expected_reactions", [
    ("test_small.dat", 10, 20),
    ("test_medium.dat", 50, 100),
    ("test_large.dat", 200, 500),
])
def test_network_sizes(filename, expected_species, expected_reactions):
    """Test networks load with expected sizes."""
    net = Network(f"tests/fixtures/networks/{filename}")
    assert len(net.species) == expected_species
    assert len(net.reactions) == expected_reactions
```

## Fixtures

### Basic Fixtures

```python
# conftest.py
import pytest
from jaff import Network

@pytest.fixture
def small_network():
    """Small test network."""
    return Network("tests/fixtures/networks/test_small.dat")

@pytest.fixture
def codegen_cpp(small_network):
    """C++ code generator for small network."""
    from jaff import Codegen
    return Codegen(network=small_network, lang="c++")
```

### Using Fixtures

```python
def test_with_fixture(small_network):
    """Test using network fixture."""
    assert len(small_network.species) > 0

def test_code_generation(codegen_cpp):
    """Test code generation."""
    rates = codegen_cpp.get_rates(use_cse=True)
    assert "k[0]" in rates
```

### Fixture Scope

```python
@pytest.fixture(scope="module")
def expensive_network():
    """Module-scoped fixture for expensive setup."""
    # Loaded once per module
    return Network("tests/fixtures/networks/large.dat")

@pytest.fixture(scope="function")
def temp_directory(tmp_path):
    """Function-scoped temporary directory."""
    # New directory for each test
    return tmp_path
```

## Test Data

### Creating Test Networks

```python
# tests/fixtures/networks/test_small.dat
H + O -> OH, 1.2e-10 * (tgas/300)**0.5
H2 + O -> OH + H, 3.4e-11 * exp(-500/tgas)
C + O2 -> CO + O, 5.6e-12
```

### Using Temporary Files

```python
def test_network_save_load(tmp_path):
    """Test saving and loading network."""
    # Create network
    net = Network("tests/fixtures/networks/test.dat")

    # Save to temporary file
    output_file = tmp_path / "test.jaff"
    net.to_jaff_file(str(output_file))

    # Load and verify
    net2 = Network(str(output_file))
    assert len(net2.species) == len(net.species)
```

## Mocking

### Mock External Dependencies

```python
from unittest.mock import Mock, patch

def test_with_mock():
    """Test with mocked function."""
    with patch('jaff.network.open') as mock_open:
        mock_open.return_value.__enter__.return_value.readlines.return_value = [
            "H + O -> OH, 1.2e-10\n"
        ]
        # Test code
```

### Mock Network Loading

```python
@pytest.fixture
def mock_network():
    """Mock network for testing."""
    net = Mock(spec=Network)
    net.species = [Mock(name="H"), Mock(name="O")]
    net.reactions = [Mock()]
    return net

def test_with_mock_network(mock_network):
    """Test using mocked network."""
    assert len(mock_network.species) == 2
```

## Testing Best Practices

### 1. Test One Thing at a Time

```python
# Good
def test_network_loads_successfully():
    """Test network loads without error."""
    net = Network("test.dat")
    assert net is not None

def test_network_has_species():
    """Test network has species."""
    net = Network("test.dat")
    assert len(net.species) > 0

# Avoid
def test_everything():
    """Test everything at once."""
    net = Network("test.dat")
    assert net is not None
    assert len(net.species) > 0
    # ... many more assertions
```

### 2. Use Descriptive Names

```python
# Good
def test_codegen_raises_error_for_unsupported_language():
    """Test that unsupported language raises ValueError."""
    pass

# Avoid
def test_lang():
    pass
```

### 3. Test Edge Cases

```python
def test_empty_network():
    """Test handling of empty network."""
    pass

def test_network_with_one_species():
    """Test network with single species."""
    pass

def test_network_with_duplicate_species():
    """Test handling of duplicate species."""
    pass
```

### 4. Test Error Conditions

```python
def test_file_not_found():
    """Test FileNotFoundError for missing file."""
    with pytest.raises(FileNotFoundError):
        Network("nonexistent.dat")

def test_invalid_format():
    """Test ValueError for invalid format."""
    with pytest.raises(ValueError):
        Network("tests/fixtures/invalid.dat")
```

## Integration Tests

### Testing Complete Workflows

```python
def test_complete_code_generation_workflow(tmp_path):
    """Test complete workflow from network to code."""
    # Load network
    net = Network("tests/fixtures/networks/test.dat")

    # Create code generator
    cg = Codegen(network=net, lang="c++")

    # Generate code
    rates = cg.get_rates(use_cse=True)
    odes = cg.get_ode(use_cse=True)

    # Save to file
    output_file = tmp_path / "chemistry.cpp"
    with open(output_file, 'w') as f:
        f.write(rates)
        f.write("\n\n")
        f.write(odes)

    # Verify file exists and has content
    assert output_file.exists()
    content = output_file.read_text()
    assert "k[0]" in content
    assert "dydt[0]" in content
```

## Performance Tests

### Timing Tests

```python
import time

@pytest.mark.slow
def test_large_network_performance():
    """Test large network loads in reasonable time."""
    start = time.time()
    net = Network("tests/fixtures/networks/large.dat")
    duration = time.time() - start

    assert duration < 30.0  # Should load in < 30 seconds
```

### Memory Tests

```python
import tracemalloc

@pytest.mark.slow
def test_memory_usage():
    """Test memory usage is reasonable."""
    tracemalloc.start()

    net = Network("tests/fixtures/networks/test.dat")
    cg = Codegen(network=net, lang="c++")
    rates = cg.get_rates(use_cse=True)

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # Peak memory should be reasonable
    assert peak < 100 * 1024 * 1024  # < 100 MB
```

## Continuous Integration

### GitHub Actions

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
    test:
        runs-on: ubuntu-latest
        strategy:
            matrix:
                python-version: [3.9, "3.10", 3.11]

        steps:
            - uses: actions/checkout@v3
            - name: Set up Python
              uses: actions/setup-python@v4
              with:
                  python-version: ${{ matrix.python-version }}
            - name: Install dependencies
              run: |
                  pip install -e ".[dev]"
            - name: Run tests
              run: |
                  pytest --cov=jaff --cov-report=xml
            - name: Upload coverage
              uses: codecov/codecov-action@v3
```

## Coverage Goals

- **Overall coverage**: > 80%
- **Critical modules**: > 90%
- **New code**: 100% coverage required

### Check Coverage

```bash
# Generate coverage report
pytest --cov=jaff --cov-report=term-missing

# Show lines not covered
pytest --cov=jaff --cov-report=html
open htmlcov/index.html
```

## Troubleshooting Tests

### Test Failures

```bash
# Run with detailed output
pytest -vv

# Show print statements
pytest -s

# Stop at first failure
pytest -x

# Run last failed tests
pytest --lf
```

### Debugging Tests

```python
def test_debug_example():
    """Test with debugging."""
    net = Network("test.dat")

    # Add breakpoint
    import pdb; pdb.set_trace()

    # Or use pytest's built-in
    pytest.set_trace()

    assert len(net.species) > 0
```

## Test Markers

### Defining Markers

```python
# pytest.ini or pyproject.toml
[tool.pytest.ini_options]
markers = [
    "slow: marks tests as slow",
    "unit: unit tests",
    "integration: integration tests",
    "network: network-related tests",
]
```

### Using Markers

```python
@pytest.mark.slow
def test_large_network():
    """Slow test."""
    pass

@pytest.mark.unit
def test_species_creation():
    """Unit test."""
    pass

@pytest.mark.integration
@pytest.mark.network
def test_full_workflow():
    """Integration test for network workflow."""
    pass
```

## See Also

- [Contributing Guide](contributing.md)
- [Code Style Guide](code-style.md)
- [pytest Documentation](https://docs.pytest.org/)
