#!/usr/bin/env python3
"""
Simple WRF file example that doesn't require all dependencies.

This example demonstrates using the actual WRF geo_em file with minimal dependencies.
"""

import os
import sys
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import only what we need (avoiding rasterio dependency)
from wrf_nlcd_lulc_converter.colormap import get_lulc_colormap, get_class_info, get_urban_classes


def extract_wrf_domain_info_simple(wrf_file):
    """
    Simple WRF domain extraction without complex dependencies.
    """
    with xr.open_dataset(wrf_file) as ds:
        # Extract coordinates
        geog_latitudes = ds['XLAT_M'].values.squeeze()
        geog_longitudes = ds['XLONG_M'].values.squeeze()
        
        geog_latitudes_1d = geog_latitudes[:, 0]
        geog_longitudes_1d = geog_longitudes[0, :]
        
        geog01_lulc = ds['LU_INDEX'].values.squeeze()
        
        geog_roi_domain = {
            'lon_min': geog_longitudes_1d[0], 
            'lon_max': geog_longitudes_1d[-1], 
            'lat_min': geog_latitudes_1d[0], 
            'lat_max': geog_latitudes_1d[-1]
        }
        
        return {
            'latitudes': geog_latitudes_1d,
            'longitudes': geog_longitudes_1d,
            'lu_index': geog01_lulc,
            'domain': geog_roi_domain
        }


def plot_lulc_data_simple(longitudes, latitudes, lulc_data, title="LULC Data", 
                          save_path=None, dpi=150, show_plot=True):
    """
    Simple LULC plotting without cartopy dependency.
    """
    # Get colormap
    cmap, labels, colors, vmin, vmax = get_lulc_colormap()
    
    # Create figure
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    
    # Plot LULC data
    im = ax.pcolormesh(longitudes, latitudes, lulc_data, 
                       cmap=cmap, vmin=vmin, vmax=vmax)
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax, orientation='vertical', 
                        fraction=0.046, pad=0.04, ticks=np.arange(1, 41))
    cbar.set_label('LULC Class')
    cbar.set_ticks(np.arange(1, 41))
    cbar.set_ticklabels([f"{i+1}: {labels[i]}" for i in range(40)])
    
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_title(title)
    
    # Save plot if path provided
    if save_path:
        plt.savefig(save_path, dpi=dpi, bbox_inches='tight')
        print(f"Plot saved to: {save_path}")
    
    if show_plot:
        plt.show()
    
    return fig, ax


def main():
    """
    Main example using actual WRF file with minimal dependencies.
    """
    print("WRF NLCD LULC Converter - Simple WRF File Example")
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
        wrf_info = extract_wrf_domain_info_simple(wrf_file)
        
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
            
            # Get class info (convert float to int)
            info = get_class_info(int(class_num))
            print(f"   Class {int(class_num):2d}: {info['label']:30s} - {count:8d} pixels ({percentage:5.1f}%)")
        
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
        plot_lulc_data_simple(longitudes, latitudes, lulc_data,
                             title="Actual WRF LULC Data - Full Domain",
                             save_path="plots/simple_wrf_full_domain.png", show_plot=False)
        
        # Plot 2: Urban areas only
        print("   Creating urban areas plot...")
        urban_data = np.where(urban_mask, lulc_data, np.nan)
        plot_lulc_data_simple(longitudes, latitudes, urban_data,
                             title="Urban Areas in WRF Domain",
                             save_path="plots/simple_wrf_urban_areas.png", show_plot=False)
        
        # Create a simulated "updated" dataset for comparison
        print("\n5. Creating comparison example...")
        
        # Simulate some urban expansion (for demonstration)
        updated_lulc = lulc_data.copy()
        
        # Simple expansion simulation
        for urban_class in urban_classes:
            if urban_class in unique_classes:
                # Simple expansion simulation (just for demo)
                expansion_mask = np.random.random(updated_lulc.shape) < 0.005  # 0.5% expansion
                expansion_mask &= (updated_lulc != urban_class)  # Don't expand into same class
                updated_lulc[expansion_mask] = urban_class
        
        # Plot comparison
        print("   Creating before/after comparison...")
        
        # Create comparison plot
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Original data
        cmap, labels, colors, vmin, vmax = get_lulc_colormap()
        im1 = ax1.pcolormesh(longitudes, latitudes, lulc_data, cmap=cmap, vmin=vmin, vmax=vmax)
        ax1.set_title("Original LULC Data")
        ax1.set_xlabel('Longitude')
        ax1.set_ylabel('Latitude')
        
        # Updated data
        im2 = ax2.pcolormesh(longitudes, latitudes, updated_lulc, cmap=cmap, vmin=vmin, vmax=vmax)
        ax2.set_title("Updated LULC Data (Simulated)")
        ax2.set_xlabel('Longitude')
        ax2.set_ylabel('Latitude')
        
        # Add colorbar
        cbar = plt.colorbar(im1, ax=[ax1, ax2], orientation='vertical', 
                           fraction=0.046, pad=0.04, ticks=np.arange(1, 41))
        cbar.set_label('LULC Class')
        cbar.set_ticks(np.arange(1, 41))
        cbar.set_ticklabels([f"{i+1}: {labels[i]}" for i in range(40)])
        
        plt.tight_layout()
        plt.savefig("plots/simple_wrf_comparison.png", dpi=150, bbox_inches='tight')
        print("   Comparison plot saved to: plots/simple_wrf_comparison.png")
        
        # Statistics comparison
        print("\n6. Statistics comparison...")
        original_urban = np.sum(np.isin(lulc_data, urban_classes))
        updated_urban = np.sum(np.isin(updated_lulc, urban_classes))
        
        print(f"   Original urban pixels: {original_urban:,}")
        print(f"   Updated urban pixels: {updated_urban:,}")
        print(f"   Change: {updated_urban - original_urban:,} pixels")
        
        print(f"\nAll plots saved in the 'plots/' directory:")
        print(f"  - simple_wrf_full_domain.png")
        print(f"  - simple_wrf_urban_areas.png")
        print(f"  - simple_wrf_comparison.png")
        
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
