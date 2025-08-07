Contributing
============

Thank you for your interest in contributing to the WRF NLCD LULC converter project! This document provides guidelines for contributing to the project.

Getting Started
--------------

Development Setup
~~~~~~~~~~~~~~~~

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   .. code-block:: bash

       git clone https://github.com/YOUR_USERNAME/wrf-nlcd-lulc-converter.git
       cd wrf-nlcd-lulc-converter

3. **Create a development environment**:
   .. code-block:: bash

       conda create -n wrf_nlcd_dev python=3.9
       conda activate wrf_nlcd_dev
       conda install -c conda-forge xarray numpy matplotlib cartopy rasterio netcdf4

4. **Install in development mode**:
   .. code-block:: bash

       pip install -e .[dev]

5. **Create a new branch** for your changes:
   .. code-block:: bash

       git checkout -b feature/your-feature-name

Code Style
----------

Python Style Guide
~~~~~~~~~~~~~~~~~

* Follow `PEP 8 <https://www.python.org/dev/peps/pep-0008/>`_ style guidelines
* Use 4 spaces for indentation (no tabs)
* Maximum line length of 88 characters (use `black` for formatting)
* Use descriptive variable and function names
* Add type hints where appropriate

Code Formatting
~~~~~~~~~~~~~~~

The project uses `black` for code formatting:

.. code-block:: bash

    # Install black
    pip install black

    # Format your code
    black wrf_nlcd_lulc_converter/ tests/ examples/

Documentation
~~~~~~~~~~~~

* Write clear, concise docstrings for all functions and classes
* Use Google-style docstrings
* Include examples in docstrings where appropriate
* Update documentation when adding new features

Testing
-------

Writing Tests
~~~~~~~~~~~~

* Write tests for all new functionality
* Use `pytest` for testing
* Place tests in the `tests/` directory
* Test both success and error cases

Running Tests
~~~~~~~~~~~~

.. code-block:: bash

    # Run all tests
    pytest

    # Run tests with coverage
    pytest --cov=wrf_nlcd_lulc_converter

    # Run specific test file
    pytest tests/test_processor.py

    # Run tests with verbose output
    pytest -v

Test Structure
~~~~~~~~~~~~~

Tests should be organized as follows:

.. code-block:: python

    # tests/test_processor.py
    import pytest
    from wrf_nlcd_lulc_converter import NLCDProcessor

    class TestNLCDProcessor:
        def setup_method(self):
            """Set up test fixtures."""
            self.processor = NLCDProcessor()

        def test_initialization(self):
            """Test processor initialization."""
            assert self.processor is not None

        def test_process_nlcd_file(self):
            """Test NLCD file processing."""
            # Test implementation
            pass

Pull Request Process
-------------------

1. **Make your changes** in your feature branch
2. **Write tests** for new functionality
3. **Update documentation** if needed
4. **Run tests** to ensure everything works:
   .. code-block:: bash

       pytest
       python -m flake8 wrf_nlcd_lulc_converter/
       python setup.py check

5. **Commit your changes** with clear commit messages:
   .. code-block:: bash

       git add .
       git commit -m "Add feature: brief description of changes"

6. **Push to your fork**:
   .. code-block:: bash

       git push origin feature/your-feature-name

7. **Create a pull request** on GitHub with:
   * Clear description of changes
   * Reference to any related issues
   * Screenshots for UI changes (if applicable)

Commit Message Guidelines
~~~~~~~~~~~~~~~~~~~~~~~~

Use clear, descriptive commit messages:

* **Format**: `type(scope): description`
* **Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`
* **Examples**:
  * `feat(processor): add urban-only processing option`
  * `fix(plotting): resolve colorbar overlapping issue`
  * `docs(readme): update installation instructions`

Issue Reporting
--------------

Before creating an issue, please:

1. **Search existing issues** to avoid duplicates
2. **Check the documentation** for solutions
3. **Try the examples** to reproduce the issue

When reporting an issue, include:

* **Description**: Clear description of the problem
* **Steps to reproduce**: Detailed steps to reproduce the issue
* **Expected behavior**: What you expected to happen
* **Actual behavior**: What actually happened
* **Environment**: OS, Python version, package versions
* **Error messages**: Full error traceback if applicable

Feature Requests
---------------

When requesting new features:

* **Describe the use case** clearly
* **Explain the benefits** of the feature
* **Provide examples** of how it would be used
* **Consider implementation complexity**

Development Guidelines
--------------------

Code Organization
~~~~~~~~~~~~~~~~

* Keep functions small and focused
* Use meaningful variable names
* Add comments for complex logic
* Follow the existing code structure

Error Handling
~~~~~~~~~~~~~

* Use appropriate exception types
* Provide clear error messages
* Handle edge cases gracefully
* Log errors for debugging

Performance
~~~~~~~~~~~

* Profile code for bottlenecks
* Use efficient data structures
* Consider memory usage for large datasets
* Optimize critical paths

Documentation Standards
----------------------

Docstrings
~~~~~~~~~~

Use Google-style docstrings:

.. code-block:: python

    def process_nlcd_data(nlcd_file, wrf_file, output_file):
        """Process NLCD data and update WRF file.

        Args:
            nlcd_file (str): Path to NLCD GeoTIFF file
            wrf_file (str): Path to WRF geo_em file
            output_file (str): Path for output updated WRF file

        Returns:
            bool: True if processing successful, False otherwise

        Raises:
            FileNotFoundError: If input files don't exist
            ValueError: If file formats are invalid
        """
        pass

README Updates
~~~~~~~~~~~~~

* Update README.md for new features
* Add usage examples
* Update installation instructions if needed
* Keep examples current

API Documentation
~~~~~~~~~~~~~~~~

* Document all public functions and classes
* Include parameter descriptions
* Provide usage examples
* Update when API changes

Release Process
--------------

Versioning
~~~~~~~~~~

Follow semantic versioning (MAJOR.MINOR.PATCH):

* **MAJOR**: Breaking changes
* **MINOR**: New features (backward compatible)
* **PATCH**: Bug fixes (backward compatible)

Release Checklist
~~~~~~~~~~~~~~~~

Before releasing:

1. **Update version** in `setup.py` and `__init__.py`
2. **Update changelog** with new features/fixes
3. **Run all tests** to ensure everything works
4. **Update documentation** for new features
5. **Create release notes** on GitHub

Contact Information
------------------

* **Maintainer**: Ankur Kumar
* **Email**: ankurk017@gmail.com, ankur.kumar@uah.edu, ankur.kumar@nasa.gov
* **GitHub**: https://github.com/ankurk017/wrf_nlcd_lulc_converter
* **Issues**: https://github.com/ankurk017/wrf_nlcd_lulc_converter/issues
* **Discussions**: https://github.com/ankurk017/wrf_nlcd_lulc_converter/discussions

Thank you for contributing to the WRF NLCD LULC converter project!
