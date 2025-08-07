Usage Guide
===========

This guide provides comprehensive usage examples for the WRF NLCD LULC converter package.

Basic Usage
----------

Python API
~~~~~~~~~~

The main class for processing NLCD data is ``NLCDProcessor``:

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

Command Line Interface
~~~~~~~~~~~~~~~~~~~~~

The package provides a command-line interface for easy batch processing:

.. code-block:: bash

    # Basic usage (Matrix users can use the default NLCD folder)
    wrf-nlcd-converter --nlcd-file /nas/rstor/akumar/common/NLCD_raw_maps/Annual_NLCD_LndCov_2017_CU_C1V1.tif --wrf-file path/to/geo_em.d02.nc --output-file path/to/output.nc --year 2017

    # With custom domain margins
    wrf-nlcd-converter --nlcd-file /nas/rstor/akumar/common/NLCD_raw_maps/Annual_NLCD_LndCov_2017_CU_C1V1.tif --wrf-file path/to/geo_em.d02.nc --output-file path/to/output.nc --year 2017 --margin 2.0

Advanced Usage
-------------

Custom LULC Mapping
~~~~~~~~~~~~~~~~~~~

You can customize the mapping between NLCD and WRF classes:

.. code-block:: python

    from wrf_nlcd_lulc_converter import NLCDProcessor, LULCMapping

    # Custom LULC mapping
    custom_mapping = {
        21: 23,  # NLCD Open Water -> WRF Developed Open Space
        22: 24,  # NLCD Perennial Ice/Snow -> WRF Developed Low Intensity
        23: 25,  # NLCD Developed Open Space -> WRF Developed Medium Intensity
        24: 26,  # NLCD Developed Low Intensity -> WRF Developed High Intensity
    }

    processor = NLCDProcessor(lulc_mapping=custom_mapping)

    # Process with custom parameters
    processor.process_nlcd_and_update_wrf(
        nlcd_file="/nas/rstor/akumar/common/NLCD_raw_maps/Annual_NLCD_LndCov_2017_CU_C1V1.tif",
        wrf_file="path/to/geo_em.d02.nc",
        output_file="path/to/geo_em_updated.nc",
        year="2017",
        margin=1.5,
        force_recalculate=True
    )

Urban-Only Processing
~~~~~~~~~~~~~~~~~~~~

Process only urban classes for faster processing:

.. code-block:: python

    # Process only urban classes
    processor.process_urban_only(
        nlcd_file="/nas/rstor/akumar/common/NLCD_raw_maps/Annual_NLCD_LndCov_2017_CU_C1V1.tif",
        wrf_file="path/to/geo_em.d02.nc",
        output_file="path/to/geo_em_urban.nc",
        year="2017"
    )

Or use the CLI:

.. code-block:: bash

    wrf-nlcd-converter --nlcd-file /nas/rstor/akumar/common/NLCD_raw_maps/Annual_NLCD_LndCov_2017_CU_C1V1.tif --wrf-file path/to/geo_em.d02.nc --output-file path/to/geo_em_urban.nc --year 2017 --urban-only

Visualization
------------

The package includes comprehensive visualization tools:

.. code-block:: python

    from wrf_nlcd_lulc_converter import plot_lulc_data, plot_urban_comparison

    # Plot LULC data
    plot_lulc_data(longitudes, latitudes, lulc_data,
                   title="LULC Data",
                   extent=[lon_min, lon_max, lat_min, lat_max],
                   save_path="lulc_plot.png")

    # Compare urban areas before and after
    plot_urban_comparison(original_lulc, updated_lulc, 
                         longitudes, latitudes,
                         title="Urban Area Comparison",
                         save_path="urban_comparison.png")

Colormap Module
~~~~~~~~~~~~~~~

The package includes a comprehensive colormap module:

.. code-block:: python

    from wrf_nlcd_lulc_converter import get_lulc_colormap, get_class_info

    # Get the 40-class LULC colormap
    cmap, labels, colors, vmin, vmax = get_lulc_colormap()

    # Get information for a specific class
    info = get_class_info(23)  # Returns {"label": "Developed Open Space", "color": "#ffb3b3"}

Parameters
---------

