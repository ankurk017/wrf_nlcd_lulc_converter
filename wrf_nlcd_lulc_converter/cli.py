"""
Command-line interface for WRF NLCD LULC converter.
"""

import argparse
import sys
import os
from .processor import NLCDProcessor
from .mapping import LULCMapping


def main():
    """
    Main command-line interface function.
    """
    parser = argparse.ArgumentParser(
        description="Convert NLCD land use data and update WRF geo_em files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage
  wrf-nlcd-converter --nlcd-file nlcd_2017.tif --wrf-file geo_em.d02.nc --output-file geo_em_updated.nc --year 2017
  
  # With custom margin
  wrf-nlcd-converter --nlcd-file nlcd_2017.tif --wrf-file geo_em.d02.nc --output-file geo_em_updated.nc --year 2017 --margin 2.0
  
  # Force recalculation
  wrf-nlcd-converter --nlcd-file nlcd_2017.tif --wrf-file geo_em.d02.nc --output-file geo_em_updated.nc --year 2017 --force-recalculate
  
  # Urban classes only
  wrf-nlcd-converter --nlcd-file nlcd_2017.tif --wrf-file geo_em.d02.nc --output-file geo_em_urban.nc --year 2017 --urban-only
        """
    )
    
    # Required arguments
    parser.add_argument(
        "--nlcd-file",
        required=True,
        help="Path to the NLCD GeoTIFF file"
    )
    
    parser.add_argument(
        "--wrf-file",
        required=True,
        help="Path to the WRF geo_em file"
    )
    
    parser.add_argument(
        "--output-file",
        required=True,
        help="Path for the output updated WRF file"
    )
    
    parser.add_argument(
        "--year",
        required=True,
        help="Year of the NLCD data"
    )
    
    # Optional arguments
    parser.add_argument(
        "--margin",
        type=float,
        default=1.0,
        help="Margin to add around the WRF domain in degrees (default: 1.0)"
    )
    
    parser.add_argument(
        "--force-recalculate",
        action="store_true",
        help="Force recalculation even if files exist"
    )
    
    parser.add_argument(
        "--urban-only",
        action="store_true",
        help="Process only urban classes from NLCD data"
    )
    
    parser.add_argument(
        "--tmp-folder",
        default="~/tmp/nlcd_processed/",
        help="Temporary folder for processed files (default: ~/tmp/nlcd_processed/)"
    )
    
    parser.add_argument(
        "--custom-mapping",
        help="Custom NLCD to WRF mapping as JSON string (e.g., '{\"21\": 23, \"22\": 24}')"
    )
    
    parser.add_argument(
        "--info",
        action="store_true",
        help="Show processor information and exit"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    # Show processor information if requested
    if args.info:
        processor = NLCDProcessor()
        info = processor.get_processing_info()
        print("Processor Information:")
        print(f"  Total LULC classes: {info['total_classes']}")
        print(f"  Urban classes: {info['urban_classes']}")
        print(f"  NLCD to WRF mapping: {info['lulc_mapping']}")
        return
    
    # Validate input files
    if not os.path.exists(args.nlcd_file):
        print(f"Error: NLCD file not found: {args.nlcd_file}")
        sys.exit(1)
    
    if not os.path.exists(args.wrf_file):
        print(f"Error: WRF file not found: {args.wrf_file}")
        sys.exit(1)
    
    # Initialize processor
    processor = NLCDProcessor()
    
    # Set custom mapping if provided
    if args.custom_mapping:
        try:
            import json
            custom_mapping = json.loads(args.custom_mapping)
            processor.set_custom_mapping(custom_mapping)
        except json.JSONDecodeError:
            print("Error: Invalid JSON format for custom mapping")
            sys.exit(1)
    
    try:
        # Process the data
        if args.urban_only:
            output_file = processor.process_urban_only(
                nlcd_file=args.nlcd_file,
                wrf_file=args.wrf_file,
                output_file=args.output_file,
                year=args.year,
                margin=args.margin,
                force_recalculate=args.force_recalculate,
                tmp_folder=args.tmp_folder
            )
        else:
            output_file = processor.process_nlcd_and_update_wrf(
                nlcd_file=args.nlcd_file,
                wrf_file=args.wrf_file,
                output_file=args.output_file,
                year=args.year,
                margin=args.margin,
                force_recalculate=args.force_recalculate,
                tmp_folder=args.tmp_folder
            )
        
        print(f"\nSuccess! Updated WRF file created: {output_file}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
