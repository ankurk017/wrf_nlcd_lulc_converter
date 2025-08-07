#!/usr/bin/env python3
"""
Custom mapping example for the WRF NLCD LULC converter.

This example demonstrates how to use custom NLCD to WRF/GEOG class mappings.
"""

import os
import sys

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from wrf_nlcd_lulc_converter import NLCDProcessor, LULCMapping


def main():
    """
    Example with custom LULC mapping.
    """
    print("WRF NLCD LULC Converter - Custom Mapping Example")
    print("=" * 60)
    
    # Create a custom LULC mapping
    custom_mapping = LULCMapping()
    
    # Define a custom NLCD to WRF/GEOG mapping
    # This example maps NLCD urban classes to different WRF classes
    custom_nlcd_to_wrf_mapping = {
        21: 23,  # NLCD Open Water -> WRF Developed Open Space
        22: 24,  # NLCD Perennial Ice/Snow -> WRF Developed Low Intensity
        23: 25,  # NLCD Developed Open Space -> WRF Developed Medium Intensity
        24: 26,  # NLCD Developed Low Intensity -> WRF Developed High Intensity
        11: 39,  # NLCD Permanent Wetlands -> WRF Woody Wetlands
        12: 38,  # NLCD Croplands -> WRF Cultivated Crops
    }
    
    # Set the custom mapping
    custom_mapping.set_custom_mapping(custom_nlcd_to_wrf_mapping)
    
    # Initialize processor with custom mapping
    processor = NLCDProcessor(lulc_mapping=custom_mapping)
    
    # Example file paths (you'll need to update these with your actual paths)
    nlcd_file = "path/to/your/nlcd_2017.tif"
    wrf_file = "path/to/your/geo_em.d02.nc"
    output_file = "path/to/output/geo_em_custom_mapping_2017.nc"
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
        # Show the custom mapping
        print("Custom NLCD to WRF Mapping:")
        mapping = processor.lulc_mapping.get_nlcd_to_geog_mapping()
        for nlcd_class, wrf_class in mapping.items():
            nlcd_info = processor.lulc_mapping.get_class_info(nlcd_class)
            wrf_info = processor.lulc_mapping.get_class_info(wrf_class)
            print(f"  NLCD {nlcd_class} ({nlcd_info['label']}) -> WRF {wrf_class} ({wrf_info['label']})")
        
        print(f"\nProcessing with custom mapping...")
        print(f"NLCD file: {nlcd_file}")
        print(f"WRF file: {wrf_file}")
        print(f"Output file: {output_file}")
        print(f"Year: {year}")
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Process the data with custom mapping
        updated_file = processor.process_nlcd_and_update_wrf(
            nlcd_file=nlcd_file,
            wrf_file=wrf_file,
            output_file=output_file,
            year=year,
            margin=1.5,  # Larger margin for this example
            force_recalculate=True,  # Force recalculation
            tmp_folder="~/tmp/nlcd_processed/"
        )
        
        print(f"\nSuccess! Updated WRF file created: {updated_file}")
        
        # Show processor information
        info = processor.get_processing_info()
        print(f"\nProcessor Information:")
        print(f"  Total LULC classes: {info['total_classes']}")
        print(f"  Urban classes: {info['urban_classes']}")
        print(f"  Custom NLCD to WRF mapping: {info['lulc_mapping']}")
        
    except Exception as e:
        print(f"Error during processing: {str(e)}")
        import traceback
        traceback.print_exc()


def demonstrate_mapping_methods():
    """
    Demonstrate various mapping methods.
    """
    print("\n" + "=" * 60)
    print("Demonstrating LULC Mapping Methods")
    print("=" * 60)
    
    # Create a mapping object
    mapping = LULCMapping()
    
    # Get information about specific classes
    print("Class Information Examples:")
    for class_num in [21, 23, 24, 26]:
        info = mapping.get_class_info(class_num)
        print(f"  Class {class_num}: {info['label']} (Color: {info['color']})")
    
    # Get urban classes
    urban_classes = mapping.get_urban_classes()
    print(f"\nUrban Classes: {urban_classes}")
    
    # Get current mapping
    current_mapping = mapping.get_nlcd_to_geog_mapping()
    print(f"\nCurrent NLCD to WRF Mapping: {current_mapping}")
    
    # Demonstrate setting custom mapping
    custom_mapping = {21: 30, 22: 31, 23: 32, 24: 33}
    mapping.set_custom_mapping(custom_mapping)
    print(f"Updated Mapping: {mapping.get_nlcd_to_geog_mapping()}")


if __name__ == "__main__":
    main()
    demonstrate_mapping_methods()
