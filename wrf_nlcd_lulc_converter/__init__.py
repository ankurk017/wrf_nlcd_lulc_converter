"""
WRF NLCD LULC Converter

A Python package for converting National Land Cover Database (NLCD) land use data 
and updating WRF (Weather Research and Forecasting) geo_em files with new land use information.
"""

__version__ = "0.1.0"
__author__ = "Ankur Kumar"
__email__ = "ankur.kumar@example.com"

from .processor import NLCDProcessor
from .mapping import LULCMapping
from .utils import generate_landusef_from_lu_index
from .plotting import plot_lulc_data, plot_urban_comparison, plot_domain_info, create_sample_plot
from .colormap import (
    get_lulc_colormap, get_lulc_normalization, get_urban_colormap, 
    get_urban_normalization, create_colorbar, create_urban_colorbar,
    get_class_info, get_urban_classes, plot_colormap_legend
)

__all__ = [
    "NLCDProcessor",
    "LULCMapping", 
    "generate_landusef_from_lu_index",
    "plot_lulc_data",
    "plot_urban_comparison", 
    "plot_domain_info",
    "create_sample_plot",
    "get_lulc_colormap",
    "get_lulc_normalization",
    "get_urban_colormap",
    "get_urban_normalization",
    "create_colorbar",
    "create_urban_colorbar",
    "get_class_info",
    "get_urban_classes",
    "plot_colormap_legend",
]
