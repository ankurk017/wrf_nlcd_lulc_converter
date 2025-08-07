#!/usr/bin/env python3
"""
Complete workflow example for the WRF NLCD LULC converter.

This example demonstrates the complete workflow from the original notebook,
including file path setup, domain extraction, NLCD cropping, interpolation,
and WRF file updating.
"""

import os
import sys
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from wrf_nlcd_lulc_converter import NLCDProcessor, LULCMapping
from wrf_nlcd_lulc_converter.utils import extract_wrf_domain_info, calculate_nlcd_crop_domain
from wrf_nlcd_lulc_converter.plotting import plot_lulc_data, plot_urban_comparison, plot_domain_info


def main():
    """
    Complete workflow example replicating the notebook functionality.
    """
    print("WRF NLCD LULC Converter - Complete Workflow Example")
    print("=" * 60)
    
    # Set up file paths using actual WRF file and default NLCD folder
    nlcd_raw_map_folder = '/nas/rstor/akumar/common/NLCD_raw_maps'
    year = '2017'
    infile_geog01 = '/nas/rstor/akumar/common/sample_geog/geo_em.d02.nc'
    
    # Construct NLCD file path (Matrix users can use the default folder)
    raw_NLCD_map = f'{nlcd_raw_map_folder}/Annual_NLCD_LndCov_{year}_CU_C1V1.tif'
    
    # Check if files exist
    if not os.path.exists(raw_NLCD_map):
        print(f"Warning: NLCD file not found: {raw_NLCD_map}")
        print("Please update the nlcd_raw_map_folder path in this script.")
        print("Download NLCD data from: https://www.mrlc.gov/data")
        return
    
    if not os.path.exists(infile_geog01):
        print(f"Warning: WRF file not found: {infile_geog01}")
        print("Please update the infile_geog01 path in this script.")
        return
    
    try:
        # Step 1: Extract WRF domain information
        print("Step 1: Extracting WRF domain information...")
        wrf_info = extract_wrf_domain_info(infile_geog01)
        
        geog_latitudes_1d = wrf_info['latitudes']
        geog_longitudes_1d = wrf_info['longitudes']
        geog01_lulc = wrf_info['lu_index']
        geog_roi_domain = wrf_info['domain']
        
        print(f"WRF domain: {geog_roi_domain}")
        
        # Step 2: Calculate NLCD crop domain with margin
        print("\nStep 2: Calculating NLCD crop domain...")
        margin = 1.0
        nlcd_crop_domain = calculate_nlcd_crop_domain(geog_roi_domain, margin)
        print(f"NLCD crop domain: {nlcd_crop_domain}")
        
        # Step 3: Initialize processor
        print("\nStep 3: Initializing processor...")
        processor = NLCDProcessor()
        
        # Step 4: Process NLCD data and update WRF file
        print("\nStep 4: Processing NLCD data and updating WRF file...")
        outfile_geog01_2017 = infile_geog01.replace('.nc', '_2017.nc')
        
        updated_file = processor.process_nlcd_and_update_wrf(
            nlcd_file=raw_NLCD_map,
            wrf_file=infile_geog01,
            output_file=outfile_geog01_2017,
            year=year,
            margin=margin,
            force_recalculate=False,
            tmp_folder='~/tmp/nlcd_processed/'
        )
        
        print(f"\nSuccess! Created new geo_em file: {updated_file}")
        
        # Step 5: Verify the results
        print("\nStep 5: Verifying results...")
        verify_results(updated_file, geog01_lulc)
        
        # Step 6: Create visualizations
        print("\nStep 6: Creating visualizations...")
        create_visualizations(geog01_lulc, geog_latitudes_1d, geog_longitudes_1d, 
                            geog_roi_domain, updated_file)
        
        # Step 7: Show processor information
        print("\nStep 7: Processor information:")
        info = processor.get_processing_info()
        print(f"  Total LULC classes: {info['total_classes']}")
        print(f"  Urban classes: {info['urban_classes']}")
        print(f"  NLCD to WRF mapping: {info['lulc_mapping']}")
        
    except Exception as e:
        print(f"Error during processing: {str(e)}")
        import traceback
        traceback.print_exc()


