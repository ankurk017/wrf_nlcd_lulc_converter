#!/usr/bin/env python3
"""
Test script to verify the WRF NLCD LULC converter package installation.
"""

import sys
import os

def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")
    
    try:
        import numpy as np
        print("✓ numpy imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import numpy: {e}")
        return False
    
    try:
        import xarray as xr
        print("✓ xarray imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import xarray: {e}")
        return False
    
    try:
        import rasterio
        print("✓ rasterio imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import rasterio: {e}")
        return False
    
    try:
        import netCDF4
        print("✓ netCDF4 imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import netCDF4: {e}")
        return False
    
    try:
        import matplotlib
        print("✓ matplotlib imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import matplotlib: {e}")
        return False
    
    try:
        import cartopy
        print("✓ cartopy imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import cartopy: {e}")
        return False
    
    return True


def test_package_imports():
    """Test that the package modules can be imported."""
    print("\nTesting package imports...")
    
    try:
        from wrf_nlcd_lulc_converter import NLCDProcessor, LULCMapping
        print("✓ Main package classes imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import main package classes: {e}")
        return False
    
    try:
        from wrf_nlcd_lulc_converter.utils import generate_landusef_from_lu_index
        print("✓ Utility functions imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import utility functions: {e}")
        return False
    
    try:
        from wrf_nlcd_lulc_converter.mapping import lulc_mapping
        print("✓ LULC mapping imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import LULC mapping: {e}")
        return False
    
    return True


def test_basic_functionality():
    """Test basic package functionality."""
    print("\nTesting basic functionality...")
    
    try:
        from wrf_nlcd_lulc_converter import NLCDProcessor, LULCMapping
        import numpy as np
        
        # Test LULCMapping
        mapping = LULCMapping()
        info = mapping.get_class_info(21)
        assert info['label'] == "Open Water"
        print("✓ LULCMapping functionality works")
        
        # Test NLCDProcessor
        processor = NLCDProcessor()
        processing_info = processor.get_processing_info()
        assert 'total_classes' in processing_info
        assert 'urban_classes' in processing_info
        print("✓ NLCDProcessor functionality works")
        
        # Test utility function
        lu_index = np.array([[1, 2], [3, 4]])
        landusef = generate_landusef_from_lu_index(lu_index, nclass=4)
        assert landusef.shape == (1, 4, 2, 2)
        print("✓ Utility functions work")
        
        return True
        
    except Exception as e:
        print(f"✗ Basic functionality test failed: {e}")
        return False


def test_cli_availability():
    """Test that the CLI is available."""
    print("\nTesting CLI availability...")
    
    try:
        import subprocess
        result = subprocess.run(['wrf-nlcd-converter', '--info'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✓ CLI command works")
            return True
        else:
            print(f"✗ CLI command failed: {result.stderr}")
            return False
    except FileNotFoundError:
        print("✗ CLI command not found (package may not be installed)")
        return False
    except Exception as e:
        print(f"✗ CLI test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("WRF NLCD LULC Converter - Installation Test")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_package_imports,
        test_basic_functionality,
        test_cli_availability
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! The package is installed correctly.")
        return 0
    else:
        print("❌ Some tests failed. Please check the installation.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
