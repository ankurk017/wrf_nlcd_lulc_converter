Installation Guide
=================

This guide provides detailed instructions for installing the WRF NLCD LULC converter package.

Prerequisites
------------

System Requirements
~~~~~~~~~~~~~~~~~~

* **Operating System**: Linux, macOS, or Windows
* **Python**: 3.8 or higher
* **Memory**: At least 4GB RAM (8GB+ recommended for large domains)
* **Storage**: At least 1GB free space for temporary files

Required System Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~

GDAL (Geospatial Data Abstraction Library)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

GDAL is required for processing GeoTIFF files. Install it before installing the Python package.

**Ubuntu/Debian:**
.. code-block:: bash

    sudo apt-get update
    sudo apt-get install gdal-bin libgdal-dev python3-gdal

**CentOS/RHEL/Fedora:**
.. code-block:: bash

    sudo yum install gdal gdal-devel python3-gdal
    # or for newer versions:
    sudo dnf install gdal gdal-devel python3-gdal

**macOS (using Homebrew):**
.. code-block:: bash

    brew install gdal

**Windows:**
Download and install from `OSGeo4W <https://trac.osgeo.org/osgeo4w/>`_ or use `conda-forge <https://conda-forge.org/>`_.

NetCDF4 Libraries
^^^^^^^^^^^^^^^^^

**Ubuntu/Debian:**
.. code-block:: bash

    sudo apt-get install libnetcdf-dev libhdf5-dev

**CentOS/RHEL/Fedora:**
.. code-block:: bash

    sudo yum install netcdf-devel hdf5-devel

**macOS:**
.. code-block:: bash

    brew install netcdf hdf5

Python Environment Setup
-----------------------

Option 1: Using pip (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Create a virtual environment:**
.. code-block:: bash

    python3 -m venv wrf_nlcd_env
    source wrf_nlcd_env/bin/activate  # On Windows: wrf_nlcd_env\Scripts\activate

2. **Install the package:**
.. code-block:: bash

    # Clone the repository
    git clone https://github.com/ankurk017/wrf-nlcd-lulc-converter.git
    cd wrf-nlcd-lulc-converter

    # Install in development mode
    pip install -e .

    # Or install with development dependencies
    pip install -e .[dev]

Option 2: Using conda
~~~~~~~~~~~~~~~~~~~~~

1. **Create a conda environment:**
.. code-block:: bash

    conda create -n wrf_nlcd python=3.9
    conda activate wrf_nlcd

2. **Install dependencies:**
.. code-block:: bash

    conda install -c conda-forge xarray numpy matplotlib cartopy rasterio netcdf4

3. **Install the package:**
.. code-block:: bash

    git clone https://github.com/ankurk017/wrf-nlcd-lulc-converter.git
    cd wrf-nlcd-lulc-converter
    pip install -e .

Verification
-----------

After installation, verify that everything is working:

.. code-block:: bash

    # Test the command-line interface
    wrf-nlcd-converter --info

    # Run the tests
    python -m pytest tests/

    # Test basic functionality
    python examples/basic_example.py

Troubleshooting
--------------

Common Issues
~~~~~~~~~~~~

1. **GDAL not found**
   **Error**: ``OSError: [Errno 2] No such file or directory: 'gdalwarp'``
   
   **Solution**: Install GDAL system-wide or ensure it's in your PATH.

2. **NetCDF4 import error**
   **Error**: ``ImportError: No module named 'netCDF4'``
   
   **Solution**: Install netCDF4 Python package:
   .. code-block:: bash

       pip install netCDF4
       # or
       conda install netcdf4

3. **Cartopy installation issues**
   **Error**: ``ImportError: No module named 'cartopy'``
   
   **Solution**: Install cartopy with conda:
   .. code-block:: bash

       conda install -c conda-forge cartopy

4. **Memory issues with large files**
   **Error**: ``MemoryError`` or slow performance
   
   **Solution**: 
   * Increase system RAM
   * Process smaller domains
   * Use ``--urban-only`` flag for faster processing

Platform-Specific Notes
~~~~~~~~~~~~~~~~~~~~~~~

**Linux**
* Most dependencies are available through package managers
* GDAL installation is straightforward
* Good performance for large datasets

**macOS**
* Use Homebrew for system dependencies
* May need to set environment variables for GDAL
* Good compatibility with Python scientific stack

**Windows**
* Use OSGeo4W for GDAL installation
* Consider using WSL (Windows Subsystem for Linux) for better performance
* Some dependencies may require Visual C++ build tools

Data Requirements
----------------

NLCD Data
~~~~~~~~~

* Download from `MRLC Viewer <https://www.mrlc.gov/data>`_
* Annual NLCD Land Cover data (GeoTIFF format)
* File naming convention: ``Annual_NLCD_LndCov_YYYY_CU_C1V1.tif``

**Note for Matrix Users**: NLCD raw maps from 1985 to 2024 are available in the default folder:
.. code-block:: bash

    /nas/rstor/akumar/common/NLCD_raw_maps

WRF geo_em Files
~~~~~~~~~~~~~~~~

* Generated using WPS (WRF Preprocessing System)
* NetCDF format with LU_INDEX and LANDUSEF variables
* Domain-specific files (e.g., ``geo_em.d02.nc``)

Next Steps
----------

After successful installation:

1. **Read the documentation**: See :doc:`usage` for usage examples
2. **Try the examples**: Run the example scripts in the ``examples/`` directory
3. **Prepare your data**: Download NLCD data and prepare WRF geo_em files
4. **Start processing**: Use the command-line interface or Python API

Getting Help
-----------

* **Documentation**: See :doc:`usage` and docstrings in the code
* **Examples**: Check the ``examples/`` directory
* **Issues**: Report bugs on `GitHub <https://github.com/ankurk017/wrf_nlcd_lulc_converter/issues>`_
* **Questions**: Open a discussion on `GitHub <https://github.com/ankurk017/wrf_nlcd_lulc_converter/discussions>`_
