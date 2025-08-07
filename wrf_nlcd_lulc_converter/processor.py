"""
Main processor for NLCD to WRF conversion.
"""

import numpy as np
import xarray as xr
import rasterio
import os
import shutil
from .mapping import LULCMapping
from .utils import (
    generate_landusef_from_lu_index,
    crop_nlcd_with_gdalwarp,
    update_lu_index_and_landusef_in_netcdf,
    extract_wrf_domain_info,
    calculate_nlcd_crop_domain,
    validate_file_paths,
    create_output_directory
)


class NLCDProcessor:
    """
    Main class for processing NLCD data and updating WRF files.
    """
    
    def __init__(self, lulc_mapping=None):
        """
        Initialize the NLCD processor.
        
        Parameters:
            lulc_mapping (LULCMapping, optional): Custom LULC mapping object.
        """
        self.lulc_mapping = lulc_mapping if lulc_mapping is not None else LULCMapping()
    
    def process_nlcd_and_update_wrf(self, nlcd_file, wrf_file, output_file, year, 
                                   margin=1.0, force_recalculate=False, tmp_folder='~/tmp/nlcd_processed/'):
        """
        Main method to process NLCD data and update WRF file.
        
        Parameters:
            nlcd_file (str): Path to the NLCD GeoTIFF file.
            wrf_file (str): Path to the WRF geo_em file.
            output_file (str): Path for the output updated WRF file.
            year (str or int): Year of the NLCD data.
            margin (float): Margin to add around the WRF domain in degrees.
            force_recalculate (bool): Force recalculation even if files exist.
            tmp_folder (str): Temporary folder for processed files.
            
        Returns:
            str: Path to the updated WRF file.
        """
        print(f"Processing NLCD file: {nlcd_file}")
        print(f"WRF file: {wrf_file}")
        print(f"Output file: {output_file}")
        print(f"Year: {year}")
        
        # Validate input files
        validate_file_paths(nlcd_file, wrf_file)
        
        # Create output directory if needed
        create_output_directory(output_file)
        
        # Extract WRF domain information
        print("Extracting WRF domain information...")
        wrf_info = extract_wrf_domain_info(wrf_file)
        geog_latitudes_1d = wrf_info['latitudes']
        geog_longitudes_1d = wrf_info['longitudes']
        geog01_lulc = wrf_info['lu_index']
        geog_roi_domain = wrf_info['domain']
        
        print(f"WRF domain: {geog_roi_domain}")
        
        # Calculate NLCD crop domain
        nlcd_crop_domain = calculate_nlcd_crop_domain(geog_roi_domain, margin)
        print(f"NLCD crop domain: {nlcd_crop_domain}")
        
        # Crop NLCD file
        print("Cropping NLCD file...")
        cropped_nlcd_file = crop_nlcd_with_gdalwarp(
            nlcd_file, year, nlcd_crop_domain, 
            nlcd_processed_tmp_folder=tmp_folder,
            output_NLCD_crop_filename=f'NLCD_{year}_crop.tif',
            force_recalculate=force_recalculate
        )
        
        # Read cropped NLCD data
        print("Reading cropped NLCD data...")
        with rasterio.open(cropped_nlcd_file) as src:
            lulc_data = src.read(1)
        
        # Get domain bounds
        lon_min, lon_max, lat_min, lat_max = (
            nlcd_crop_domain['lon_min'], nlcd_crop_domain['lon_max'],
            nlcd_crop_domain['lat_min'], nlcd_crop_domain['lat_max']
        )
        
        # Create coordinate arrays
        nlcd_longitudes = np.linspace(lon_min, lon_max, lulc_data.shape[1])
        nlcd_latitudes = np.linspace(lat_min, lat_max, lulc_data.shape[0])
        
        # Create xarray DataArray for interpolation
        nlcd_lulc_da = xr.DataArray(
            np.flipud(lulc_data),
            dims=("lat", "lon"),
            coords={"lat": nlcd_latitudes, "lon": nlcd_longitudes},
            name=f"LULC_{year}"
        )
        
        # Interpolate to WRF grid
        print("Interpolating NLCD data to WRF grid...")
        nlcd_lulc_interp = nlcd_lulc_da.interp(
            lat=geog_latitudes_1d, 
            lon=geog_longitudes_1d, 
            method='nearest'
        )
        
        # Get NLCD to WRF mapping
        nlcd_to_geog_urban = self.lulc_mapping.get_nlcd_to_geog_mapping()
        
        # Create updated LU_INDEX array
        print("Updating LU_INDEX with NLCD data...")
        geog01_lulc_updated = np.copy(geog01_lulc)
        
        for nlcd_val, geog_val in nlcd_to_geog_urban.items():
            mask = nlcd_lulc_interp == nlcd_val
            geog01_lulc_updated[mask] = geog_val
        
        # Generate LANDUSEF array
        print("Generating LANDUSEF array...")
        landuse_updated = generate_landusef_from_lu_index(
            geog01_lulc_updated, nclass=40, dtype=np.float32
        )
        
        # Create output file
        print("Creating output WRF file...")
        shutil.copy(wrf_file, output_file)
        
        # Update the file with new data
        update_lu_index_and_landusef_in_netcdf(
            output_file, geog01_lulc_updated, landuse_updated
        )
        
        print(f"Successfully created updated WRF file: {output_file}")
        return output_file
    
    def process_urban_only(self, nlcd_file, wrf_file, output_file, year, 
                          margin=1.0, force_recalculate=False, tmp_folder='~/tmp/nlcd_processed/'):
        """
        Process only urban classes from NLCD data.
        
        Parameters:
            nlcd_file (str): Path to the NLCD GeoTIFF file.
            wrf_file (str): Path to the WRF geo_em file.
            output_file (str): Path for the output updated WRF file.
            year (str or int): Year of the NLCD data.
            margin (float): Margin to add around the WRF domain in degrees.
            force_recalculate (bool): Force recalculation even if files exist.
            tmp_folder (str): Temporary folder for processed files.
            
        Returns:
            str: Path to the updated WRF file.
        """
        print(f"Processing urban classes from NLCD file: {nlcd_file}")
        
        # Validate input files
        validate_file_paths(nlcd_file, wrf_file)
        
        # Create output directory if needed
        create_output_directory(output_file)
        
        # Extract WRF domain information
        print("Extracting WRF domain information...")
        wrf_info = extract_wrf_domain_info(wrf_file)
        geog_latitudes_1d = wrf_info['latitudes']
        geog_longitudes_1d = wrf_info['longitudes']
        geog01_lulc = wrf_info['lu_index']
        geog_roi_domain = wrf_info['domain']
        
        # Calculate NLCD crop domain
        nlcd_crop_domain = calculate_nlcd_crop_domain(geog_roi_domain, margin)
        
        # Crop NLCD file
        print("Cropping NLCD file...")
        cropped_nlcd_file = crop_nlcd_with_gdalwarp(
            nlcd_file, year, nlcd_crop_domain, 
            nlcd_processed_tmp_folder=tmp_folder,
            output_NLCD_crop_filename=f'NLCD_{year}_urban_crop.tif',
            force_recalculate=force_recalculate
        )
        
        # Read cropped NLCD data
        print("Reading cropped NLCD data...")
        with rasterio.open(cropped_nlcd_file) as src:
            lulc_data = src.read(1)
        
        # Get urban classes
        urban_classes = self.lulc_mapping.get_urban_classes()
        
        # Filter for urban classes only
        lulc_urban = np.where(
            (lulc_data >= 21) & (lulc_data <= 24), 
            lulc_data, 
            np.nan
        )
        
        # Get domain bounds
        lon_min, lon_max, lat_min, lat_max = (
            nlcd_crop_domain['lon_min'], nlcd_crop_domain['lon_max'],
            nlcd_crop_domain['lat_min'], nlcd_crop_domain['lat_max']
        )
        
        # Create coordinate arrays
        nlcd_longitudes = np.linspace(lon_min, lon_max, lulc_urban.shape[1])
        nlcd_latitudes = np.linspace(lat_min, lat_max, lulc_urban.shape[0])
        
        # Create xarray DataArray for interpolation
        nlcd_lulc_da = xr.DataArray(
            np.flipud(lulc_urban),
            dims=("lat", "lon"),
            coords={"lat": nlcd_latitudes, "lon": nlcd_longitudes},
            name=f"Urban_LULC_{year}"
        )
        
        # Interpolate to WRF grid
        print("Interpolating urban NLCD data to WRF grid...")
        nlcd_lulc_interp = nlcd_lulc_da.interp(
            lat=geog_latitudes_1d, 
            lon=geog_longitudes_1d, 
            method='nearest'
        )
        
        # Get NLCD to WRF mapping
        nlcd_to_geog_urban = self.lulc_mapping.get_nlcd_to_geog_mapping()
        
        # Create updated LU_INDEX array
        print("Updating LU_INDEX with urban NLCD data...")
        geog01_lulc_updated = np.copy(geog01_lulc)
        
        for nlcd_val, geog_val in nlcd_to_geog_urban.items():
            mask = nlcd_lulc_interp == nlcd_val
            geog01_lulc_updated[mask] = geog_val
        
        # Generate LANDUSEF array
        print("Generating LANDUSEF array...")
        landuse_updated = generate_landusef_from_lu_index(
            geog01_lulc_updated, nclass=40, dtype=np.float32
        )
        
        # Create output file
        print("Creating output WRF file...")
        shutil.copy(wrf_file, output_file)
        
        # Update the file with new data
        update_lu_index_and_landusef_in_netcdf(
            output_file, geog01_lulc_updated, landuse_updated
        )
        
        print(f"Successfully created updated WRF file with urban data: {output_file}")
        return output_file
    
    def set_custom_mapping(self, mapping_dict):
        """
        Set a custom NLCD to WRF/GEOG mapping.
        
        Parameters:
            mapping_dict (dict): Custom mapping dictionary.
        """
        self.lulc_mapping.set_custom_mapping(mapping_dict)
        print(f"Updated NLCD to WRF mapping: {mapping_dict}")
    
    def get_processing_info(self):
        """
        Get information about the current processor configuration.
        
        Returns:
            dict: Dictionary with processor information.
        """
        return {
            'lulc_mapping': self.lulc_mapping.get_nlcd_to_geog_mapping(),
            'urban_classes': self.lulc_mapping.get_urban_classes(),
            'total_classes': len(self.lulc_mapping.lulc_dict)
        }
