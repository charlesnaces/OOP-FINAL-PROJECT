# json_therule0/normalizer.py

import json
import copy
from typing import Dict, List, Any, Tuple


class Normalizer:
    """
    Detects and normalizes unstructured JSON files (like COCO format).
    Converts unstructured data into a clean, tabular format suitable for analysis.
    """

    def __init__(self, filepath: str):
        """
        Initialize the Normalizer with a JSON file.

        Args:
            filepath (str): Path to the JSON file to normalize.
        """
        self.filepath = filepath
        self.raw_data = self._load_json()
        self.detected_format = self._detect_format()
        self.normalized_data = []

    def _load_json(self) -> Any:
        """Load and parse JSON file."""
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {self.filepath}")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON in file: {self.filepath}")

    def _detect_format(self) -> str:
        """
        Detect the format of the unstructured JSON.

        Returns:
            str: Format type ('coco', 'nested_list', 'nested_dict', 'array', 'unknown')
        """
        if isinstance(self.raw_data, dict):
            keys = set(self.raw_data.keys())
            
            # Detect COCO-like format
            if keys >= {'images', 'annotations'} or (
                'images' in keys and isinstance(self.raw_data['images'], list)
            ):
                return 'coco'
            
            # Detect nested dictionary structure
            if any(isinstance(v, dict) for v in self.raw_data.values()):
                return 'nested_dict'
            
            # Detect single-level dict with arrays
            if any(isinstance(v, list) for v in self.raw_data.values()):
                return 'nested_list'
        
        elif isinstance(self.raw_data, list):
            return 'array'
        
        return 'unknown'

    def normalize(self) -> List[Dict]:
        """
        Normalize the data based on detected format.

        Returns:
            list: Normalized data as list of dictionaries.
        """
        if self.detected_format == 'coco':
            self.normalized_data = self._normalize_coco()
        elif self.detected_format == 'nested_list':
            self.normalized_data = self._normalize_nested_list()
        elif self.detected_format == 'nested_dict':
            self.normalized_data = self._normalize_nested_dict()
        elif self.detected_format == 'array':
            self.normalized_data = self._normalize_array()
        else:
            self.normalized_data = self._normalize_unknown()
        
        return self.normalized_data

    def _normalize_coco(self) -> List[Dict]:
        """
        Normalize COCO-format data by joining images, annotations, and categories.
        
        Returns:
            list: List of dictionaries with flattened structure.
        """
        images = {img['id']: img for img in self.raw_data.get('images', [])}
        categories = {cat['id']: cat['name'] for cat in self.raw_data.get('categories', [])}
        
        normalized = []
        for ann in self.raw_data.get('annotations', []):
            record = {
                'annotation_id': ann.get('id'),
                'image_id': ann.get('image_id'),
                'category_id': ann.get('category_id'),
                'category_name': categories.get(ann.get('category_id'), 'unknown'),
            }
            
            # Add image info if available
            if ann.get('image_id') in images:
                img = images[ann['image_id']]
                record['image_name'] = img.get('file_name')
                record['image_width'] = img.get('width')
                record['image_height'] = img.get('height')
            
            # Add annotation details
            if 'bbox' in ann:
                bbox = ann['bbox']
                record['bbox_x'] = bbox[0] if len(bbox) > 0 else None
                record['bbox_y'] = bbox[1] if len(bbox) > 1 else None
                record['bbox_width'] = bbox[2] if len(bbox) > 2 else None
                record['bbox_height'] = bbox[3] if len(bbox) > 3 else None
            
            if 'area' in ann:
                record['area'] = ann['area']
            
            if 'iscrowd' in ann:
                record['iscrowd'] = ann['iscrowd']
            
            normalized.append(record)
        
        return normalized

    def _normalize_nested_list(self) -> List[Dict]:
        """
        Normalize data with nested lists by expanding and flattening.
        
        Returns:
            list: Flattened list of dictionaries.
        """
        normalized = []
        for key, values in self.raw_data.items():
            if isinstance(values, list):
                for item in values:
                    record = {'source': key}
                    if isinstance(item, dict):
                        record.update(item)
                    else:
                        record['value'] = item
                    normalized.append(record)
        
        return normalized if normalized else [self.raw_data]

    def _normalize_nested_dict(self) -> List[Dict]:
        """
        Normalize deeply nested dictionary structures.
        
        Returns:
            list: Flattened list of dictionaries.
        """
        def flatten_dict(d, parent_key='', sep='_'):
            items = []
            for k, v in d.items():
                new_key = f"{parent_key}{sep}{k}" if parent_key else k
                if isinstance(v, dict):
                    items.extend(flatten_dict(v, new_key, sep=sep).items())
                elif isinstance(v, list):
                    items.append((new_key, v))
                else:
                    items.append((new_key, v))
            return dict(items)
        
        return [flatten_dict(self.raw_data)]

    def _normalize_array(self) -> List[Dict]:
        """
        Normalize array data (already structured, minimal changes).
        
        Returns:
            list: Same data if already a list of dicts.
        """
        if all(isinstance(item, dict) for item in self.raw_data):
            return copy.deepcopy(self.raw_data)
        
        # Convert non-dict items to dicts
        return [{'value': item, 'index': idx} for idx, item in enumerate(self.raw_data)]

    def _normalize_unknown(self) -> List[Dict]:
        """
        Handle unknown formats by wrapping in a dictionary.
        
        Returns:
            list: Data wrapped in a list.
        """
        return [{'data': self.raw_data}]

    def get_structure_info(self) -> Dict[str, Any]:
        """
        Get information about the data structure.

        Returns:
            dict: Structure information including format, sections, and sample.
        """
        info = {
            'detected_format': self.detected_format,
            'original_type': type(self.raw_data).__name__,
        }
        
        if self.detected_format == 'coco':
            info['sections'] = {
                'images': len(self.raw_data.get('images', [])),
                'annotations': len(self.raw_data.get('annotations', [])),
                'categories': len(self.raw_data.get('categories', [])),
            }
        elif isinstance(self.raw_data, dict):
            info['sections'] = {k: len(v) if isinstance(v, list) else type(v).__name__ 
                              for k, v in self.raw_data.items()}
        
        if self.normalized_data:
            info['normalized_records'] = len(self.normalized_data)
            info['normalized_columns'] = list(self.normalized_data[0].keys()) if self.normalized_data else []
            info['sample_record'] = self.normalized_data[0] if self.normalized_data else None
        
        return info

    def display_structure(self) -> str:
        """
        Display the data structure in a human-readable format.

        Returns:
            str: Formatted structure information.
        """
        info = self.get_structure_info()
        
        output = []
        output.append("=" * 60)
        output.append(f"Format Detected: {info['detected_format'].upper()}")
        output.append("=" * 60)
        
        if 'sections' in info:
            output.append("\nData Sections:")
            for section, count in info['sections'].items():
                output.append(f"  - {section}: {count}")
        
        if 'normalized_records' in info:
            output.append(f"\nNormalized Records: {info['normalized_records']}")
            output.append(f"Columns: {', '.join(info['normalized_columns'])}")
        
        if info.get('sample_record'):
            output.append(f"\nSample Record:")
            for k, v in list(info['sample_record'].items())[:5]:
                output.append(f"  {k}: {v}")
        
        output.append("=" * 60)
        
        return "\n".join(output)

    def __repr__(self) -> str:
        """String representation."""
        return f"<Normalizer format='{self.detected_format}' records={len(self.normalized_data)}>"
