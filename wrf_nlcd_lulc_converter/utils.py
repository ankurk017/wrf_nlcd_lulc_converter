"""
Utility functions for WRF NLCD LULC converter.
"""

import numpy as np
import xarray as xr
import netCDF4
import shutil
import os
import subprocess
import random
import string


def generate_landusef_from_lu_index(lu_index, nclass=None, dtype=np.float32):
    """
    Generate a LANDUSEF-style array from a LU_INDEX array.

    Parameters:
        lu_index (np.ndarray): 2D array of land use class indices (ny, nx).
        nclass (int): Number of land use classes.
        dtype (np.dtype): Data type for the output array.

    Returns:
        np.ndarray: Array of shape (1, nclass, ny, nx) with one-hot encoding for each class.
    """
    # Ensure lu_index is 2D (ny, nx)
    if lu_index.ndim == 3 and lu_index.shape[0] == 1:
        lu_index = lu_index[0]
    elif lu_index.ndim > 2:
        raise ValueError(f"Unexpected lu_index shape: {lu_index.shape}")

    ny, nx = lu_index.shape
    landuse_generated = np.zeros((1, nclass, ny, nx), dtype=dtype)

    for class_idx in range(nclass):
        # Class numbers are assumed to be 1-based (i.e., class 1 is index 0)
        landuse_generated[0, class_idx, :, :] = (lu_index == (class_idx + 1)).astype(dtype)

    return landuse_generated


def crop_nlcd_with_gdalwarp(raw_NLCD_map, year, nlcd_domain, nlcd_processed_tmp_folder='~/tmp/nlcd_processed/', 
                            output_NLCD_crop_filename=None, force_recalculate=False):
    """
    Crop the NLCD GeoTIFF using gdalwarp for a given year and domain.

    Parameters:
        raw_NLCD_map (str): Path to the raw NLCD GeoTIFF file.
        year (int or str): Year of the NLCD data (used in output filename).
        nlcd_domain (dict): Dictionary with keys 'lon_min', 'lon_max', 'lat_min', 'lat_max'.
        nlcd_processed_tmp_folder (str): Temporary folder for processed files.
        output_NLCD_crop_filename (str): Output filename for cropped file.
        force_recalculate (bool): Force recalculation even if file exists.

    Returns:
        str: Path to the cropped NLCD GeoTIFF.
    """
    # Expand user in output folder path and ensure directory exists
    nlcd_processed_tmp_folder_expanded = os.path.expanduser(nlcd_processed_tmp_folder)
    os.makedirs(nlcd_processed_tmp_folder_expanded, exist_ok=True)

    if output_NLCD_crop_filename is None:
        rand_prefix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        output_NLCD_crop_filename = os.path.join(nlcd_processed_tmp_folder_expanded, f'{rand_prefix}_NLCD_{year}_crop.tif')
    else:
        output_NLCD_crop_filename = os.path.join(nlcd_processed_tmp_folder_expanded, output_NLCD_crop_filename)

    if os.path.exists(output_NLCD_crop_filename) and not force_recalculate:
        print(f"Cropped NLCD file already exists: {output_NLCD_crop_filename}. Use force_recalculate=True to overwrite.")
        return output_NLCD_crop_filename

    te_args = [
        str(nlcd_domain['lon_min']),
        str(nlcd_domain['lat_min']),
        str(nlcd_domain['lon_max']),
        str(nlcd_domain['lat_max'])
    ]

    gdalwarp_cmd = [
        "gdalwarp",
        "-t_srs", "EPSG:4326",
        "-te"
    ] + te_args + [
        "-te_srs", "EPSG:4326",
        raw_NLCD_map,
        output_NLCD_crop_filename
    ]

    print("Running gdalwarp command:", " ".join(gdalwarp_cmd))
    subprocess.run(gdalwarp_cmd, check=True)
    return output_NLCD_crop_filename


def update_lu_index_and_landusef_in_netcdf(ncfile, new_lu_index, new_landusef):
    """
    Update LU_INDEX and LANDUSEF variables in a NetCDF file.

    Parameters:
        ncfile (str): Path to the NetCDF file.
        new_lu_index (np.ndarray): New LU_INDEX data.
        new_landusef (np.ndarray): New LANDUSEF data.
    """
    with netCDF4.Dataset(ncfile, mode='r+') as ds:
        # Update LU_INDEX
        lu_index_var = ds.variables['LU_INDEX']
        if new_lu_index.shape != lu_index_var.shape:
            if lu_index_var.shape[0] == 1 and new_lu_index.ndim == 2:
                lu_index_to_write = new_lu_index[np.newaxis, :, :]
            else:
                lu_index_to_write = np.reshape(new_lu_index, lu_index_var.shape)
        else:
            lu_index_to_write = new_lu_index
        lu_index_var[:] = lu_index_to_write

        # Update LANDUSEF
        landusef_var = ds.variables['LANDUSEF']
        if new_landusef.shape != landusef_var.shape:
            if landusef_var.shape[0] == 1 and new_landusef.shape[0] == 1 and new_landusef.shape[1:] == landusef_var.shape[1:]:
                landusef_to_write = new_landusef
            else:
                landusef_to_write = np.reshape(new_landusef, landusef_var.shape)
        else:
            landusef_to_write = new_landusef
        landusef_var[:] = landusef_to_write


def extract_wrf_domain_info(wrf_file):
    """
    Extract domain information from a WRF geo_em file.

    Parameters:
        wrf_file (str): Path to the WRF geo_em file.

    Returns:
        dict: Dictionary containing domain information.
    """
    with xr.open_dataset(wrf_file) as ds:
        geog_latitudes = ds['XLAT_M'].values.squeeze()
        geog_longitudes = ds['XLONG_M'].values.squeeze()
        
        geog_latitudes_1d = geog_latitudes[:, 0]
        geog_longitudes_1d = geog_longitudes[0, :]
        
        geog01_lulc = ds['LU_INDEX'].values.squeeze()
        
        geog_roi_domain = {
            'lon_min': geog_longitudes_1d[0], 
            'lon_max': geog_longitudes_1d[-1], 
            'lat_min': geog_latitudes_1d[0], 
            'lat_max': geog_latitudes_1d[-1]
        }
        
        return {
            'latitudes': geog_latitudes_1d,
            'longitudes': geog_longitudes_1d,
            'lu_index': geog01_lulc,
            'domain': geog_roi_domain
        }


def calculate_nlcd_crop_domain(wrf_domain, margin=1.0):
    """
    Calculate the NLCD crop domain based on WRF domain with margin.

    Parameters:
        wrf_domain (dict): WRF domain dictionary.
        margin (float): Margin to add around the domain in degrees.

    Returns:
        dict: NLCD crop domain dictionary.
    """
    nlcd_crop_domain = {
        'lon_min': wrf_domain['lon_min'] - margin,
        'lon_max': wrf_domain['lon_max'] + margin,
        'lat_min': wrf_domain['lat_min'] - margin,
        'lat_max': wrf_domain['lat_max'] + margin
    }
    return nlcd_crop_domain


def validate_file_paths(*file_paths):
    """
    Validate that all file paths exist.

    Parameters:
        *file_paths: Variable number of file paths to validate.

    Raises:
        FileNotFoundError: If any file path doesn't exist.
    """
    for file_path in file_paths:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")


def create_output_directory(output_path):
    """
    Create output directory if it doesn't exist.

    Parameters:
        output_path (str): Path to the output directory or file.
    """
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
