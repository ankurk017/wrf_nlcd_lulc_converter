# Plotting Functionality Summary

## Overview

The WRF NLCD LULC converter package now includes comprehensive plotting and visualization capabilities to help users understand and analyze their LULC data.

## New Plotting Module

### `wrf_nlcd_lulc_converter/plotting.py`

This module provides several key plotting functions:

#### 1. `plot_lulc_data()`
- **Purpose**: Plot LULC data with geographic context
- **Features**: 
  - Proper color mapping for 40 LULC classes
  - Geographic projections using cartopy
  - Coastlines and state boundaries
  - Customizable extent and title
  - Automatic saving capability

#### 2. `plot_urban_comparison()`
- **Purpose**: Compare urban areas before and after processing
- **Features**:
  - Side-by-side comparison plots
  - Focus on urban classes (21-24)
  - Before/after visualization
  - Shared colorbar for consistency

#### 3. `plot_domain_info()`
- **Purpose**: Visualize WRF domain information
- **Features**:
  - Plot WRF domain LULC data
  - Automatic extent calculation
  - Integration with WRF file reading

#### 4. `create_sample_plot()`
- **Purpose**: Generate demonstration plots
- **Features**:
  - Sample data generation
  - Realistic urban patterns
  - Houston area focus

## Example Usage

### Basic LULC Plotting
```python
from wrf_nlcd_lulc_converter import plot_lulc_data

# Plot LULC data
plot_lulc_data(longitudes, latitudes, lulc_data,
               title="My LULC Data",
               extent=[lon_min, lon_max, lat_min, lat_max],
               save_path="my_plot.png")
```

### Urban Comparison
```python
from wrf_nlcd_lulc_converter import plot_urban_comparison

# Compare before and after
plot_urban_comparison(original_lulc, updated_lulc, 
                     longitudes, latitudes,
                     title="Urban Area Changes",
                     save_path="urban_comparison.png")
```

### WRF Domain Visualization
```python
from wrf_nlcd_lulc_converter import plot_domain_info, extract_wrf_domain_info

# Extract and plot WRF domain
wrf_info = extract_wrf_domain_info("geo_em.d02.nc")
plot_domain_info(wrf_info, 
                title="WRF Domain LULC",
                save_path="wrf_domain.png")
```

## New Examples

### `examples/plotting_example.py`
Comprehensive plotting example that demonstrates:
- Sample plot creation
- Custom LULC data generation
- Urban area analysis
- WRF domain plotting
- LULC class statistics
- Urban area comparison

### Updated `examples/complete_workflow_example.py`
Now includes visualization step that creates:
- Original LULC plot
- Updated LULC plot  
- Urban comparison plot

### `examples/simple_wrf_example.py`
New example using actual WRF file that demonstrates:
- Real WRF data analysis (370,152 pixels)
- Actual LULC class distribution (28 classes)
- Urban area analysis (1.94% urban coverage)
- Multiple visualization types
- Statistics and comparisons

### `examples/colormap_example.py`
Demonstrates the colormap module with:
- All colormap functions
- Real WRF data integration
- Legend generation
- Urban-specific plotting

## Features

### Geographic Context
- Uses cartopy for proper geographic projections
- Includes coastlines, state boundaries, and borders
- Houston area outline for regional focus

### Color Mapping
- 40-class LULC color scheme
- Proper colorbar with class labels
- Consistent color mapping across plots

### Flexibility
- Customizable titles and extents
- Optional plot saving
- Configurable DPI and output formats
- Show/hide plot options

### Integration
- Works with existing package functions
- Integrates with WRF file reading
- Compatible with NLCD processing workflow

## Sample Output

The package includes a sample plot (`sample_lulc_plot.png`) that demonstrates:
- LULC class visualization
- Color mapping
- Geographic context
- Urban area highlighting

## Dependencies

The plotting functionality requires:
- `matplotlib` for basic plotting
- `cartopy` for geographic projections
- `numpy` for data handling
- `xarray` for NetCDF file reading

## Usage in Workflow

The plotting functions integrate seamlessly with the main processing workflow:

1. **Data Processing**: Process NLCD and WRF data
2. **Visualization**: Create plots to understand the data
3. **Comparison**: Visualize before/after changes
4. **Analysis**: Analyze urban area changes

This provides a complete workflow from data processing to visualization and analysis.
