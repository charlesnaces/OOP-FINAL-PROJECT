# tests/test_jsonfile.py

import unittest
import json
import tempfile
import os
from pathlib import Path
from json_therule0 import JSONFile, read_json


class TestJSONFile(unittest.TestCase):
    """Comprehensive test suite for the JSONFile class."""

    @classmethod
    def setUpClass(cls):
        """Create temporary test files."""
        cls.temp_dir = tempfile.mkdtemp()
        
        # Create a simple structured JSON file
        cls.simple_json = os.path.join(cls.temp_dir, 'simple.json')
        simple_data = [
            {'name': 'Alice', 'age': 30, 'city': 'New York'},
            {'name': 'Bob', 'age': 25, 'city': 'Los Angeles'},
            {'name': 'Charlie', 'age': 35, 'city': 'Chicago'},
        ]
        with open(cls.simple_json, 'w') as f:
            json.dump(simple_data, f)
        
        # Create a COCO-format JSON file
        cls.coco_json = Path(__file__).parent.parent / 'data' / 'coco_sample.json'

    @classmethod
    def tearDownClass(cls):
        """Clean up temporary files."""
        import shutil
        shutil.rmtree(cls.temp_dir)

    # ============ Initialization Tests ============

    def test_init_simple_json(self):
        """Test initialization with simple JSON."""
        data = JSONFile(self.simple_json)
        self.assertIsNotNone(data)
        self.assertEqual(len(data), 3)
        self.assertEqual(data.shape(), (3, 3))

    def test_init_file_not_found(self):
        """Test initialization with non-existent file."""
        with self.assertRaises(FileNotFoundError):
            JSONFile('/nonexistent/path.json')

    def test_init_invalid_json(self):
        """Test initialization with invalid JSON."""
        bad_json = os.path.join(self.temp_dir, 'bad.json')
        with open(bad_json, 'w') as f:
            f.write('{invalid json}')
        
        with self.assertRaises(Exception):
            JSONFile(bad_json)

    # ============ Display Methods ============

    def test_head(self):
        """Test head() method."""
        data = JSONFile(self.simple_json)
        head_data = data.head(2)
        self.assertEqual(len(head_data), 2)
        self.assertEqual(head_data[0]['name'], 'Alice')

    def test_tail(self):
        """Test tail() method."""
        data = JSONFile(self.simple_json)
        tail_data = data.tail(2)
        self.assertEqual(len(tail_data), 2)
        self.assertEqual(tail_data[-1]['name'], 'Charlie')

    def test_info(self):
        """Test info() method."""
        data = JSONFile(self.simple_json)
        info = data.info()
        self.assertIn('Dataset Info', info)
        self.assertIn('Rows: 3', info)
        self.assertIn('Columns: 3', info)
        self.assertIn('name', info)
        self.assertIn('age', info)

    def test_summary(self):
        """Test summary() method."""
        data = JSONFile(self.simple_json)
        summary = data.summary()
        self.assertIn('Summary', summary)
        self.assertIn('Rows: 3', summary)
        self.assertIn('Statistics', summary)

    def test_stats(self):
        """Test stats() method."""
        data = JSONFile(self.simple_json)
        stats = data.stats()
        self.assertIn('age', stats)
        self.assertIn('name', stats)
        # Age is numeric, should have mean/std
        self.assertIn('mean', stats['age'])
        # Name is categorical, should have unique count
        self.assertIn('unique', stats['name'])

    # ============ Data Access Methods ============

    def test_shape(self):
        """Test shape() method."""
        data = JSONFile(self.simple_json)
        rows, cols = data.shape()
        self.assertEqual(rows, 3)
        self.assertEqual(cols, 3)

    def test_columns(self):
        """Test columns() method."""
        data = JSONFile(self.simple_json)
        cols = data.columns()
        self.assertIsInstance(cols, list)
        self.assertIn('name', cols)
        self.assertIn('age', cols)
        self.assertIn('city', cols)

    def test_data(self):
        """Test data() method."""
        data = JSONFile(self.simple_json)
        all_data = data.data()
        self.assertEqual(len(all_data), 3)
        self.assertIsInstance(all_data, list)
        self.assertIsInstance(all_data[0], dict)

    def test_len(self):
        """Test __len__() method."""
        data = JSONFile(self.simple_json)
        self.assertEqual(len(data), 3)

    # ============ Filter Tests ============

    def test_filter_by_value(self):
        """Test filter() method."""
        data = JSONFile(self.simple_json)
        result = data.filter('city', 'New York')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], 'Alice')

    def test_filter_nonexistent_column(self):
        """Test filter() with non-existent column."""
        data = JSONFile(self.simple_json)
        with self.assertRaises(ValueError) as context:
            data.filter('nonexistent', 'value')
        self.assertIn('not found', str(context.exception))
        self.assertIn('nonexistent', str(context.exception))

    def test_filter_no_matches(self):
        """Test filter() with no matching values."""
        data = JSONFile(self.simple_json)
        result = data.filter('city', 'Nonexistent City')
        self.assertEqual(len(result), 0)

    # ============ Select Tests ============

    def test_select_columns(self):
        """Test select() method."""
        data = JSONFile(self.simple_json)
        result = data.select(['name', 'age'])
        self.assertEqual(len(result), 3)
        # Each record should only have name and age
        self.assertEqual(set(result[0].keys()), {'name', 'age'})
        self.assertNotIn('city', result[0])

    def test_select_single_column(self):
        """Test select() with single column."""
        data = JSONFile(self.simple_json)
        result = data.select(['name'])
        self.assertEqual(len(result), 3)
        for record in result:
            self.assertEqual(len(record), 1)
            self.assertIn('name', record)

    def test_select_nonexistent_column(self):
        """Test select() with non-existent column."""
        data = JSONFile(self.simple_json)
        with self.assertRaises(ValueError) as context:
            data.select(['name', 'nonexistent'])
        self.assertIn('not found', str(context.exception))

    def test_select_preserves_order(self):
        """Test that select() preserves record order."""
        data = JSONFile(self.simple_json)
        result = data.select(['name'])
        names = [r['name'] for r in result]
        self.assertEqual(names, ['Alice', 'Bob', 'Charlie'])

    # ============ Sort Tests ============

    def test_sort_ascending(self):
        """Test sort() in ascending order."""
        data = JSONFile(self.simple_json)
        result = data.sort('age', ascending=True)
        ages = [r['age'] for r in result]
        self.assertEqual(ages, [25, 30, 35])

    def test_sort_descending(self):
        """Test sort() in descending order."""
        data = JSONFile(self.simple_json)
        result = data.sort('age', ascending=False)
        ages = [r['age'] for r in result]
        self.assertEqual(ages, [35, 30, 25])

    def test_sort_by_string(self):
        """Test sort() by string column."""
        data = JSONFile(self.simple_json)
        result = data.sort('name', ascending=True)
        names = [r['name'] for r in result]
        self.assertEqual(names, ['Alice', 'Bob', 'Charlie'])

    def test_sort_nonexistent_column(self):
        """Test sort() with non-existent column."""
        data = JSONFile(self.simple_json)
        with self.assertRaises(ValueError):
            data.sort('nonexistent')

    def test_sort_default_ascending(self):
        """Test that sort() defaults to ascending."""
        data = JSONFile(self.simple_json)
        result = data.sort('age')
        ages = [r['age'] for r in result]
        self.assertEqual(ages, [25, 30, 35])

    # ============ Export Tests ============

    def test_to_csv(self):
        """Test to_csv() method."""
        data = JSONFile(self.simple_json)
        output_csv = os.path.join(self.temp_dir, 'output.csv')
        data.to_csv(output_csv)
        self.assertTrue(os.path.exists(output_csv))
        
        # Verify CSV content
        with open(output_csv, 'r') as f:
            lines = f.readlines()
        self.assertGreater(len(lines), 1)  # Header + data

    def test_to_json(self):
        """Test to_json() method."""
        data = JSONFile(self.simple_json)
        output_json = os.path.join(self.temp_dir, 'output.json')
        data.to_json(output_json)
        self.assertTrue(os.path.exists(output_json))
        
        # Verify JSON content
        with open(output_json, 'r') as f:
            exported = json.load(f)
        self.assertEqual(len(exported), 3)

    # ============ String Representations ============

    def test_repr(self):
        """Test __repr__() method."""
        data = JSONFile(self.simple_json)
        repr_str = repr(data)
        self.assertIn('JSONFile', repr_str)
        self.assertIn('rows=3', repr_str)

    def test_str(self):
        """Test __str__() method."""
        data = JSONFile(self.simple_json)
        str_repr = str(data)
        self.assertIn('3 rows', str_repr)
        self.assertIn('3 columns', str_repr)

    # ============ API Function Tests ============

    def test_read_json_api(self):
        """Test read_json() API function."""
        data = read_json(self.simple_json)
        self.assertIsInstance(data, JSONFile)
        self.assertEqual(len(data), 3)

    # ============ Edge Cases ============

    def test_empty_list(self):
        """Test with empty JSON list."""
        empty_json = os.path.join(self.temp_dir, 'empty.json')
        with open(empty_json, 'w') as f:
            json.dump([], f)
        
        data = JSONFile(empty_json)
        self.assertEqual(len(data), 0)
        self.assertEqual(data.shape(), (0, 0))

    def test_single_record(self):
        """Test with single record."""
        single_json = os.path.join(self.temp_dir, 'single.json')
        with open(single_json, 'w') as f:
            json.dump([{'key': 'value'}], f)
        
        data = JSONFile(single_json)
        self.assertEqual(len(data), 1)
        self.assertEqual(data.head(1)[0]['key'], 'value')

    def test_null_values(self):
        """Test handling of null values in data."""
        null_json = os.path.join(self.temp_dir, 'null.json')
        null_data = [
            {'name': 'Alice', 'age': 30},
            {'name': 'Bob', 'age': None},
        ]
        with open(null_json, 'w') as f:
            json.dump(null_data, f)
        
        data = JSONFile(null_json)
        self.assertEqual(len(data), 2)
        stats = data.stats()
        # Should handle None values gracefully
        self.assertIsNotNone(stats)

    def test_mixed_types(self):
        """Test handling of mixed types in columns."""
        mixed_json = os.path.join(self.temp_dir, 'mixed.json')
        mixed_data = [
            {'value': 10},
            {'value': 'string'},
            {'value': 20},
        ]
        with open(mixed_json, 'w') as f:
            json.dump(mixed_data, f)
        
        data = JSONFile(mixed_json)
        # Should handle mixed types without error
        self.assertEqual(len(data), 3)

    # ============ Chain Operations Tests ============

    def test_filter_then_select(self):
        """Test chaining filter and select operations."""
        data = JSONFile(self.simple_json)
        filtered = data.filter('city', 'New York')
        # Select from filtered results
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]['name'], 'Alice')

    def test_select_then_sort(self):
        """Test selecting columns then sorting."""
        data = JSONFile(self.simple_json)
        selected = data.select(['name', 'age'])
        # Manually sort selected data
        sorted_by_age = sorted(selected, key=lambda x: x['age'])
        self.assertEqual(sorted_by_age[0]['age'], 25)

    def test_operations_on_empty_result(self):
        """Test operations on empty filter results."""
        data = JSONFile(self.simple_json)
        empty_result = data.filter('city', 'Nonexistent')
        self.assertEqual(len(empty_result), 0)


if __name__ == '__main__':
    unittest.main()
