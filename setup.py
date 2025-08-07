from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="wrf-nlcd-lulc-converter",
    version="0.1.0",
    author="Ankur Kumar",
    author_email="ankur.kumar@example.com",
    description="A Python package for converting NLCD land use data and updating WRF geo_em files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ankurk017/wrf-nlcd-lulc-converter",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Atmospheric Science",
    ],
    python_requires=">=3.8",
    install_requires=[
        "xarray>=2023.1.0",
        "numpy>=1.21.0",
        "matplotlib>=3.5.0",
        "cartopy>=0.20.0",
        "rasterio>=1.3.0",
        "netCDF4>=1.6.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=3.0",
            "black>=22.0",
            "flake8>=4.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "wrf-nlcd-converter=wrf_nlcd_lulc_converter.cli:main",
        ],
    },
)
