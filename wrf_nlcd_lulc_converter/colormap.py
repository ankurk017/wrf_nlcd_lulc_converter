"""
Colormap and normalization utilities for WRF NLCD LULC converter.
"""

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np


def get_lulc_colormap():
    """
    Get the 40-class LULC colormap from the original notebook.
    
    Returns:
        tuple: (colormap, labels, colors, vmin, vmax)
    """
    # Define the exact 40-class LULC mapping from the notebook
    lulc_dict = {
        1:  {"label": "Evergreen Needleleaf Forest",         "color": "#05450a"},
        2:  {"label": "Evergreen Broadleaf Forest",          "color": "#086a10"},
        3:  {"label": "Deciduous Needleleaf Forest",         "color": "#54a708"},
        4:  {"label": "Deciduous Broadleaf Forest",          "color": "#78d203"},
        5:  {"label": "Mixed Forests",                       "color": "#009900"},
        6:  {"label": "Closed Shrublands",                   "color": "#c6b044"},
        7:  {"label": "Open Shrublands",                     "color": "#dcd159"},
        8:  {"label": "Woody Savannas",                      "color": "#dade48"},
        9:  {"label": "Savannas",                            "color": "#fbff13"},
        10: {"label": "Grasslands",                          "color": "#b6ff05"},
        11: {"label": "Permanent Wetlands",                  "color": "#27ff87"},
        12: {"label": "Croplands",                           "color": "#006400"},
        13: {"label": "Urban and Built Up",                  "color": "#FF0000"},
        14: {"label": "Cropland/Natural Vegetation Mosaic",  "color": "#ADFF2F"},
        15: {"label": "Permanent Snow and Ice",              "color": "#69fff8"},
        16: {"label": "Barren or Sparsely Vegetated",        "color": "#f9ffa4"},
        17: {"label": "IGBP Water",                          "color": "#1c0dff"},
        18: {"label": "Unclassified",                        "color": "#cccccc"},
        19: {"label": "Fill Value",                          "color": "#999999"},
        20: {"label": "Unclassified",                        "color": "#cccccc"},
        21: {"label": "Open Water",                          "color": "#1c0dff"},
        22: {"label": "Perennial Ice/Snow",                  "color": "#69fff8"},
        23: {"label": "Developed Open Space",                "color": "#ffb3b3"},
        24: {"label": "Developed Low Intensity",             "color": "#ff6666"},
        25: {"label": "Developed Medium Intensity",          "color": "#cc0000"},
        26: {"label": "Developed High Intensity",            "color": "#990000"},
        27: {"label": "Barren Land (Rock/Sand/Clay)",        "color": "#e2e2e2"},
        28: {"label": "Deciduous Forest",                    "color": "#b2df8a"},
        29: {"label": "Evergreen Forest",                    "color": "#33a02c"},
        30: {"label": "Mixed Forest",                        "color": "#6a3d9a"},
        31: {"label": "Dwarf Scrub",                         "color": "#cab2d6"},
        32: {"label": "Shrub/Scrub",                         "color": "#ffff99"},
        33: {"label": "Grassland/Herbaceous",                "color": "#b15928"},
        34: {"label": "Sedge/Herbaceous",                    "color": "#8dd3c7"},
        35: {"label": "Lichens",                             "color": "#fb8072"},
        36: {"label": "Moss",                                "color": "#80b1d3"},
        37: {"label": "Pasture/Hay",                         "color": "#fdb462"},
        38: {"label": "Cultivated Crops",                    "color": "#ffd92f"},
        39: {"label": "Woody Wetlands",                      "color": "#a6cee3"},
        40: {"label": "Emergent Herbaceous Wetlands",        "color": "#1f78b4"},
    }
    
    # Extract color list and label list in order for plotting
    lulc_colors = [lulc_dict[i]["color"] for i in range(1, 41)]
    lulc_labels = [lulc_dict[i]["label"] for i in range(1, 41)]
    
    # Create colormap
    cmap_40 = mcolors.ListedColormap(lulc_colors)
    
    # Define normalization bounds
    vmin = 1 - 0.5
    vmax = 40 + 0.5
    
    return cmap_40, lulc_labels, lulc_colors, vmin, vmax


def get_lulc_normalization():
    """
    Get the normalization for LULC data plotting.
    
    Returns:
        tuple: (vmin, vmax, ticks, tick_labels)
    """
    _, labels, _, vmin, vmax = get_lulc_colormap()
    
    # Create ticks and tick labels
    ticks = np.arange(1, 41)
    tick_labels = [f"{i+1}: {labels[i]}" for i in range(40)]
    
    return vmin, vmax, ticks, tick_labels


