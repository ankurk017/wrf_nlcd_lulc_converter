# WRF NLCD LULC Converter Package Summary

## Overview

This package has been converted from the Jupyter notebook `NLCD_replace_geo_em.ipynb` into a comprehensive Python package for processing National Land Cover Database (NLCD) data and updating WRF (Weather Research and Forecasting) geo_em files.

## Repository Information

- **GitHub Repository**: https://github.com/ankurk017/wrf_nlcd_lulc_converter
- **Author**: Ankur Kumar
- **License**: Apache 2.0
- **Python Version**: 3.8+

## Package Structure

```
wrf_nlcd_lulc_converter/
├── setup.py                          # Package configuration
├── requirements.txt                   # Python dependencies
├── README.md                         # Comprehensive documentation
├── INSTALL.md                        # Installation guide
├── MANIFEST.in                       # Package distribution files
├── test_installation.py              # Installation test script
├── wrf_nlcd_lulc_converter/         # Main package
│   ├── __init__.py                   # Package initialization
│   ├── processor.py                  # Main processing class
│   ├── mapping.py                    # LULC class definitions
│   ├── utils.py                      # Utility functions
│   └── cli.py                       # Command-line interface
├── examples/                         # Usage examples
│   ├── basic_example.py             # Basic usage
│   ├── custom_mapping_example.py    # Custom mappings
│   ├── urban_only_example.py        # Urban-only processing
│   └── complete_workflow_example.py # Complete workflow
└── tests/                           # Unit tests
    └── test_processor.py            # Core functionality tests
```

## Key Features

### 1. **NLCDProcessor** - Main Processing Class
- `process_nlcd_and_update_wrf()`: Full NLCD processing workflow
- `process_urban_only()`: Process only urban classes
- `set_custom_mapping()`: Custom NLCD to WRF class mappings
- `get_processing_info()`: Configuration information

### 2. **LULCMapping** - Class Definitions
- 40-class LULC definitions with colors and labels
- Default NLCD to WRF/GEOG mappings
- Urban class identification (classes 21-24)
- Custom mapping support

### 3. **Utility Functions**
- `generate_landusef_from_lu_index()`: Generate LANDUSEF arrays
- `crop_nlcd_with_gdalwarp()`: Crop NLCD GeoTIFF files
- `update_lu_index_and_landusef_in_netcdf()`: Update WRF files
- `extract_wrf_domain_info()`: Extract WRF domain information

### 4. **Command-Line Interface**
- Easy-to-use CLI for batch processing
- Support for all major features
- Helpful error messages and validation

## Installation

```bash
# Clone the repository
git clone https://github.com/ankurk017/wrf-nlcd-lulc-converter.git
cd wrf-nlcd-lulc-converter

# Install in development mode
pip install -e .

# Test installation
python test_installation.py
```

## Usage Examples

### Command Line Interface

```bash
# Basic usage
wrf-nlcd-converter --nlcd-file nlcd_2017.tif --wrf-file geo_em.d02.nc --output-file geo_em_updated.nc --year 2017

# Urban-only processing
wrf-nlcd-converter --nlcd-file nlcd_2017.tif --wrf-file geo_em.d02.nc --output-file geo_em_urban.nc --year 2017 --urban-only

# With custom margin
wrf-nlcd-converter --nlcd-file nlcd_2017.tif --wrf-file geo_em.d02.nc --output-file geo_em_updated.nc --year 2017 --margin 2.0

# Show processor information
wrf-nlcd-converter --info
```

### Python API

```python
from wrf_nlcd_lulc_converter import NLCDProcessor

# Initialize processor
processor = NLCDProcessor()

# Process NLCD data and update WRF file
processor.process_nlcd_and_update_wrf(
    nlcd_file="path/to/nlcd.tif",
    wrf_file="path/to/geo_em.d02.nc",
    output_file="path/to/geo_em_updated.nc",
    year="2017"
)
```

## Improvements Over Original Notebook

1. **Modularity**: Code is organized into logical modules
2. **Reusability**: Can be imported and used in other projects
3. **Error Handling**: Comprehensive error handling and validation
4. **Documentation**: Detailed docstrings and examples
5. **Testing**: Unit tests for reliability
6. **CLI**: Command-line interface for batch processing
7. **Flexibility**: Support for custom mappings and parameters
8. **Professional Structure**: Proper Python package structure

## Data Requirements

### NLCD Data
- Download from [MRLC Viewer](https://www.mrlc.gov/data)
- Annual NLCD Land Cover data (GeoTIFF format)
- File naming: `Annual_NLCD_LndCov_YYYY_CU_C1V1.tif`

### WRF geo_em Files
- Generated using WPS (WRF Preprocessing System)
- NetCDF format with LU_INDEX and LANDUSEF variables
- Domain-specific files (e.g., `geo_em.d02.nc`)

## System Requirements

- **Python**: 3.8 or higher
- **GDAL**: For GeoTIFF processing
- **NetCDF4**: For NetCDF file handling
- **Memory**: 4GB+ RAM recommended
- **Storage**: 1GB+ free space for temporary files

## Testing

```bash
# Run installation test
python test_installation.py

# Run unit tests
python -m pytest tests/

# Test examples
python examples/basic_example.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.

## Citation

If you use this package in your research, please cite:

```bibtex
@software{wrf_nlcd_lulc_converter,
  title={WRF NLCD LULC Converter},
  author={Ankur Kumar},
  year={2024},
  url={https://github.com/ankurk017/wrf-nlcd-lulc-converter}
}
```

## Support

- **Documentation**: See `README.md` and docstrings
- **Examples**: Check the `examples/` directory
- **Issues**: Report bugs on GitHub
- **Questions**: Open a discussion on GitHub
