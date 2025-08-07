"""
Land Use/Land Cover (LULC) mapping definitions and utilities.
"""

import matplotlib.colors as mcolors
import numpy as np


class LULCMapping:
    """
    Class containing land use/land cover class definitions and color mappings.
    """
    
    def __init__(self):
        # Define the 40-class LULC mapping as a dictionary
        self.lulc_dict = {
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
        self.lulc_colors = [self.lulc_dict[i]["color"] for i in range(1, 41)]
        self.lulc_labels = [self.lulc_dict[i]["label"] for i in range(1, 41)]
        
        # Create matplotlib colormap
        self.cmap_40 = mcolors.ListedColormap(self.lulc_colors)
        
        # Default NLCD to WRF/GEOG urban class mapping
        self.nlcd_to_geog_urban = {
            21: 23,  # Open Water -> Developed Open Space
            22: 24,  # Perennial Ice/Snow -> Developed Low Intensity  
            23: 25,  # Developed Open Space -> Developed Medium Intensity
            24: 26,  # Developed Low Intensity -> Developed High Intensity
        }
    
    def get_class_info(self, class_number):
        """
        Get information for a specific LULC class.
        
        Parameters:
            class_number (int): LULC class number (1-40)
            
        Returns:
            dict: Dictionary with 'label' and 'color' keys
        """
        return self.lulc_dict.get(class_number, {"label": "Unknown", "color": "#000000"})
    
    def get_urban_classes(self):
        """
        Get list of urban development classes.
        
        Returns:
            list: List of urban class numbers
        """
        return [21, 22, 23, 24]
    
    def get_nlcd_to_geog_mapping(self):
        """
        Get the NLCD to WRF/GEOG urban class mapping.
        
        Returns:
            dict: Mapping dictionary
        """
        return self.nlcd_to_geog_urban.copy()
    
    def set_custom_mapping(self, mapping_dict):
        """
        Set a custom NLCD to WRF/GEOG mapping.
        
        Parameters:
            mapping_dict (dict): Custom mapping dictionary
        """
        self.nlcd_to_geog_urban = mapping_dict.copy()


# Create a global instance for easy access
lulc_mapping = LULCMapping()
