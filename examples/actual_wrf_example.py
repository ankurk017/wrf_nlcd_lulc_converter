#!/usr/bin/env python3
"""
Actual WRF file example for the WRF NLCD LULC converter.

This example demonstrates using the actual WRF geo_em file instead of random data.
"""

import os
import sys
import numpy as np
import xarray as xr

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from wrf_nlcd_lulc_converter import (
    NLCDProcessor, LULCMapping, 
    plot_lulc_data, plot_urban_comparison, plot_domain_info,
    get_lulc_colormap, get_class_info, get_urban_classes
)
from wrf_nlcd_lulc_converter.utils import extract_wrf_domain_info


def main():
    """
    Main example using actual WRF file.
    """
    print("WRF NLCD LULC Converter - Actual WRF File Example")
    print("=" * 60)
    
    # Define the actual WRF file path
    wrf_file = "/nas/rstor/akumar/common/sample_geog/geo_em.d02.nc"
    
    if not os.path.exists(wrf_file):
        print(f"Error: WRF file not found: {wrf_file}")
        print("Please ensure the file exists and is accessible.")
        return
    
    # Create output directory
    os.makedirs("plots", exist_ok=True)
    
    try:
        # Extract WRF domain information
        print("1. Extracting WRF domain information...")
        wrf_info = extract_wrf_domain_info(wrf_file)
        
        longitudes = wrf_info['longitudes']
        latitudes = wrf_info['latitudes']
        lulc_data = wrf_info['lu_index']
        domain = wrf_info['domain']
        
        print(f"   Domain: {domain}")
        print(f"   Data shape: {lulc_data.shape}")
        print(f"   Longitude range: {longitudes.min():.3f} to {longitudes.max():.3f}")
        print(f"   Latitude range: {latitudes.min():.3f} to {latitudes.max():.3f}")
        
        # Analyze the data
        print("\n2. Analyzing LULC data...")
        unique_classes = np.unique(lulc_data)
        print(f"   Unique LULC classes: {unique_classes}")
        print(f"   Number of unique classes: {len(unique_classes)}")
        
        # Count pixels for each class
        class_counts = {}
        for class_num in unique_classes:
            count = np.sum(lulc_data == class_num)
            percentage = (count / lulc_data.size) * 100
            class_counts[class_num] = count
            
            # Get class info
            info = get_class_info(class_num)
            print(f"   Class {class_num:2d}: {info['label']:30s} - {count:8d} pixels ({percentage:5.1f}%)")
        
        # Analyze urban areas
        print("\n3. Analyzing urban areas...")
        urban_classes = get_urban_classes()
        urban_mask = np.isin(lulc_data, urban_classes)
        urban_pixels = np.sum(urban_mask)
        urban_percentage = (urban_pixels / lulc_data.size) * 100
        
        print(f"   Total urban pixels: {urban_pixels:,}")
        print(f"   Urban percentage: {urban_percentage:.2f}%")
        
        # Breakdown by urban class
        for urban_class in urban_classes:
            if urban_class in unique_classes:
                count = np.sum(lulc_data == urban_class)
                percentage = (count / lulc_data.size) * 100
                info = get_class_info(urban_class)
                print(f"     Class {urban_class}: {info['label']:25s} - {count:6d} pixels ({percentage:5.1f}%)")
        
        # Create plots
        print("\n4. Creating visualizations...")
        
        # Plot 1: Full domain LULC data
        print("   Creating full domain plot...")
        plot_lulc_data(longitudes, latitudes, lulc_data,
                      title="Actual WRF LULC Data - Full Domain",
                      extent=[domain['lon_min'], domain['lon_max'], 
                             domain['lat_min'], domain['lat_max']],
                      save_path="plots/actual_wrf_full_domain.png", show_plot=False)
        
        # Plot 2: Urban areas only
        print("   Creating urban areas plot...")
        urban_data = np.where(urban_mask, lulc_data, np.nan)
        plot_lulc_data(longitudes, latitudes, urban_data,
                      title="Urban Areas in WRF Domain",
                      extent=[domain['lon_min'], domain['lon_max'], 
                             domain['lat_min'], domain['lat_max']],
                      save_path="plots/actual_wrf_urban_areas.png", show_plot=False)
        
        # Plot 3: Domain info plot
        print("   Creating domain info plot...")
        plot_domain_info(wrf_info, 
                        title="WRF Domain Information",
                        save_path="plots/actual_wrf_domain_info.png", dpi=150)
        
        # Create a simulated "updated" dataset for comparison
        print("\n5. Creating comparison example...")
        
        # Simulate some urban expansion (for demonstration)
        updated_lulc = lulc_data.copy()
        
        # Find some non-urban areas near existing urban areas
        # This is just for demonstration - in real usage, this would come from NLCD processing
        for urban_class in urban_classes:
            if urban_class in unique_classes:
                # Find areas adjacent to existing urban areas
                urban_mask = (updated_lulc == urban_class)
                # Simple expansion simulation (just for demo)
                expansion_mask = np.random.random(updated_lulc.shape) < 0.01  # 1% expansion
                expansion_mask &= (updated_lulc != urban_class)  # Don't expand into same class
                updated_lulc[expansion_mask] = urban_class
        
        # Plot comparison
        print("   Creating before/after comparison...")
        plot_urban_comparison(lulc_data, updated_lulc, longitudes, latitudes,
                            title="Urban Area Comparison (Simulated Update)",
                            save_path="plots/actual_wrf_urban_comparison.png", dpi=150)
        
        # Statistics comparison
        print("\n6. Statistics comparison...")
        original_urban = np.sum(np.isin(lulc_data, urban_classes))
        updated_urban = np.sum(np.isin(updated_lulc, urban_classes))
        
        print(f"   Original urban pixels: {original_urban:,}")
        print(f"   Updated urban pixels: {updated_urban:,}")
        print(f"   Change: {updated_urban - original_urban:,} pixels")
        
        print(f"\nAll plots saved in the 'plots/' directory:")
        print(f"  - actual_wrf_full_domain.png")
        print(f"  - actual_wrf_urban_areas.png")
        print(f"  - actual_wrf_domain_info.png")
        print(f"  - actual_wrf_urban_comparison.png")
        
    except Exception as e:
        print(f"Error processing WRF file: {e}")
        import traceback
        traceback.print_exc()


