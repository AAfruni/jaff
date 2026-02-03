#!/usr/bin/env python3
# Test module to verify if jacobian works properly

from pathlib import Path
from typing import List

import pytest

from jaff.network import Network


@pytest.fixture
def test_network():
    """Load the test network with a fake rate expression"""

    network_file = Path(__file__).parent / "fixtures" / "test_jac.dat"
    if not network_file.exists():
        pytest.skip(f"Test network file not found: {network_file}")
    print(network_file)

    return Network(str(network_file))


@pytest.fixture
def test_network_dedt():
    """Load the test network with a fake rate expression and an internal energy expression"""

    network_file = Path(__file__).parent / "fixtures" / "test_jac_dedt.dat"
    if not network_file.exists():
        pytest.skip(f"Test network file not found: {network_file}")
    print(network_file)

    return Network(str(network_file))


def test_network_reactions_loaded(test_network: Network):
    """Test that the test network loads with expected reactions."""

    assert len(test_network.reactions) > 0, "Test network should contain reactions"
    assert len(test_network.reactions) == 1, (
        "Test network should contain exactly 1 reaction"
    )


def test_rates(test_network: Network):
    "Test whether the correct rate has been loaded"

    rates = test_network.get_rates().strip().split("\n")
    rate = rates[-1].split("=")[-1].strip()
    expected_rate = "nden[0, 0]"

    assert len(rates) == 1, "Number of rates should be exactly 1"
    assert rate == expected_rate, f"Rate must be equal to {expected_rate}"


def test_ode_and_jac(test_network: Network):
    "Test generated odes and jac with precalculated expression strings"

    ode, jac = test_network.get_symbolic_ode_and_jacobian(use_cse=False)

    expected_rhs: List[str] = [
        "-std::pow(nden[0], 2)*nden[1]",
        "-std::pow(nden[0], 2)*nden[1]",
        "std::pow(nden[0], 2)*nden[1]",
    ]

    expected_jac: List[str] = [
        "-2*nden[0]*nden[1]",
        "-std::pow(nden[0], 2)",
        "-2*nden[0]*nden[1]",
        "-std::pow(nden[0], 2)",
        "2*nden[0]*nden[1]",
        "std::pow(nden[0], 2)",
    ]

    ode_comp = ode.strip().split("\n")
    jac_comp = jac.strip().split("\n")

    ode_comp = [comp.split("=")[-1].strip().strip(";") for comp in ode_comp]
    jac_comp = [comp.split("=")[-1].strip().strip(";") for comp in jac_comp]

    assert len(ode_comp) == len(expected_rhs), (
        f"Number of ode equations must be equal to {len(expected_rhs)}"
    )
    assert len(jac_comp) == len(expected_jac), (
        f"Number of jacobian components must be equal to {len(expected_jac)}"
    )

    for comp, excomp in zip(ode_comp, expected_rhs):
        assert comp == excomp, f"ODE: {comp} must be equal to {excomp}"

    for comp, excomp in zip(jac_comp, expected_jac):
        assert comp == excomp, f"Jacobian: {comp} must be equal to {excomp}"


def test_network_reactions_loaded_dedt(test_network_dedt: Network):
    """Test that the test network loads with expected reactions."""

    assert len(test_network_dedt.reactions) > 0, "Test network should contain reactions"
    assert len(test_network_dedt.reactions) == 1, (
        "Test network should contain exactly 1 reaction"
    )


def test_rates_dedt(test_network_dedt: Network):
    "Test whether the correct rate has been loaded"

    rates = test_network_dedt.get_rates().strip().split("\n")
    rate = rates[-1].split("=")[-1].strip()
    expected_rate = "nden[0, 0]"

    assert len(rates) == 1, "Number of rates should be exactly 1"
    assert rate == expected_rate, f"Rate must be equal to {expected_rate}"


def test_dedt(test_network_dedt: Network):
    "Test whether the correct internal energy rate has been loaded"

    dEdt = str(test_network_dedt.dEdt_chem)
    expected_dEdt = "nden[0, 0]**3*nden[1, 0]"

    assert dEdt == expected_dEdt, f"dEdt must be equal to {expected_dEdt}"


def test_ode_and_jac_dedt(test_network_dedt: Network):
    "Test generated odes and jac with precalculated expression strings"

    ode, jac = test_network_dedt.get_symbolic_ode_and_jacobian(
        use_cse=False, dedt_chem=True
    )

    expected_rhs: List[str] = [
        "-std::pow(nden[0], 2)*nden[1]",
        "-std::pow(nden[0], 2)*nden[1]",
        "std::pow(nden[0], 2)*nden[1]",
        "std::pow(nden[0], 3)*nden[1]/(1.6737729999999998e-24*nden[0] + 3.3435860000000001e-24*nden[1] + 6.6464729999999996e-24*nden[2])",
    ]

    expected_jac: List[str] = [
        "-2*nden[0]*nden[1]",
        "-std::pow(nden[0], 2)",
        "-2*nden[0]*nden[1]",
        "-std::pow(nden[0], 2)",
        "2*nden[0]*nden[1]",
        "std::pow(nden[0], 2)",
        "-1.6737729999999998e-24*std::pow(nden[0], 3)*nden[1]/std::pow(1.6737729999999998e-24*nden[0] + 3.3435860000000001e-24*nden[1] + 6.6464729999999996e-24*nden[2], 2) + 3*std::pow(nden[0], 2)*nden[1]/(1.6737729999999998e-24*nden[0] + 3.3435860000000001e-24*nden[1] + 6.6464729999999996e-24*nden[2])",
        "-3.3435860000000001e-24*std::pow(nden[0], 3)*nden[1]/std::pow(1.6737729999999998e-24*nden[0] + 3.3435860000000001e-24*nden[1] + 6.6464729999999996e-24*nden[2], 2) + std::pow(nden[0], 3)/(1.6737729999999998e-24*nden[0] + 3.3435860000000001e-24*nden[1] + 6.6464729999999996e-24*nden[2])",
        "-6.6464729999999996e-24*std::pow(nden[0], 3)*nden[1]/std::pow(1.6737729999999998e-24*nden[0] + 3.3435860000000001e-24*nden[1] + 6.6464729999999996e-24*nden[2], 2)",
    ]

    ode_comp = ode.strip().split("\n")
    jac_comp = jac.strip().split("\n")

    ode_comp = [comp.split("=")[-1].strip().strip(";") for comp in ode_comp]
    jac_comp = [comp.split("=")[-1].strip().strip(";") for comp in jac_comp]

    assert len(ode_comp) == len(expected_rhs), (
        f"Number of ode equations must be equal to {len(expected_rhs)}"
    )
    assert len(jac_comp) == len(expected_jac), (
        f"Number of jacobian components must be equal to {len(expected_jac)}"
    )

    for comp, excomp in zip(ode_comp, expected_rhs):
        assert comp == excomp, f"ODE: {comp} must be equal to {excomp}"

    for comp, excomp in zip(jac_comp, expected_jac):
        assert comp == excomp, f"Jacobian: {comp} must be equal to {excomp}"
