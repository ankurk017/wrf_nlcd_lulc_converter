Examples
========

This page provides examples of how to use the WRF NLCD LULC converter package.

Basic Examples
-------------

Simple WRF Example
~~~~~~~~~~~~~~~~~~

The `simple_wrf_example.py` demonstrates using actual WRF data:

.. code-block:: python

    #!/usr/bin/env python3
    """
    Simple WRF file example that doesn't require all dependencies.
    """

    import os
    import sys
    import numpy as np
    import xarray as xr
    import matplotlib.pyplot as plt

    from wrf_nlcd_lulc_converter.colormap import get_lulc_colormap, get_class_info, get_urban_classes

    def main():
        # Define the actual WRF file path
        wrf_file = "/nas/rstor/akumar/common/sample_geog/geo_em.d02.nc"
        
        if not os.path.exists(wrf_file):
            print(f"Error: WRF file not found: {wrf_file}")
            return
        
        # Extract WRF domain information
        wrf_info = extract_wrf_domain_info_simple(wrf_file)
        
        longitudes = wrf_info['longitudes']
        latitudes = wrf_info['latitudes']
        lulc_data = wrf_info['lu_index']
        domain = wrf_info['domain']
        
        print(f"Domain: {domain}")
        print(f"Data shape: {lulc_data.shape}")
        print(f"Longitude range: {longitudes.min():.3f} to {longitudes.max():.3f}")
        print(f"Latitude range: {latitudes.min():.3f} to {latitudes.max():.3f}")
        
        # Analyze the data
        unique_classes = np.unique(lulc_data)
        print(f"Unique LULC classes: {unique_classes}")
        print(f"Number of unique classes: {len(unique_classes)}")
        
        # Create visualizations
        plot_lulc_data_simple(longitudes, latitudes, lulc_data,
                             title="Actual WRF LULC Data - Full Domain",
                             save_path="plots/simple_wrf_full_domain.png", show_plot=False)

Colormap Example
~~~~~~~~~~~~~~~

The `colormap_example.py` demonstrates the colormap module:

.. code-block:: python

    #!/usr/bin/env python3
    """
    Colormap example for the WRF NLCD LULC converter.
    """

    from wrf_nlcd_lulc_converter import (
        get_lulc_colormap, get_lulc_normalization, get_urban_colormap,
        get_urban_normalization, create_colorbar, create_urban_colorbar,
        get_class_info, get_urban_classes, plot_colormap_legend
    )

    def main():
        # Get LULC colormap
        cmap, labels, colors, vmin, vmax = get_lulc_colormap()
        print(f"Colormap: {type(cmap)}")
        print(f"Number of classes: {len(labels)}")
        print(f"Vmin: {vmin}, Vmax: {vmax}")
        
        # Get normalization
        norm_vmin, norm_vmax, ticks, tick_labels = get_lulc_normalization()
        print(f"Normalization bounds: {norm_vmin} to {norm_vmax}")
        
        # Get class information
        for class_num in [1, 13, 21, 23, 26, 40]:
            info = get_class_info(class_num)
            print(f"Class {class_num:2d}: {info['label']:30s} - Color: {info['color']}")
        
        # Create sample plot with actual WRF data
        wrf_file = "/nas/rstor/akumar/common/sample_geog/geo_em.d02.nc"
        
        if os.path.exists(wrf_file):
            wrf_info = extract_wrf_domain_info(wrf_file)
            longitudes = wrf_info['longitudes']
            latitudes = wrf_info['latitudes']
            lulc_data = wrf_info['lu_index']
            
            # Create plot
            fig, ax = plt.subplots(1, 1, figsize=(12, 8))
            im = ax.pcolormesh(longitudes, latitudes, lulc_data, 
                              cmap=cmap, vmin=vmin, vmax=vmax)
            create_colorbar(ax, im)
            ax.set_xlabel('Longitude')
            ax.set_ylabel('Latitude')
            ax.set_title('Actual WRF LULC Data with Colormap Module')
            plt.savefig("plots/actual_wrf_colormap_example.png", dpi=150, bbox_inches='tight')

Plotting Example
~~~~~~~~~~~~~~~

The `plotting_example.py` demonstrates comprehensive plotting:

