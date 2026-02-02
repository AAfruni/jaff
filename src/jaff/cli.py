# ABOUTME: Command-line interface for JAFF package
# ABOUTME: Provides main entry point for the jaff command

"""Command-line interface for JAFF."""

import argparse
import sys
from .network import Network


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="JAFF - Just Another Fancy Format: Astrochemical network parser"
    )
    parser.add_argument("network_file", help="Path to the chemical network file")
    parser.add_argument(
        "-e", "--errors", action="store_true", help="Exit on errors during validation"
    )
    parser.add_argument("-l", "--label", help="Label for the network")
    parser.add_argument(
        "--check-mass", action="store_true", help="Check mass conservation in reactions"
    )
    parser.add_argument(
        "--check-charge",
        action="store_true",
        help="Check charge conservation in reactions",
    )
    parser.add_argument(
        "--list-species", action="store_true", help="List all species in the network"
    )
    parser.add_argument(
        "--list-reactions", action="store_true", help="List all reactions in the network"
    )

    args = parser.parse_args()

    try:
        # Load the network
        network = Network(args.network_file, errors=args.errors, label=args.label)

        # Perform requested actions
        if args.check_mass:
            network.check_mass(errors=args.errors)

        if args.check_charge:
            network.check_charge(errors=args.errors)

        if args.list_species:
            print(f"\nSpecies in network ({len(network.species)} total):")
            for species in sorted(network.species, key=lambda s: s.name):
                print(
                    f"  {species.name} (mass: {species.mass:.2f}, charge: {species.charge:+d})"
                )

        if args.list_reactions:
            print(f"\nReactions in network ({len(network.reactions)} total):")
            for i, reaction in enumerate(network.reactions):
                print(f"  {i + 1}: {reaction}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
