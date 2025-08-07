#!/usr/bin/env python3
"""
Plotting example for the WRF NLCD LULC converter.

This example demonstrates how to create various plots and visualizations
for LULC data and WRF domains.
"""

import os
import sys
import numpy as np
import xarray as xr

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from wrf_nlcd_lulc_converter import (
    NLCDProcessor, LULCMapping, 
    plot_lulc_data, plot_urban_comparison, plot_domain_info, create_sample_plot
)
from wrf_nlcd_lulc_converter.utils import extract_wrf_domain_info


def main():
    """
    Main plotting example demonstrating various visualization features.
    """
    print("WRF NLCD LULC Converter - Plotting Example")
    print("=" * 50)
    
    # Create output directory for plots
    os.makedirs("plots", exist_ok=True)
    
    # Example 1: Create a sample plot
    print("\n1. Creating sample LULC plot...")
    sample_plot_path = create_sample_plot()
    print(f"Sample plot created: {sample_plot_path}")
    
    # Example 2: Plot with custom data
    print("\n2. Creating custom LULC plot...")
    
    # Create sample data for Houston area
    lon_min, lon_max = -96.5, -94.0
    lat_min, lat_max = 28.9, 30.5
    nx, ny = 100, 80
    
    longitudes = np.linspace(lon_min, lon_max, nx)
    latitudes = np.linspace(lat_min, lat_max, ny)
    
    # Create realistic LULC data
    lulc_data = np.ones((ny, nx)) * 16  # Default to barren land
    
    # Add some urban areas
    mapping = LULCMapping()
    urban_classes = mapping.get_urban_classes()
    
    # Create urban clusters
    urban_centers = [
        (29.7604, -95.3698),  # Houston downtown
        (29.9511, -95.3571),  # The Woodlands
        (29.5577, -95.1102),  # Baytown
    ]
    
    for center_lat, center_lon in urban_centers:
        # Find grid indices
        lat_idx = np.argmin(np.abs(latitudes - center_lat))
        lon_idx = np.argmin(np.abs(longitudes - center_lon))
        
        # Create urban area around center
        radius = 10
        for i in range(max(0, lat_idx-radius), min(ny, lat_idx+radius)):
            for j in range(max(0, lon_idx-radius), min(nx, lon_idx+radius)):
                if np.random.random() < 0.7:  # 70% urban in radius
                    lulc_data[i, j] = np.random.choice(urban_classes)
    
    # Add some water bodies
    water_mask = np.random.random((ny, nx)) < 0.05
    lulc_data[water_mask] = 21  # Open Water
    
    # Add some forest areas
    forest_mask = np.random.random((ny, nx)) < 0.15
    lulc_data[forest_mask] = np.random.choice([1, 2, 3, 4, 5], size=np.sum(forest_mask))
    
    # Plot the data
    custom_plot_path = "plots/custom_lulc_plot.png"
    plot_lulc_data(longitudes, latitudes, lulc_data,
                   title="Custom LULC Data (Houston Area)",
                   extent=[lon_min, lon_max, lat_min, lat_max],
                   save_path=custom_plot_path, show_plot=False)
    
    print(f"Custom plot saved: {custom_plot_path}")
    
    # Example 3: Urban comparison plot
    print("\n3. Creating urban comparison plot...")
    
    # Create "before" and "after" data
    original_lulc = lulc_data.copy()
    updated_lulc = lulc_data.copy()
    
    # Simulate urban expansion
    expansion_mask = np.random.random((ny, nx)) < 0.02  # 2% expansion
    expansion_mask &= (lulc_data != 21)  # Don't expand into water
    updated_lulc[expansion_mask] = np.random.choice(urban_classes, size=np.sum(expansion_mask))
    
    comparison_plot_path = "plots/urban_comparison.png"
    plot_urban_comparison(original_lulc, updated_lulc, longitudes, latitudes,
                         title="Urban Area Comparison (Before vs After)",
                         save_path=comparison_plot_path, dpi=150)
    
    print(f"Urban comparison plot saved: {comparison_plot_path}")
    
    # Example 4: WRF domain plotting using actual WRF file
    print("\n4. Plotting WRF domain from actual file...")
    
    # Use the actual WRF file
    wrf_file = "/nas/rstor/akumar/common/sample_geog/geo_em.d02.nc"
    
    if os.path.exists(wrf_file):
        try:
            wrf_info = extract_wrf_domain_info(wrf_file)
            domain_plot_path = "plots/wrf_domain.png"
            plot_domain_info(wrf_info, 
                           title="WRF Domain LULC Data (Actual File)",
                           save_path=domain_plot_path, dpi=150)
            print(f"WRF domain plot saved: {domain_plot_path}")
            
            # Also create a custom plot with the actual data
            longitudes = wrf_info['longitudes']
            latitudes = wrf_info['latitudes']
            lulc_data = wrf_info['lu_index']
            domain = wrf_info['domain']
            
            # Create custom plot with actual data
            custom_plot_path = "plots/actual_lulc_data.png"
            plot_lulc_data(longitudes, latitudes, lulc_data,
                          title="Actual WRF LULC Data",
                          extent=[domain['lon_min'], domain['lon_max'], 
                                 domain['lat_min'], domain['lat_max']],
                          save_path=custom_plot_path, show_plot=False)
            print(f"Actual LULC data plot saved: {custom_plot_path}")
            
        except Exception as e:
            print(f"Could not plot WRF domain: {e}")
            import traceback
            traceback.print_exc()
    else:
        print(f"WRF file not found: {wrf_file}")
        print("Skipping WRF domain plotting...")
    
    # Example 5: LULC class statistics
    print("\n5. Creating LULC class statistics...")
    
    mapping = LULCMapping()
    unique_classes, counts = np.unique(lulc_data, return_counts=True)
    
    print("LULC Class Distribution:")
    for class_num, count in zip(unique_classes, counts):
        if class_num in mapping.lulc_dict:
            label = mapping.lulc_dict[class_num]['label']
            percentage = (count / lulc_data.size) * 100
            print(f"  Class {int(class_num):2d}: {label:30s} - {count:6d} pixels ({percentage:5.1f}%)")
    
    # Example 6: Urban area analysis
    print("\n6. Urban area analysis...")
    
    urban_mask = np.isin(lulc_data, urban_classes)
    urban_pixels = np.sum(urban_mask)
    urban_percentage = (urban_pixels / lulc_data.size) * 100
    
    print(f"Urban pixels: {urban_pixels:,}")
    print(f"Total pixels: {lulc_data.size:,}")
    print(f"Urban percentage: {urban_percentage:.2f}%")
    
    # Urban class breakdown
    for urban_class in urban_classes:
        class_count = np.sum(lulc_data == urban_class)
        class_percentage = (class_count / lulc_data.size) * 100
        label = mapping.lulc_dict[urban_class]['label']
        print(f"  Class {urban_class}: {label:25s} - {class_count:6d} pixels ({class_percentage:5.1f}%)")
    
    print(f"\nAll plots saved in the 'plots/' directory")
    print("Check the following files:")
    print(f"  - {sample_plot_path}")
    print(f"  - {custom_plot_path}")
    print(f"  - {comparison_plot_path}")


