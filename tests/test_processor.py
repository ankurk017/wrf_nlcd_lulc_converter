"""
Tests for the WRF NLCD LULC converter processor.
"""

import unittest
import numpy as np
import tempfile
import os
import sys

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from wrf_nlcd_lulc_converter import NLCDProcessor, LULCMapping
from wrf_nlcd_lulc_converter.utils import generate_landusef_from_lu_index


class TestLULCMapping(unittest.TestCase):
    """Test the LULCMapping class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mapping = LULCMapping()
    
    def test_class_info(self):
        """Test getting class information."""
        info = self.mapping.get_class_info(21)
        self.assertEqual(info['label'], "Open Water")
        self.assertEqual(info['color'], "#1c0dff")
    
    def test_urban_classes(self):
        """Test getting urban classes."""
        urban_classes = self.mapping.get_urban_classes()
        self.assertEqual(urban_classes, [21, 22, 23, 24])
    
    def test_custom_mapping(self):
        """Test setting custom mapping."""
        custom_mapping = {21: 30, 22: 31}
        self.mapping.set_custom_mapping(custom_mapping)
        retrieved_mapping = self.mapping.get_nlcd_to_geog_mapping()
        self.assertEqual(retrieved_mapping, custom_mapping)


class TestUtils(unittest.TestCase):
    """Test utility functions."""
    
    def test_generate_landusef_from_lu_index(self):
        """Test generating LANDUSEF from LU_INDEX."""
        # Create a simple test array
        lu_index = np.array([[1, 2, 3], [4, 5, 6]])
        
        # Generate LANDUSEF
        landusef = generate_landusef_from_lu_index(lu_index, nclass=6)
        
        # Check shape
        self.assertEqual(landusef.shape, (1, 6, 2, 3))
        
        # Check that the correct classes are set to 1
        self.assertEqual(landusef[0, 0, 0, 0], 1.0)  # Class 1 at position (0,0)
        self.assertEqual(landusef[0, 1, 0, 1], 1.0)  # Class 2 at position (0,1)
        self.assertEqual(landusef[0, 2, 0, 2], 1.0)  # Class 3 at position (0,2)
        self.assertEqual(landusef[0, 3, 1, 0], 1.0)  # Class 4 at position (1,0)
        self.assertEqual(landusef[0, 4, 1, 1], 1.0)  # Class 5 at position (1,1)
        self.assertEqual(landusef[0, 5, 1, 2], 1.0)  # Class 6 at position (1,2)
        
        # Check that other positions are 0
        self.assertEqual(landusef[0, 0, 0, 1], 0.0)  # Class 1 at position (0,1) should be 0


class TestNLCDProcessor(unittest.TestCase):
    """Test the NLCDProcessor class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.processor = NLCDProcessor()
    
    def test_initialization(self):
        """Test processor initialization."""
        self.assertIsNotNone(self.processor.lulc_mapping)
        self.assertIsInstance(self.processor.lulc_mapping, LULCMapping)
    
    def test_get_processing_info(self):
        """Test getting processing information."""
        info = self.processor.get_processing_info()
        
        self.assertIn('lulc_mapping', info)
        self.assertIn('urban_classes', info)
        self.assertIn('total_classes', info)
        
        self.assertEqual(info['total_classes'], 40)
        self.assertEqual(info['urban_classes'], [21, 22, 23, 24])
    
    def test_set_custom_mapping(self):
        """Test setting custom mapping."""
        custom_mapping = {21: 30, 22: 31, 23: 32, 24: 33}
        self.processor.set_custom_mapping(custom_mapping)
        
        info = self.processor.get_processing_info()
        self.assertEqual(info['lulc_mapping'], custom_mapping)


if __name__ == '__main__':
    unittest.main()
