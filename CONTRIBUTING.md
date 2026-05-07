# Contributing to Kiro Dock

Thank you for your interest in contributing to the Kiro Dock project! This document provides guidelines and instructions for contributing.

## Code of Conduct

Be respectful and inclusive. All contributors are expected to follow basic principles of respect and professionalism.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/yourusername/engineersTech-dock-kiro/issues)
2. If not, create a new issue with:
   - Clear title describing the bug
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - Your environment (OS, Python version, etc.)
   - Screenshots if applicable

### Suggesting Enhancements

1. Check existing [Issues](https://github.com/yourusername/engineersTech-dock-kiro/issues) and [Discussions](https://github.com/yourusername/engineersTech-dock-kiro/discussions)
2. Create an issue with:
   - Clear title
   - Description of the enhancement
   - Why it would be useful
   - Possible implementation approach (optional)

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Add tests if applicable
5. Update documentation
6. Commit with clear messages (`git commit -m 'Add feature: description'`)
7. Push to your fork (`git push origin feature/your-feature`)
8. Open a Pull Request with:
   - Clear title
   - Description of changes
   - Link to related issues
   - Screenshots/demos if UI-related

## Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/engineersTech-dock-kiro.git
cd engineersTech-dock-kiro

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest black pylint

# Run tests
pytest
```

## Code Style

- Follow PEP 8 guidelines
- Use 4 spaces for indentation
- Add type hints where applicable
- Write docstrings for functions and classes

## Testing

- Write tests for new features
- Ensure all tests pass: `pytest`
- Test on multiple Python versions if possible

## Documentation

- Update README.md for user-facing changes
- Add docstrings to new functions
- Update CHANGELOG.md with changes

## Project Structure

```
engineersTech-dock-kiro/
├── main.py           # Main application
├── setup.py          # Configuration wizard
├── install.sh        # Installation script
├── requirements.txt  # Python dependencies
├── README.md         # Documentation
├── CHANGELOG.md      # Version history
├── LICENSE           # MIT License
└── CONTRIBUTING.md   # This file
```

## Questions?

- Open a [Discussion](https://github.com/yourusername/engineersTech-dock-kiro/discussions)
- Check existing documentation
- Review closed issues for similar questions

Thank you for contributing! 🎉
