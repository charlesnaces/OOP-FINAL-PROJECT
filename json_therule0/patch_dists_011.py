#!/usr/bin/env python3
"""
Patch script to remove all license-related metadata from wheel and sdist for 0.1.1.
This is a workaround for setuptools auto-generating license-file fields.
"""

import zipfile
import tarfile
import tempfile
import re
from pathlib import Path

wheel = Path('dist/json_therule0-0.1.1-py3-none-any.whl')
sdist = Path('dist/json_therule0-0.1.1.tar.gz')

def clean_metadata(content):
    """Remove all license-related metadata lines."""
    lines = content.split('\n')
    # Filter out lines starting with 'License-' or containing 'license-file'
    filtered = [l for l in lines if not (l.startswith('License-') or 'license-file' in l.lower())]
    return '\n'.join(filtered)

# Patch the wheel
print(f"Patching wheel: {wheel}")
with tempfile.TemporaryDirectory() as tmpdir:
    tmpdir = Path(tmpdir)
    
    # Extract
    with zipfile.ZipFile(wheel, 'r') as z:
        z.extractall(tmpdir / 'wheel')
    
    # Modify METADATA and clean thoroughly
    for metadata_file in (tmpdir / 'wheel').rglob('METADATA'):
        print(f"  Found: {metadata_file}")
        content = metadata_file.read_text()
        cleaned = clean_metadata(content)
        metadata_file.write_text(cleaned)
        print(f"  Cleaned metadata")
    
    # Recreate wheel
    wheel.unlink()
    with zipfile.ZipFile(wheel, 'w', zipfile.ZIP_DEFLATED) as new_z:
        for file_path in (tmpdir / 'wheel').rglob('*'):
            if file_path.is_file():
                arcname = file_path.relative_to(tmpdir / 'wheel')
                new_z.write(file_path, arcname)

print(f"Patched wheel created: {wheel}\n")

# Patch the sdist
print(f"Patching sdist: {sdist}")
with tempfile.TemporaryDirectory() as tmpdir:
    tmpdir = Path(tmpdir)
    
    # Extract
    with tarfile.open(sdist, 'r:gz') as tar:
        tar.extractall(tmpdir / 'sdist')
    
    # Modify PKG-INFO files
    for pkg_info_file in (tmpdir / 'sdist').rglob('PKG-INFO'):
        print(f"  Found: {pkg_info_file}")
        content = pkg_info_file.read_text()
        cleaned = clean_metadata(content)
        pkg_info_file.write_text(cleaned)
        print(f"  Cleaned metadata")
    
    # Recreate sdist
    sdist.unlink()
    with tarfile.open(sdist, 'w:gz') as new_tar:
        for file_path in (tmpdir / 'sdist').rglob('*'):
            if file_path.is_file():
                arcname = file_path.relative_to(tmpdir / 'sdist')
                new_tar.add(file_path, arcname=str(arcname))

print(f"Patched sdist created: {sdist}")
print("\nDone! Run 'twine check dist/*' to validate.")