.. code-block:: python

    #!/usr/bin/env python3
    """
    Plotting example for the WRF NLCD LULC converter.
    """

    from wrf_nlcd_lulc_converter import (
        plot_lulc_data, plot_urban_comparison, plot_domain_info,
        create_sample_plot
    )
    from wrf_nlcd_lulc_converter.utils import extract_wrf_domain_info

    def main():
        # Create sample plots
        plot_lulc_data(longitudes, latitudes, lulc_data,
                      title="Sample LULC Data",
                      save_path="plots/sample_lulc_plot.png")
        
        # Create custom plots
        plot_lulc_data(longitudes, latitudes, lulc_data,
                      title="Custom LULC Plot",
                      extent=[lon_min, lon_max, lat_min, lat_max],
                      save_path="plots/custom_lulc_plot.png")
        
        # Create urban comparison
        plot_urban_comparison(original_lulc, updated_lulc, 
                            longitudes, latitudes,
                            title="Urban Area Comparison",
                            save_path="plots/urban_comparison.png")
        
        # Plot WRF domain from actual file
        wrf_file = "/nas/rstor/akumar/common/sample_geog/geo_em.d02.nc"
        
        if os.path.exists(wrf_file):
            wrf_info = extract_wrf_domain_info(wrf_file)
            plot_domain_info(wrf_info, 
                           title="WRF Domain LULC Data (Actual File)",
                           save_path="plots/wrf_domain.png", dpi=150)
            
            # Create custom plot with actual data
            longitudes = wrf_info['longitudes']
            latitudes = wrf_info['latitudes']
            lulc_data = wrf_info['lu_index']
            domain = wrf_info['domain']
            
            plot_lulc_data(longitudes, latitudes, lulc_data,
                          title="Actual WRF LULC Data",
                          extent=[domain['lon_min'], domain['lon_max'], 
                                 domain['lat_min'], domain['lat_max']],
                          save_path="plots/actual_lulc_data.png", show_plot=False)

Complete Workflow Example
~~~~~~~~~~~~~~~~~~~~~~~~

The `complete_workflow_example.py` demonstrates the full workflow:

.. code-block:: python

    #!/usr/bin/env python3
    """
    Complete workflow example for the WRF NLCD LULC converter.
    """

    from wrf_nlcd_lulc_converter import NLCDProcessor, LULCMapping
    from wrf_nlcd_lulc_converter.utils import extract_wrf_domain_info, calculate_nlcd_crop_domain
    from wrf_nlcd_lulc_converter.plotting import plot_lulc_data, plot_urban_comparison, plot_domain_info

    def main():
        # Set up file paths using actual WRF file and default NLCD folder
        nlcd_raw_map_folder = '/nas/rstor/akumar/common/NLCD_raw_maps'
        year = '2017'
        infile_geog01 = '/nas/rstor/akumar/common/sample_geog/geo_em.d02.nc'

        # Construct NLCD file path (Matrix users can use the default folder)
        raw_NLCD_map = f'{nlcd_raw_map_folder}/Annual_NLCD_LndCov_{year}_CU_C1V1.tif'

        # Initialize processor
        processor = NLCDProcessor()

        # Extract WRF domain information
        wrf_info = extract_wrf_domain_info(infile_geog01)
        geog_roi_domain = wrf_info['domain']

        # Calculate NLCD crop domain
        nlcd_crop_domain = calculate_nlcd_crop_domain(geog_roi_domain, margin=1.0)

        # Process NLCD data and update WRF file
        processor.process_nlcd_and_update_wrf(
            nlcd_file=raw_NLCD_map,
            wrf_file=infile_geog01,
            output_file="geo_em_updated.nc",
            year=year,
            margin=1.0
        )

        # Create visualizations
        create_visualizations(wrf_info['lu_index'], wrf_info['latitudes'], 
                           wrf_info['longitudes'], geog_roi_domain, "geo_em_updated.nc")

    def create_visualizations(original_lu_index, latitudes, longitudes, domain, updated_file):
        """
        Create visualizations of the LULC data and processing results.
        """
        try:
            os.makedirs("plots", exist_ok=True)
            extent = [domain['lon_min'], domain['lon_max'], domain['lat_min'], domain['lat_max']]
            
            plot_lulc_data(longitudes, latitudes, original_lu_index, 
                          title="Original WRF LULC Data", extent=extent, 
                          save_path="plots/original_lulc.png", show_plot=False)
            
            if os.path.exists(updated_file):
                with xr.open_dataset(updated_file) as ds:
                    updated_lu_index = ds['LU_INDEX'].values.squeeze()
                
                plot_lulc_data(longitudes, latitudes, updated_lu_index, 
                              title="Updated WRF LULC Data", extent=extent, 
                              save_path="plots/updated_lulc.png", show_plot=False)
                
                plot_urban_comparison(original_lu_index, updated_lu_index, 
                                    longitudes, latitudes,
                                    title="Urban Area Comparison (Original vs Updated)", 
                                    save_path="plots/urban_comparison.png", dpi=150)
            
            print("  All plots saved in 'plots/' directory")
        except Exception as e:
            print(f"  Error creating visualizations: {str(e)}")

