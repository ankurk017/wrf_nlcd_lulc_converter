#!/usr/bin/env python3
"""
Basic example of using the WRF NLCD LULC converter.

This example demonstrates the basic usage of the package to process NLCD data
and update a WRF geo_em file.
"""

import os
import sys

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from wrf_nlcd_lulc_converter import NLCDProcessor


def main():
    """
    Basic example of NLCD to WRF conversion.
    """
    print("WRF NLCD LULC Converter - Basic Example")
    print("=" * 50)
    
    # Initialize the processor
    processor = NLCDProcessor()
    
    # Example file paths (you'll need to update these with your actual paths)
    nlcd_file = "path/to/your/nlcd_2017.tif"
    wrf_file = "path/to/your/geo_em.d02.nc"
    output_file = "path/to/output/geo_em_updated_2017.nc"
    year = "2017"
    
    # Check if files exist (optional - for demonstration)
    if not os.path.exists(nlcd_file):
        print(f"Warning: NLCD file not found: {nlcd_file}")
        print("Please update the nlcd_file path in this script.")
        return
    
    if not os.path.exists(wrf_file):
        print(f"Warning: WRF file not found: {wrf_file}")
        print("Please update the wrf_file path in this script.")
        return
    
    try:
        # Process NLCD data and update WRF file
        print(f"Processing NLCD file: {nlcd_file}")
        print(f"WRF file: {wrf_file}")
        print(f"Output file: {output_file}")
        print(f"Year: {year}")
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Process the data
        updated_file = processor.process_nlcd_and_update_wrf(
            nlcd_file=nlcd_file,
            wrf_file=wrf_file,
            output_file=output_file,
            year=year,
            margin=1.0,  # 1 degree margin around the domain
            force_recalculate=False,  # Set to True to force recalculation
            tmp_folder="~/tmp/nlcd_processed/"
        )
        
        print(f"\nSuccess! Updated WRF file created: {updated_file}")
        
        # Show processor information
        info = processor.get_processing_info()
        print(f"\nProcessor Information:")
        print(f"  Total LULC classes: {info['total_classes']}")
        print(f"  Urban classes: {info['urban_classes']}")
        print(f"  NLCD to WRF mapping: {info['lulc_mapping']}")
        
    except Exception as e:
        print(f"Error during processing: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
