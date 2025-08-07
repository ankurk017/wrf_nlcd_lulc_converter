# GitHub Pages Documentation

This directory contains the built Sphinx documentation for the WRF NLCD LULC converter package.

## Deployment

The documentation is automatically built and deployed to GitHub Pages via GitHub Actions when changes are pushed to the main branch.

## Access

- **Live Site**: https://ankurk017.github.io/wrf_nlcd_lulc_converter/
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

1. Check that GitHub Pages is enabled in the repository settings
2. Ensure the gh-pages branch exists and contains the built documentation
3. Verify that the GitHub Actions workflow completed successfully
4. Check the repository settings for the correct source branch (gh-pages)

## Manual Deployment

If automatic deployment fails, you can manually trigger the workflow:

1. Go to the Actions tab in the repository
2. Select "Build and Deploy Documentation"
3. Click "Run workflow"
4. Select the branch and click "Run workflow"