NLCDProcessor.process_nlcd_and_update_wrf()
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* **nlcd_file** (str): Path to NLCD GeoTIFF file
* **wrf_file** (str): Path to WRF geo_em file
* **output_file** (str): Path for output updated WRF file
* **year** (str): Year of NLCD data
* **margin** (float, optional): Margin around WRF domain in degrees (default: 1.0)
* **force_recalculate** (bool, optional): Force recalculation even if files exist (default: False)
* **tmp_folder** (str, optional): Temporary folder for processed files (default: ~/tmp/nlcd_processed/)

Command Line Arguments
~~~~~~~~~~~~~~~~~~~~~

* **--nlcd-file**: Path to NLCD GeoTIFF file
* **--wrf-file**: Path to WRF geo_em file
* **--output-file**: Path for output updated WRF file
* **--year**: Year of NLCD data
* **--margin**: Margin around WRF domain in degrees (default: 1.0)
* **--force-recalculate**: Force recalculation even if files exist
* **--urban-only**: Process only urban classes from NLCD data
* **--tmp-folder**: Temporary folder for processed files
* **--custom-mapping**: Custom NLCD to WRF mapping as JSON string
* **--info**: Show processor information and exit
* **--verbose**: Enable verbose output

Examples
--------

Complete Workflow
~~~~~~~~~~~~~~~~~

.. code-block:: python

    from wrf_nlcd_lulc_converter import NLCDProcessor
    from wrf_nlcd_lulc_converter.utils import extract_wrf_domain_info
    from wrf_nlcd_lulc_converter.plotting import plot_lulc_data, plot_urban_comparison

    # Set up file paths
    nlcd_raw_map_folder = '/nas/rstor/akumar/common/NLCD_raw_maps'
    year = '2017'
    infile_geog01 = '/nas/rstor/akumar/common/sample_geog/geo_em.d02.nc'

    # Construct NLCD file path
    raw_NLCD_map = f'{nlcd_raw_map_folder}/Annual_NLCD_LndCov_{year}_CU_C1V1.tif'

    # Initialize processor
    processor = NLCDProcessor()

    # Extract WRF domain information
    wrf_info = extract_wrf_domain_info(infile_geog01)
    geog_roi_domain = wrf_info['domain']

    # Process NLCD data and update WRF file
    processor.process_nlcd_and_update_wrf(
        nlcd_file=raw_NLCD_map,
        wrf_file=infile_geog01,
        output_file="geo_em_updated.nc",
        year=year,
        margin=1.0
    )

    # Create visualizations
    plot_lulc_data(wrf_info['longitudes'], wrf_info['latitudes'], 
                   wrf_info['lu_index'], title="Original WRF LULC Data")
    plot_urban_comparison(wrf_info['lu_index'], updated_lu_index,
                         wrf_info['longitudes'], wrf_info['latitudes'])

Real Data Example
~~~~~~~~~~~~~~~~

The package includes examples using actual WRF data:

.. code-block:: python

    # Use actual WRF file
    wrf_file = "/nas/rstor/akumar/common/sample_geog/geo_em.d02.nc"
    
    # Extract and analyze real data
    wrf_info = extract_wrf_domain_info(wrf_file)
    print(f"Domain: {wrf_info['domain']}")
    print(f"Data shape: {wrf_info['lu_index'].shape}")
    print(f"Unique classes: {np.unique(wrf_info['lu_index'])}")

Error Handling
-------------

The package includes comprehensive error handling:

* **File validation**: Checks if input files exist and are readable
* **Format validation**: Validates NLCD and WRF file formats
* **Memory management**: Handles large datasets efficiently
* **Progress reporting**: Shows processing progress for long operations

Troubleshooting
--------------

Common Issues
~~~~~~~~~~~~

1. **GDAL not found**: Install GDAL system-wide
2. **Memory errors**: Use smaller domains or urban-only processing
3. **File format errors**: Ensure files are in correct format
4. **Permission errors**: Check file permissions and paths

Getting Help
-----------

* **Documentation**: `Live Documentation <https://wrf-nlcd-lulc-converter.readthedocs.io/en/latest/>`_
* **Examples**: Check the ``examples/`` directory
* **Issues**: Report bugs on `GitHub <https://github.com/ankurk017/wrf_nlcd_lulc_converter/issues>`_
* **Questions**: Open a discussion on `GitHub <https://github.com/ankurk017/wrf_nlcd_lulc_converter/discussions>`_