def demonstrate_wrf_analysis():
    """
    Demonstrate WRF file analysis capabilities.
    """
    print("\n" + "=" * 60)
    print("WRF File Analysis Demonstrations")
    print("=" * 60)
    
    wrf_file = "/nas/rstor/akumar/common/sample_geog/geo_em.d02.nc"
    
    if not os.path.exists(wrf_file):
        print(f"WRF file not found: {wrf_file}")
        return
    
    try:
        # Read WRF file directly with xarray
        print("Reading WRF file with xarray...")
        with xr.open_dataset(wrf_file) as ds:
            print(f"  Dataset variables: {list(ds.variables.keys())}")
            print(f"  Dimensions: {dict(ds.dims)}")
            
            # Show LU_INDEX information
            if 'LU_INDEX' in ds.variables:
                lu_index = ds['LU_INDEX'].values.squeeze()
                print(f"  LU_INDEX shape: {lu_index.shape}")
                print(f"  LU_INDEX range: {lu_index.min()} to {lu_index.max()}")
                print(f"  LU_INDEX unique values: {np.unique(lu_index)}")
            
            # Show coordinate information
            if 'XLAT_M' in ds.variables and 'XLONG_M' in ds.variables:
                lats = ds['XLAT_M'].values.squeeze()
                lons = ds['XLONG_M'].values.squeeze()
                print(f"  Latitude range: {lats.min():.3f} to {lats.max():.3f}")
                print(f"  Longitude range: {lons.min():.3f} to {lons.max():.3f}")
        
        print("✓ WRF file analysis completed successfully")
        
    except Exception as e:
        print(f"✗ WRF file analysis failed: {e}")


if __name__ == "__main__":
    main()
    demonstrate_wrf_analysis()
