# Documentation

This directory contains the Sphinx documentation for the WRF NLCD LULC converter package.

## Building the Documentation

### Prerequisites

1. Install Sphinx and the Read the Docs theme:
   ```bash
   pip install sphinx sphinx-rtd-theme
   ```

2. Install the package in development mode:
   ```bash
   pip install -e .
   ```

### Building Locally

1. Navigate to the docs directory:
   ```bash
   cd docs
   ```

2. Build the HTML documentation:
   ```bash
   make html
   ```

3. View the documentation:
   ```bash
   # Open docs/_build/html/index.html in your browser
   # Or use a simple HTTP server:
   python -m http.server -d _build/html
   ```

### Building Other Formats

- **PDF**: `make latexpdf`
- **EPUB**: `make epub`
- **Link Check**: `make linkcheck`

## Documentation Structure

- `index.rst` - Main documentation page
- `installation.rst` - Installation guide
- `usage.rst` - Usage guide with examples
- `api.rst` - API reference (auto-generated)
- `examples.rst` - Detailed examples
- `contributing.rst` - Contributing guidelines

## Configuration

The documentation is configured in `conf.py`:

- **Theme**: Read the Docs theme
- **Extensions**: autodoc, viewcode, napoleon, intersphinx
- **GitHub Pages**: Configured for deployment to GitHub Pages

## Auto-Generated Documentation

The API documentation is automatically generated from docstrings in the source code using Sphinx's autodoc extension.

## Deployment

The documentation is automatically deployed to Read the Docs when changes are pushed to the main branch. The documentation is hosted at: https://wrf-nlcd-lulc-converter.readthedocs.io/

## Contributing to Documentation

1. Update the relevant `.rst` files
2. Add docstrings to new functions/classes
3. Update the `index.rst` table of contents if needed
4. Test the build locally before committing
5. Push changes to trigger automatic deployment

## Troubleshooting

### Common Issues

1. **Import errors**: Make sure the package is installed in development mode
2. **Missing modules**: Check that all dependencies are installed
3. **Build errors**: Check the Sphinx output for specific error messages

### Getting Help

- Check the [Sphinx documentation](https://www.sphinx-doc.org/)
- Review the [Read the Docs theme documentation](https://sphinx-rtd-theme.readthedocs.io/)
- Open an issue on GitHub for documentation-specific problems