Urban Only Example
~~~~~~~~~~~~~~~~~

The `urban_only_example.py` demonstrates urban-only processing:

.. code-block:: python

    #!/usr/bin/env python3
    """
    Urban-only processing example for the WRF NLCD LULC converter.
    """

    from wrf_nlcd_lulc_converter import NLCDProcessor

    def main():
        # Initialize processor
        processor = NLCDProcessor()

        # Process only urban classes
        processor.process_urban_only(
            nlcd_file="/nas/rstor/akumar/common/NLCD_raw_maps/Annual_NLCD_LndCov_2017_CU_C1V1.tif",
            wrf_file="path/to/geo_em.d02.nc",
            output_file="path/to/geo_em_urban.nc",
            year="2017"
        )

        # Show processor information
        info = processor.get_processing_info()
        print(f"Total LULC classes: {info['total_classes']}")
        print(f"Urban classes: {info['urban_classes']}")

Real Data Statistics
-------------------

The examples using actual WRF data show:

* **Domain**: Texas/Gulf Coast region (22.8°N to 33.3°N, -100.3°W to -87.3°W)
* **Grid Size**: 582 × 636 pixels
* **Total Pixels**: 370,152
* **Unique Classes**: 28 LULC classes
* **Urban Coverage**: 1.94% (7,199 pixels)

Class Distribution:
* Class 17 (IGBP Water): 183,525 pixels (49.6%)
* Class 32 (Shrub/Scrub): 38,169 pixels (10.3%)
* Class 29 (Evergreen Forest): 26,298 pixels (7.1%)
* Class 37 (Pasture/Hay): 19,806 pixels (5.4%)
* Class 38 (Cultivated Crops): 16,598 pixels (4.5%)
* Class 39 (Woody Wetlands): 15,361 pixels (4.1%)

Urban Classes:
* Class 23 (Developed Open Space): 2,707 pixels
* Class 24 (Developed Low Intensity): 3,058 pixels
* Class 25 (Developed Medium Intensity): 1,303 pixels
* Class 26 (Developed High Intensity): 131 pixels

Running Examples
---------------

To run the examples:

.. code-block:: bash

    # Run simple WRF example
    python examples/simple_wrf_example.py

    # Run colormap example
    python examples/colormap_example.py

    # Run plotting example
    python examples/plotting_example.py

    # Run complete workflow example
    python examples/complete_workflow_example.py

    # Run urban-only example
    python examples/urban_only_example.py

Output Files
-----------

The examples generate various output files:

* **Plots**: Visualizations saved in `plots/` directory
* **Updated WRF files**: Modified geo_em files with new LULC data
* **Statistics**: Analysis results printed to console
* **Logs**: Processing information and progress reports

Example Output
-------------

.. code-block:: text

    WRF NLCD LULC Converter - Simple WRF File Example
    ============================================================
    1. Extracting WRF domain information...
       Domain: {'lon_min': -100.269455, 'lon_max': -87.3017, 'lat_min': 22.845161, 'lat_max': 33.291862}
       Data shape: (582, 636)
       Longitude range: -100.269 to -87.302
       Latitude range: 22.845 to 33.292

    2. Analyzing LULC data...
       Unique LULC classes: [ 2.  4.  5.  6.  7.  8.  9. 10. 11. 12. 13. 14. 16. 17. 23. 24. 25. 26. 27. 28. 29. 30. 32. 33. 37. 38. 39. 40.]
       Number of unique classes: 28
       Class  2: Evergreen Broadleaf Forest     -      884 pixels (  0.2%)
       Class  4: Deciduous Broadleaf Forest     -        6 pixels (  0.0%)
       ...
       Class 17: IGBP Water                     -   183525 pixels ( 49.6%)
       ...
       Class 23: Developed Open Space           -     2707 pixels (  0.7%)
       Class 24: Developed Low Intensity        -     3058 pixels (  0.8%)
       Class 25: Developed Medium Intensity     -     1303 pixels (  0.4%)
       Class 26: Developed High Intensity       -      131 pixels (  0.0%)

    3. Analyzing urban areas...
       Total urban pixels: 7,199
       Urban percentage: 1.94%

    4. Creating visualizations...
       Creating full domain plot...
       Plot saved to: plots/simple_wrf_full_domain.png
       Creating urban areas plot...
       Plot saved to: plots/simple_wrf_urban_areas.png

    All plots saved in the 'plots/' directory:
      - simple_wrf_full_domain.png
      - simple_wrf_urban_areas.png
      - simple_wrf_comparison.png
