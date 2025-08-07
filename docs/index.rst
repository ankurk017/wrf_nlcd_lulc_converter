Welcome to WRF NLCD LULC Converter's documentation!
================================================================

A Python package for converting National Land Cover Database (NLCD) land use data and updating WRF (Weather Research and Forecasting) geo_em files with new land use information.

.. image:: ../sample_lulc_plot.png
   :alt: Actual WRF LULC Data
   :width: 600px
   :align: center

*Actual LULC data from WRF geo_em file showing real land use classes for the Texas/Gulf Coast region (370,152 pixels, 28 unique classes).*

Features
--------

* Crop NLCD GeoTIFF files to specific domains using GDAL
* Interpolate NLCD land use data to WRF grid coordinates
* Map NLCD urban classes to WRF/GEOG urban classes
* Generate LANDUSEF arrays from LU_INDEX data
* Update WRF geo_em NetCDF files with new land use information
* Support for multiple NLCD years and WRF domains
* Visualization tools for LULC data and urban comparisons
* Plotting utilities with cartopy for geographic plots

Quick Start
-----------

.. code-block:: python

    from wrf_nlcd_lulc_converter import NLCDProcessor

    # Initialize processor
    processor = NLCDProcessor()

    # Process NLCD data and update WRF file
    processor.process_nlcd_and_update_wrf(
        nlcd_file="/nas/rstor/akumar/common/NLCD_raw_maps/Annual_NLCD_LndCov_2017_CU_C1V1.tif",
        wrf_file="path/to/geo_em.d02.nc",
        output_file="path/to/geo_em_updated.nc",
        year="2017"
    )

Installation
-----------

.. code-block:: bash

    # Clone the repository
    git clone https://github.com/ankurk017/wrf-nlcd-lulc-converter.git
    cd wrf-nlcd-lulc-converter

    # Install in development mode
    pip install -e .

Documentation Contents
---------------------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   usage
   api
   examples
   contributing

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Repository Information
---------------------

* **GitHub**: https://github.com/ankurk017/wrf_nlcd_lulc_converter
* **Author**: Ankur Kumar
* **Contact**: ankurk017@gmail.com, ankur.kumar@uah.edu, ankur.kumar@nasa.gov
* **License**: Apache 2.0

