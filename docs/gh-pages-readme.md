# Read the Docs Documentation

This directory contains the built Sphinx documentation for the WRF NLCD LULC converter package.

## Deployment

The documentation is automatically built and deployed to Read the Docs when changes are pushed to the main branch.

## Access

- **Live Site**: https://wrf-nlcd-lulc-converter.readthedocs.io/
- **Repository**: https://github.com/ankurk017/wrf_nlcd_lulc_converter

## Building Locally

To build the documentation locally:

```bash
cd docs
make html
```

The built documentation will be in `_build/html/`.

## Troubleshooting

If the site shows a 404 error:

1. Check that the repository is connected to Read the Docs
2. Ensure the .readthedocs.yml file is present and correct
3. Verify that the documentation builds successfully
4. Check the Read the Docs dashboard for build status

## Manual Deployment

If automatic deployment fails, you can manually trigger a build:

1. Go to https://readthedocs.org/dashboard/
2. Find your project (wrf-nlcd-lulc-converter)
3. Click "Build Version" 
4. Select the branch and click "Build"