def verify_results(updated_file, original_lu_index):
    """
    Verify the results by comparing original and updated LU_INDEX.
    
    Parameters:
        updated_file (str): Path to the updated WRF file.
        original_lu_index (np.ndarray): Original LU_INDEX array.
    """
    try:
        # Read the updated file
        with xr.open_dataset(updated_file) as ds:
            updated_lu_index = ds['LU_INDEX'].values.squeeze()
        
        # Calculate statistics
        original_unique = np.unique(original_lu_index)
        updated_unique = np.unique(updated_lu_index)
        
        print(f"Original LU_INDEX unique values: {original_unique}")
        print(f"Updated LU_INDEX unique values: {updated_unique}")
        
        # Check for urban classes in updated data
        urban_classes = [21, 22, 23, 24]
        urban_pixels_original = np.sum(np.isin(original_lu_index, urban_classes))
        urban_pixels_updated = np.sum(np.isin(updated_lu_index, urban_classes))
        
        print(f"Urban pixels in original: {urban_pixels_original}")
        print(f"Urban pixels in updated: {urban_pixels_updated}")
        
        if urban_pixels_updated > urban_pixels_original:
            print("✓ Urban areas have been updated successfully!")
        else:
            print("⚠ No urban areas were updated (this might be expected if no urban areas in domain)")
            
    except Exception as e:
        print(f"Error during verification: {str(e)}")


def create_visualizations(original_lu_index, latitudes, longitudes, domain, updated_file):
    """
    Create visualizations of the LULC data and processing results.
    
    Parameters:
        original_lu_index (np.ndarray): Original LU_INDEX array
        latitudes (np.ndarray): Latitude coordinates
        longitudes (np.ndarray): Longitude coordinates
        domain (dict): Domain information
        updated_file (str): Path to updated WRF file
    """
    try:
        # Create plots directory
        os.makedirs("plots", exist_ok=True)
        
        # Plot 1: Original LULC data
        print("  Creating original LULC plot...")
        extent = [domain['lon_min'], domain['lon_max'], 
                 domain['lat_min'], domain['lat_max']]
        
        plot_lulc_data(longitudes, latitudes, original_lu_index,
                      title="Original WRF LULC Data",
                      extent=extent,
                      save_path="plots/original_lulc.png", show_plot=False)
        
        # Plot 2: Updated LULC data (if file exists)
        if os.path.exists(updated_file):
            print("  Creating updated LULC plot...")
            with xr.open_dataset(updated_file) as ds:
                updated_lu_index = ds['LU_INDEX'].values.squeeze()
            
            plot_lulc_data(longitudes, latitudes, updated_lu_index,
                          title="Updated WRF LULC Data",
                          extent=extent,
                          save_path="plots/updated_lulc.png", show_plot=False)
            
            # Plot 3: Urban comparison
            print("  Creating urban comparison plot...")
            plot_urban_comparison(original_lu_index, updated_lu_index, 
                                longitudes, latitudes,
                                title="Urban Area Comparison (Original vs Updated)",
                                save_path="plots/urban_comparison.png", dpi=150)
        
        print("  All plots saved in 'plots/' directory")
        
    except Exception as e:
        print(f"  Error creating visualizations: {str(e)}")


def demonstrate_visualization():
    """
    Demonstrate how to visualize the LULC data.
    """
    print("\n" + "=" * 60)
    print("Visualization Demonstration")
    print("=" * 60)
    
    # Create a sample LULC array for demonstration
    sample_lulc = np.random.randint(1, 41, size=(100, 100))
    
    # Get the LULC mapping for colors
    mapping = LULCMapping()
    
    # Create a figure
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Plot 1: Sample LULC data
    im1 = ax1.imshow(sample_lulc, cmap=mapping.cmap_40, vmin=1, vmax=40)
    ax1.set_title("Sample LULC Data")
    ax1.set_xlabel("Longitude")
    ax1.set_ylabel("Latitude")
    
    # Plot 2: Urban classes only
    urban_mask = np.isin(sample_lulc, mapping.get_urban_classes())
    urban_lulc = np.where(urban_mask, sample_lulc, np.nan)
    
    im2 = ax2.imshow(urban_lulc, cmap=mapping.cmap_40, vmin=1, vmax=40)
    ax2.set_title("Urban Classes Only")
    ax2.set_xlabel("Longitude")
    ax2.set_ylabel("Latitude")
    
    # Add colorbar
    cbar = plt.colorbar(im1, ax=[ax1, ax2], shrink=0.8)
    cbar.set_label("LULC Class")
    
    plt.tight_layout()
    plt.savefig("lulc_visualization_demo.png", dpi=150, bbox_inches='tight')
    print("Saved visualization demo to: lulc_visualization_demo.png")
    
    # Show some class information
    print("\nLULC Class Information:")
    for class_num in [21, 22, 23, 24]:
        info = mapping.get_class_info(class_num)
        print(f"  Class {class_num}: {info['label']} (Color: {info['color']})")


if __name__ == "__main__":
    main()
    demonstrate_visualization()
