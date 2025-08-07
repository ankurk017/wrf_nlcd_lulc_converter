#!/usr/bin/env python3
"""
Urban-only processing example for the WRF NLCD LULC converter.

This example demonstrates how to process only urban classes from NLCD data,
which can be useful for focused urban studies or when you only want to
update urban areas in your WRF domain.
"""

import os
import sys

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from wrf_nlcd_lulc_converter import NLCDProcessor


def main():
    """
    Example of processing only urban classes from NLCD data.
    """
    print("WRF NLCD LULC Converter - Urban-Only Processing Example")
    print("=" * 65)
    
    # Initialize the processor
    processor = NLCDProcessor()
    
    # Example file paths (you'll need to update these with your actual paths)
    nlcd_file = "path/to/your/nlcd_2017.tif"
    wrf_file = "path/to/your/geo_em.d02.nc"
    output_file = "path/to/output/geo_em_urban_only_2017.nc"
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
        # Show urban classes that will be processed
        urban_classes = processor.lulc_mapping.get_urban_classes()
        print("Urban classes that will be processed:")
        for class_num in urban_classes:
            info = processor.lulc_mapping.get_class_info(class_num)
            print(f"  Class {class_num}: {info['label']}")
        
        print(f"\nProcessing urban classes only...")
        print(f"NLCD file: {nlcd_file}")
        print(f"WRF file: {wrf_file}")
        print(f"Output file: {output_file}")
        print(f"Year: {year}")
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Process only urban classes
        updated_file = processor.process_urban_only(
            nlcd_file=nlcd_file,
            wrf_file=wrf_file,
            output_file=output_file,
            year=year,
            margin=1.0,
            force_recalculate=False,
            tmp_folder="~/tmp/nlcd_processed/"
        )
        
        print(f"\nSuccess! Updated WRF file with urban data created: {updated_file}")
        
        # Show processor information
        info = processor.get_processing_info()
        print(f"\nProcessor Information:")
        print(f"  Total LULC classes: {info['total_classes']}")
        print(f"  Urban classes processed: {info['urban_classes']}")
        print(f"  NLCD to WRF mapping: {info['lulc_mapping']}")
        
    except Exception as e:
        print(f"Error during processing: {str(e)}")
        import traceback
        traceback.print_exc()


def compare_processing_methods():
    """
    Compare full processing vs urban-only processing.
    """
    print("\n" + "=" * 65)
    print("Comparing Processing Methods")
    print("=" * 65)
    
    processor = NLCDProcessor()
    
    # Example file paths (you'll need to update these with your actual paths)
    nlcd_file = "path/to/your/nlcd_2017.tif"
    wrf_file = "path/to/your/geo_em.d02.nc"
    
    if not os.path.exists(nlcd_file) or not os.path.exists(wrf_file):
        print("Skipping comparison - files not found")
        return
    
    try:
        print("Method 1: Full NLCD processing")
        print("  - Processes all NLCD classes")
        print("  - Updates all land use types in WRF domain")
        print("  - More comprehensive but takes longer")
        
        print("\nMethod 2: Urban-only processing")
        print("  - Processes only urban classes (21-24)")
        print("  - Only updates urban areas in WRF domain")
        print("  - Faster and focused on urban areas")
        
        print("\nUrban classes (21-24):")
        urban_classes = processor.lulc_mapping.get_urban_classes()
        for class_num in urban_classes:
            info = processor.lulc_mapping.get_class_info(class_num)
            print(f"  - Class {class_num}: {info['label']}")
        
        print("\nUse urban-only processing when:")
        print("  - You only need to update urban areas")
        print("  - You want faster processing")
        print("  - You're doing urban-focused research")
        print("  - You want to preserve existing non-urban land use")
        
        print("\nUse full processing when:")
        print("  - You need comprehensive land use updates")
        print("  - You're updating all land use types")
        print("  - You have time for complete processing")
        
    except Exception as e:
        print(f"Error during comparison: {str(e)}")


if __name__ == "__main__":
    main()
    compare_processing_methods()
