"""
Plotting utilities for WRF NLCD LULC converter.
"""

import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from .mapping import LULCMapping
from .colormap import get_lulc_colormap, get_lulc_normalization, create_colorbar


def plot_coast(ax, houston=True, houston_color='k', houston_linewidth=0.5):
    """
    Add coastlines and state boundaries to a cartopy plot.
    
    Parameters:
        ax: Cartopy axes object
        houston (bool): Whether to add Houston area outline
        houston_color (str): Color for Houston outline
        houston_linewidth (float): Line width for Houston outline
    """
    # Add coastlines
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
    ax.add_feature(cfeature.STATES, linewidth=0.3)
    ax.add_feature(cfeature.BORDERS, linewidth=0.5)
    
    if houston:
        # Add Houston area outline (approximate)
        houston_lon = [-95.5, -95.0, -95.0, -95.5, -95.5]
        houston_lat = [29.5, 29.5, 30.0, 30.0, 29.5]
        ax.plot(houston_lon, houston_lat, color=houston_color, 
                linewidth=houston_linewidth, transform=ccrs.PlateCarree())


def plot_lulc_data(longitudes, latitudes, lulc_data, title="LULC Data", 
                   extent=None, save_path=None, dpi=150, show_plot=True):
    """
    Plot LULC data with proper color mapping and labels.
    
    Parameters:
        longitudes (np.ndarray): Longitude coordinates
        latitudes (np.ndarray): Latitude coordinates
        lulc_data (np.ndarray): LULC class data
        title (str): Plot title
        extent (list): Map extent [lon_min, lon_max, lat_min, lat_max]
        save_path (str): Path to save the plot (optional)
        dpi (int): DPI for saved image
        show_plot (bool): Whether to display the plot
    """
    # Get colormap and normalization
    cmap, _, _, vmin, vmax = get_lulc_colormap()
    
    # Create figure
    fig, ax = plt.subplots(1, 1, figsize=(15, 8), 
                           subplot_kw={'projection': ccrs.PlateCarree()})
    
    # Plot LULC data using the exact colormap from the notebook
    out = ax.pcolormesh(longitudes, latitudes, lulc_data, 
                        cmap=cmap, vmin=vmin, vmax=vmax)
    
    # Add coastlines
    plot_coast(ax, houston=True, houston_color='k', houston_linewidth=0.5)
    
    # Add standardized colorbar
    create_colorbar(ax, out)
    
    # Set extent if provided
    if extent:
        ax.set_extent(extent)
    
    ax.set_title(title)
    
    # Save plot if path provided
    if save_path:
        plt.savefig(save_path, dpi=dpi, bbox_inches='tight')
        print(f"Plot saved to: {save_path}")
    
    if show_plot:
        plt.show()
    
    return fig, ax


def plot_urban_comparison(original_lulc, updated_lulc, longitudes, latitudes, 
                         title="Urban Area Comparison", save_path=None, dpi=150):
    """
    Plot comparison of original vs updated urban areas.
    
    Parameters:
        original_lulc (np.ndarray): Original LULC data
        updated_lulc (np.ndarray): Updated LULC data
        longitudes (np.ndarray): Longitude coordinates
        latitudes (np.ndarray): Latitude coordinates
        title (str): Plot title
        save_path (str): Path to save the plot (optional)
        dpi (int): DPI for saved image
    """
    # Get colormap and normalization
    cmap, _, _, vmin, vmax = get_lulc_colormap()
    urban_classes = [21, 22, 23, 24, 25, 26]
    
    # Create figure with subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8), 
                                    subplot_kw={'projection': ccrs.PlateCarree()})
    
    # Plot original urban areas
    urban_mask_original = np.isin(original_lulc, urban_classes)
    urban_original = np.where(urban_mask_original, original_lulc, np.nan)
    
    out1 = ax1.pcolormesh(longitudes, latitudes, urban_original, 
                          cmap=cmap, vmin=vmin, vmax=vmax)
    plot_coast(ax1, houston=True, houston_color='k', houston_linewidth=0.5)
    ax1.set_title("Original Urban Areas")
    
    # Plot updated urban areas
    urban_mask_updated = np.isin(updated_lulc, urban_classes)
    urban_updated = np.where(urban_mask_updated, updated_lulc, np.nan)
    
    out2 = ax2.pcolormesh(longitudes, latitudes, urban_updated, 
                          cmap=cmap, vmin=vmin, vmax=vmax)
    plot_coast(ax2, houston=True, houston_color='k', houston_linewidth=0.5)
    ax2.set_title("Updated Urban Areas")
    
    # Add standardized colorbar
    create_colorbar(ax1, out1)
    
    plt.suptitle(title)
    
    # Save plot if path provided
    if save_path:
        plt.savefig(save_path, dpi=dpi, bbox_inches='tight')
        print(f"Comparison plot saved to: {save_path}")
    
    plt.show()
    return fig, (ax1, ax2)


def plot_domain_info(wrf_info, title="WRF Domain Information", save_path=None, dpi=150):
    """
    Plot WRF domain information with LULC data.
    
    Parameters:
        wrf_info (dict): WRF domain information from extract_wrf_domain_info
        title (str): Plot title
        save_path (str): Path to save the plot (optional)
        dpi (int): DPI for saved image
    """
    longitudes = wrf_info['longitudes']
    latitudes = wrf_info['latitudes']
    lulc_data = wrf_info['lu_index']
    domain = wrf_info['domain']
    
    # Set extent based on domain
    extent = [domain['lon_min'], domain['lon_max'], 
              domain['lat_min'], domain['lat_max']]
    
    return plot_lulc_data(longitudes, latitudes, lulc_data, title, extent, save_path, dpi)


def create_sample_plot():
    """
    Create a sample plot for demonstration purposes.
    
    Returns:
        str: Path to the saved plot
    """
    # Get colormap and normalization
    cmap, _, _, vmin, vmax = get_lulc_colormap()
    
    # Sample domain (Houston area)
    lon_min, lon_max = -96.5, -94.0
    lat_min, lat_max = 28.9, 30.5
    
    # Create grid
    nx, ny = 100, 80
    longitudes = np.linspace(lon_min, lon_max, nx)
    latitudes = np.linspace(lat_min, lat_max, ny)
    
    # Create sample LULC data
    lulc_data = np.random.randint(1, 41, size=(ny, nx))
    
    # Add some urban areas
    urban_classes = [21, 22, 23, 24, 25, 26]
    urban_mask = np.random.random((ny, nx)) < 0.1  # 10% urban
    lulc_data[urban_mask] = np.random.choice(urban_classes, size=np.sum(urban_mask))
    
    # Plot and save
    save_path = "sample_lulc_plot.png"
    plot_lulc_data(longitudes, latitudes, lulc_data, 
                   title="Sample LULC Data (Houston Area)", 
                   extent=[lon_min, lon_max, lat_min, lat_max],
                   save_path=save_path, show_plot=False)
    
    return save_path
