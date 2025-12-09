# test_normalizer.py

import unittest
from pathlib import Path
import json
from json_therule0 import Normalizer, Analyzer, JSONCleaner


class TestNormalizer(unittest.TestCase):
    """Test suite for the Normalizer class."""

    def setUp(self):
        """Set up test data."""
        self.coco_file = Path(__file__).parent.parent / 'data' / 'coco_sample.json'

    def test_coco_detection(self):
        """Test detection of COCO format."""
        if not self.coco_file.exists():
            self.skipTest("COCO sample file not found")
        
        normalizer = Normalizer(str(self.coco_file))
        self.assertEqual(normalizer.detected_format, 'coco')

    def test_coco_normalization(self):
        """Test COCO format normalization."""
        if not self.coco_file.exists():
            self.skipTest("COCO sample file not found")
        
        normalizer = Normalizer(str(self.coco_file))
        normalized = normalizer.normalize()
        
        # Should have as many records as annotations
        self.assertEqual(len(normalized), 4)
        
        # Each record should have expected columns
        first_record = normalized[0]
        self.assertIn('annotation_id', first_record)
        self.assertIn('image_id', first_record)
        self.assertIn('category_name', first_record)
        self.assertIn('image_name', first_record)

    def test_structure_info(self):
        """Test getting structure information."""
        if not self.coco_file.exists():
            self.skipTest("COCO sample file not found")
        
        normalizer = Normalizer(str(self.coco_file))
        normalizer.normalize()
        info = normalizer.get_structure_info()
        
        self.assertEqual(info['detected_format'], 'coco')
        self.assertIn('sections', info)
        self.assertEqual(info['sections']['images'], 3)
        self.assertEqual(info['sections']['annotations'], 4)
        self.assertEqual(info['sections']['categories'], 3)

    def test_display_structure(self):
        """Test structure display."""
        if not self.coco_file.exists():
            self.skipTest("COCO sample file not found")
        
        normalizer = Normalizer(str(self.coco_file))
        normalizer.normalize()
        display = normalizer.display_structure()
        
        self.assertIn('COCO', display)
        self.assertIn('Normalized Records', display)
        self.assertIn('image_name', display)

    def test_workflow_normalize_clean_analyze(self):
        """Test complete workflow: normalize -> clean -> analyze."""
        if not self.coco_file.exists():
            self.skipTest("COCO sample file not found")
        
        # Normalize unstructured data
        normalizer = Normalizer(str(self.coco_file))
        normalized_data = normalizer.normalize()
        
        # Clean the normalized data
        # For this test, we'll create a temporary cleaned version
        cleaned_data = [
            {k: v for k, v in record.items() if v is not None}
            for record in normalized_data
        ]
        
        # Analyze the cleaned data
        analyzer = Analyzer(cleaned_data)
        
        self.assertEqual(len(analyzer), 4)
        self.assertGreater(len(analyzer.get_columns()), 0)
        
        stats = analyzer.summary_stats()
        self.assertIsNotNone(stats)


if __name__ == '__main__':
    unittest.main()
