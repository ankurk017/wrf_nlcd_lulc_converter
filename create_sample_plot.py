#!/usr/bin/env python3
"""
Create a sample LULC plot for the README.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

def create_sample_plot():
    """Create a sample LULC plot."""
    
    # Import the colormap functions
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'wrf_nlcd_lulc_converter'))
    from colormap import get_lulc_colormap, get_lulc_normalization
    
    # Get colormap and normalization
    cmap, labels, colors, vmin, vmax = get_lulc_colormap()
    
    # Create sample data
    nx, ny = 100, 80
    lon_min, lon_max = -96.5, -94.0
    lat_min, lat_max = 28.9, 30.5
    
    longitudes = np.linspace(lon_min, lon_max, nx)
    latitudes = np.linspace(lat_min, lat_max, ny)
    
    # Create sample LULC data
    lulc_data = np.random.randint(1, 41, size=(ny, nx))
    
    # Add some urban areas (classes 23-26 for demo)
    urban_mask = np.random.random((ny, nx)) < 0.1
    lulc_data[urban_mask] = np.random.choice([23, 24, 25, 26], size=np.sum(urban_mask))
    
    # Create plot
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    
    # Plot data
    im = ax.pcolormesh(longitudes, latitudes, lulc_data, 
                       cmap=cmap, vmin=vmin, vmax=vmax)
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax, orientation='vertical', 
                        fraction=0.046, pad=0.04, ticks=np.arange(1, 41))
    cbar.set_label('LULC Class')
    cbar.set_ticks(np.arange(1, 41))
    cbar.set_ticklabels([f"{i+1}: {labels[i]}" for i in range(40)])
    
    # Set labels and title
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_title('Sample LULC Data (Houston Area)')
    
    # Save plot
    plt.savefig('sample_lulc_plot.png', dpi=150, bbox_inches='tight')
    print("Sample plot saved as: sample_lulc_plot.png")
    
    return 'sample_lulc_plot.png'

if __name__ == "__main__":
    create_sample_plot()
