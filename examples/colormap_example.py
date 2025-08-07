#!/usr/bin/env python3
"""
Colormap example for the WRF NLCD LULC converter.

This example demonstrates the new colormap module functionality.
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from wrf_nlcd_lulc_converter import (
    get_lulc_colormap, get_lulc_normalization, get_urban_colormap,
    get_urban_normalization, create_colorbar, create_urban_colorbar,
    get_class_info, get_urban_classes, plot_colormap_legend
)


def main():
    """
    Demonstrate the colormap module functionality.
    """
    print("WRF NLCD LULC Converter - Colormap Example")
    print("=" * 50)
    
    # Create output directory
    os.makedirs("plots", exist_ok=True)
    
    # Example 1: Get LULC colormap
    print("\n1. Getting LULC colormap...")
    cmap, labels, colors, vmin, vmax = get_lulc_colormap()
    print(f"  Colormap: {type(cmap)}")
    print(f"  Number of classes: {len(labels)}")
    print(f"  Vmin: {vmin}, Vmax: {vmax}")
    print(f"  First 5 labels: {labels[:5]}")
    
    # Example 2: Get normalization
    print("\n2. Getting LULC normalization...")
    norm_vmin, norm_vmax, ticks, tick_labels = get_lulc_normalization()
    print(f"  Normalization bounds: {norm_vmin} to {norm_vmax}")
    print(f"  Number of ticks: {len(ticks)}")
    print(f"  First 5 tick labels: {tick_labels[:5]}")
    
    # Example 3: Get urban colormap
    print("\n3. Getting urban colormap...")
    urban_cmap, urban_labels, urban_colors, urban_vmin, urban_vmax = get_urban_colormap()
    print(f"  Urban colormap: {type(urban_cmap)}")
    print(f"  Urban classes: {urban_labels}")
    print(f"  Urban bounds: {urban_vmin} to {urban_vmax}")
    
    # Example 4: Get class information
    print("\n4. Getting class information...")
    for class_num in [1, 13, 21, 23, 26, 40]:
        info = get_class_info(class_num)
        print(f"  Class {class_num:2d}: {info['label']:30s} - Color: {info['color']}")
    
    # Example 5: Get urban classes
    print("\n5. Getting urban classes...")
    urban_classes = get_urban_classes()
    print(f"  Urban classes: {urban_classes}")
    
    # Example 6: Create a plot with actual WRF data
    print("\n6. Creating plot with actual WRF data...")
    
    # Use actual WRF file
    wrf_file = "/nas/rstor/akumar/common/sample_geog/geo_em.d02.nc"
    
    if os.path.exists(wrf_file):
        try:
            # Extract WRF data
            from wrf_nlcd_lulc_converter.utils import extract_wrf_domain_info
            wrf_info = extract_wrf_domain_info(wrf_file)
            
            longitudes = wrf_info['longitudes']
            latitudes = wrf_info['latitudes']
            lulc_data = wrf_info['lu_index']
            domain = wrf_info['domain']
            
            print(f"  WRF domain: {domain}")
            print(f"  Data shape: {lulc_data.shape}")
            print(f"  Unique classes: {np.unique(lulc_data)}")
            
        except Exception as e:
            print(f"  Could not read WRF file: {e}")
            # Fallback to sample data
            nx, ny = 50, 40
            longitudes = np.linspace(-96.5, -94.0, nx)
            latitudes = np.linspace(28.9, 30.5, ny)
            lulc_data = np.random.randint(1, 41, size=(ny, nx))
            
            # Add some urban areas
            urban_classes = get_urban_classes()
            urban_mask = np.random.random((ny, nx)) < 0.1
            lulc_data[urban_mask] = np.random.choice(urban_classes, size=np.sum(urban_mask))
    else:
        print(f"  WRF file not found: {wrf_file}")
        # Fallback to sample data
        nx, ny = 50, 40
        longitudes = np.linspace(-96.5, -94.0, nx)
        latitudes = np.linspace(28.9, 30.5, ny)
        lulc_data = np.random.randint(1, 41, size=(ny, nx))
        
        # Add some urban areas
        urban_classes = get_urban_classes()
        urban_mask = np.random.random((ny, nx)) < 0.1
        lulc_data[urban_mask] = np.random.choice(urban_classes, size=np.sum(urban_mask))
    
    # Create plot
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    
    # Plot with colormap
    im = ax.pcolormesh(longitudes, latitudes, lulc_data, 
                       cmap=cmap, vmin=vmin, vmax=vmax)
    
    # Add colorbar using the standardized function
    create_colorbar(ax, im)
    
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    if os.path.exists(wrf_file):
        ax.set_title('Actual WRF LULC Data with Colormap Module')
    else:
        ax.set_title('Sample LULC Data with Colormap Module')
    
    # Save plot
    if os.path.exists(wrf_file):
        save_path = "plots/actual_wrf_colormap_example.png"
    else:
        save_path = "plots/colormap_example.png"
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    print(f"  Plot saved to: {save_path}")
    
    # Example 7: Create colormap legend
    print("\n7. Creating colormap legend...")
    legend_path = "plots/lulc_legend.png"
    plot_colormap_legend(save_path=legend_path, dpi=150)
    print(f"  Legend saved to: {legend_path}")
    
    # Example 8: Demonstrate urban-specific plotting
    print("\n8. Creating urban-specific plot...")
    
    # Create urban-only data from the same dataset
    urban_data = np.where(np.isin(lulc_data, urban_classes), lulc_data, np.nan)
    
    fig2, ax2 = plt.subplots(1, 1, figsize=(10, 6))
    im2 = ax2.pcolormesh(longitudes, latitudes, urban_data, 
                         cmap=urban_cmap, vmin=urban_vmin, vmax=urban_vmax)
    
    # Add urban colorbar
    create_urban_colorbar(ax2, im2)
    
    ax2.set_xlabel('Longitude')
    ax2.set_ylabel('Latitude')
    if os.path.exists(wrf_file):
        ax2.set_title('Urban Areas Only (Actual WRF Data)')
    else:
        ax2.set_title('Urban Areas Only')
    
    # Save urban plot
    if os.path.exists(wrf_file):
        urban_path = "plots/actual_wrf_urban_example.png"
    else:
        urban_path = "plots/urban_example.png"
    plt.savefig(urban_path, dpi=150, bbox_inches='tight')
    print(f"  Urban plot saved to: {urban_path}")
    
    print(f"\nAll examples completed! Check the 'plots/' directory for outputs.")


def demonstrate_colormap_functions():
    """
    Demonstrate individual colormap functions.
    """
    print("\n" + "=" * 50)
    print("Colormap Function Demonstrations")
    print("=" * 50)
    
    print("Available colormap functions:")
    print("1. get_lulc_colormap() - Get 40-class LULC colormap")
    print("2. get_lulc_normalization() - Get LULC normalization")
    print("3. get_urban_colormap() - Get urban-specific colormap")
    print("4. get_urban_normalization() - Get urban normalization")
    print("5. create_colorbar() - Create standardized LULC colorbar")
    print("6. create_urban_colorbar() - Create urban colorbar")
    print("7. get_class_info() - Get information for specific class")
    print("8. get_urban_classes() - Get list of urban classes")
    print("9. plot_colormap_legend() - Create colormap legend")
    
    # Test colormap functions
    print("\nTesting colormap functions...")
    
    try:
        # Test LULC colormap
        cmap, labels, colors, vmin, vmax = get_lulc_colormap()
        print("✓ LULC colormap function works")
        
        # Test normalization
        norm_vmin, norm_vmax, ticks, tick_labels = get_lulc_normalization()
        print("✓ LULC normalization function works")
        
        # Test class info
        info = get_class_info(23)
        print(f"✓ Class info function works: Class 23 = {info['label']}")
        
        # Test urban classes
        urban_classes = get_urban_classes()
        print(f"✓ Urban classes function works: {urban_classes}")
        
    except Exception as e:
        print(f"✗ Colormap function test failed: {e}")


if __name__ == "__main__":
    main()
    demonstrate_colormap_functions()