def demonstrate_plotting_functions():
    """
    Demonstrate individual plotting functions.
    """
    print("\n" + "=" * 50)
    print("Plotting Function Demonstrations")
    print("=" * 50)
    
    # Create sample data
    mapping = LULCMapping()
    
    # Small sample for demonstration
    nx, ny = 50, 40
    longitudes = np.linspace(-96.5, -94.0, nx)
    latitudes = np.linspace(28.9, 30.5, ny)
    
    # Create sample LULC data
    lulc_data = np.random.randint(1, 41, size=(ny, nx))
    
    # Add some urban areas
    urban_classes = mapping.get_urban_classes()
    urban_mask = np.random.random((ny, nx)) < 0.1
    lulc_data[urban_mask] = np.random.choice(urban_classes, size=np.sum(urban_mask))
    
    print("Available plotting functions:")
    print("1. plot_lulc_data() - Basic LULC data plotting")
    print("2. plot_urban_comparison() - Before/after urban comparison")
    print("3. plot_domain_info() - WRF domain plotting")
    print("4. create_sample_plot() - Generate sample plot")
    
    # Test basic plotting
    print("\nTesting basic plotting function...")
    try:
        plot_lulc_data(longitudes, latitudes, lulc_data,
                      title="Test LULC Plot",
                      extent=[-96.5, -94.0, 28.9, 30.5],
                      save_path="plots/test_plot.png", show_plot=False)
        print("✓ Basic plotting function works")
    except Exception as e:
        print(f"✗ Basic plotting failed: {e}")


if __name__ == "__main__":
    main()
    demonstrate_plotting_functions()