def get_urban_colormap():
    """
    Get a colormap specifically for urban classes (21-26).
    
    Returns:
        tuple: (colormap, labels, colors, vmin, vmax)
    """
    # Urban class colors
    urban_colors = [
        "#1c0dff",  # 21: Open Water
        "#69fff8",  # 22: Perennial Ice/Snow
        "#ffb3b3",  # 23: Developed Open Space
        "#ff6666",  # 24: Developed Low Intensity
        "#cc0000",  # 25: Developed Medium Intensity
        "#990000",  # 26: Developed High Intensity
    ]
    
    urban_labels = [
        "Open Water",
        "Perennial Ice/Snow", 
        "Developed Open Space",
        "Developed Low Intensity",
        "Developed Medium Intensity",
        "Developed High Intensity"
    ]
    
    # Create colormap
    cmap_urban = mcolors.ListedColormap(urban_colors)
    
    # Define normalization bounds
    vmin = 21 - 0.5
    vmax = 26 + 0.5
    
    return cmap_urban, urban_labels, urban_colors, vmin, vmax


def get_urban_normalization():
    """
    Get the normalization for urban data plotting.
    
    Returns:
        tuple: (vmin, vmax, ticks, tick_labels)
    """
    _, labels, _, vmin, vmax = get_urban_colormap()
    
    # Create ticks and tick labels
    ticks = np.arange(21, 27)
    tick_labels = [f"{i}: {labels[i-21]}" for i in range(21, 27)]
    
    return vmin, vmax, ticks, tick_labels


def create_colorbar(ax, mappable, orientation='vertical', fraction=0.046, pad=0.04):
    """
    Create a standardized colorbar for LULC plots.
    
    Parameters:
        ax: Matplotlib axes object
        mappable: Mappable object (e.g., pcolormesh result)
        orientation (str): Colorbar orientation
        fraction (float): Colorbar fraction
        pad (float): Colorbar padding
        
    Returns:
        matplotlib.colorbar.Colorbar: The created colorbar
    """
    vmin, vmax, ticks, tick_labels = get_lulc_normalization()
    
    cbar = plt.colorbar(mappable, ax=ax, orientation=orientation, 
                        fraction=fraction, pad=pad, ticks=ticks)
    cbar.set_label('LULC Class')
    cbar.set_ticks(ticks)
    cbar.set_ticklabels(tick_labels)
    
    return cbar


def create_urban_colorbar(ax, mappable, orientation='vertical', fraction=0.046, pad=0.04):
    """
    Create a standardized colorbar for urban plots.
    
    Parameters:
        ax: Matplotlib axes object
        mappable: Mappable object (e.g., pcolormesh result)
        orientation (str): Colorbar orientation
        fraction (float): Colorbar fraction
        pad (float): Colorbar padding
        
    Returns:
        matplotlib.colorbar.Colorbar: The created colorbar
    """
    vmin, vmax, ticks, tick_labels = get_urban_normalization()
    
    cbar = plt.colorbar(mappable, ax=ax, orientation=orientation, 
                        fraction=fraction, pad=pad, ticks=ticks)
    cbar.set_label('Urban LULC Class')
    cbar.set_ticks(ticks)
    cbar.set_ticklabels(tick_labels)
    
    return cbar


def get_class_info(class_number):
    """
    Get information for a specific LULC class.
    
    Parameters:
        class_number (int or float): LULC class number (1-40)
        
    Returns:
        dict: Dictionary with 'label' and 'color' keys
    """
    cmap, labels, colors, _, _ = get_lulc_colormap()
    
    # Convert to integer if it's a float
    class_number = int(class_number)
    
    if 1 <= class_number <= 40:
        return {
            "label": labels[class_number - 1],
            "color": colors[class_number - 1]
        }
    else:
        return {"label": "Unknown", "color": "#000000"}


def get_urban_classes():
    """
    Get list of urban development classes.
    
    Returns:
        list: List of urban class numbers
    """
    return [21, 22, 23, 24, 25, 26]


def plot_colormap_legend(save_path=None, dpi=150):
    """
    Create a legend showing all LULC classes and their colors.
    
    Parameters:
        save_path (str): Path to save the legend (optional)
        dpi (int): DPI for saved image
    """
    cmap, labels, colors, _, _ = get_lulc_colormap()
    
    fig, ax = plt.subplots(1, 1, figsize=(12, 16))
    
    # Create color patches
    for i, (label, color) in enumerate(zip(labels, colors)):
        ax.add_patch(plt.Rectangle((0, i), 1, 1, facecolor=color, edgecolor='black'))
        ax.text(1.1, i + 0.5, f"{i+1:2d}: {label}", va='center', fontsize=10)
    
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 40)
    ax.set_title("LULC Class Legend", fontsize=14, fontweight='bold')
    ax.axis('off')
    
    if save_path:
        plt.savefig(save_path, dpi=dpi, bbox_inches='tight')
        print(f"Legend saved to: {save_path}")
    
    plt.show()
    return fig, ax
