# Contributing to JAFF

Welcome! We're excited that you're interested in contributing to JAFF (Just Another Fancy Format), an astrochemical network parser.

PLEASE NOTE:
If you choose to make contributions to the code, you hereby grant a non-exclusive, royalty-free perpetual license
to install, use, modify, prepare derivative works, incorporate into other computer software,
distribute, and sublicense such enhancements or derivative works thereof, in binary and source code form.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR-USERNAME/jaff.git`
3. Create a new branch: `git checkout -b your-feature-name`
4. Install the package in development mode: `uv pip install -e ".[dev]"`

## Development Process

### Code Style

- Match the style and formatting of surrounding code
- Keep solutions simple, clean, and maintainable
- Each code file should start with a 2-line comment beginning with "ABOUTME: "
- Preserve existing comments unless they are demonstrably false

### Making Changes

1. Make the smallest reasonable changes to achieve your goal
2. Write tests BEFORE implementing new features (Test-Driven Development)
3. Ensure all tests pass before submitting
4. Commit frequently with clear, descriptive messages

### Testing

All contributions should include:

- Unit tests for individual components
- An example Python notebook in `examples/` demonstrating your feature

Run tests with: `uv run pytest` (once test framework is set up)

### Submitting Changes

1. Push your branch to your fork
2. Create a Pull Request with:
    - Clear description of the changes
    - Reference to any related issues
    - Test results showing all tests pass
3. Address any review feedback promptly

## Questions?

Open an issue for:

- Bug reports
- Feature requests
- Questions about the codebase
- Discussion of potential contributions

Thank you for contributing to JAFF!
