import zipfile
import tarfile
from pathlib import Path

DIST_DIR = Path('dist')
wheel = DIST_DIR / 'json_therule0-0.1.0-py3-none-any.whl'
sdist = DIST_DIR / 'json_therule0-0.1.0.tar.gz'

# Helper to clean metadata text
def clean_metadata_text(text: str) -> str:
    lines = text.splitlines()
    new_lines = []
    for line in lines:
        if line.startswith('License-File:'):
            continue
        if line.startswith('License-Expression:'):
            continue
        if line.strip() == 'Dynamic: license-file':
            continue
        new_lines.append(line)
    return '\n'.join(new_lines) + '\n'

# Patch wheel METADATA
with zipfile.ZipFile(wheel, 'r') as z:
    items = z.namelist()
    meta_files = [n for n in items if n.endswith('METADATA')]
    temp_dir = Path('dist/_wheel_temp')
    if temp_dir.exists():
        import shutil
        shutil.rmtree(temp_dir)
    temp_dir.mkdir(parents=True)
    z.extractall(temp_dir)

meta_path = temp_dir / meta_files[0]
meta_text = meta_path.read_text(encoding='utf-8')
meta_text_clean = clean_metadata_text(meta_text)
meta_path.write_text(meta_text_clean, encoding='utf-8')

# Repack wheel
new_wheel = DIST_DIR / 'json_therule0-0.1.0-py3-none-any-fixed.whl'
with zipfile.ZipFile(new_wheel, 'w', compression=zipfile.ZIP_DEFLATED) as z:
    for f in temp_dir.rglob('*'):
        z.write(f, f.relative_to(temp_dir))

# Clean up temp
import shutil
shutil.rmtree(temp_dir)

# Patch sdist PKG-INFO inside tar.gz
with tarfile.open(sdist, 'r:gz') as tar:
    members = tar.getmembers()
    temp_sdist_dir = Path('dist/_sdist_temp')
    if temp_sdist_dir.exists():
        shutil.rmtree(temp_sdist_dir)
    temp_sdist_dir.mkdir(parents=True)
    tar.extractall(temp_sdist_dir)

# Find PKG-INFO and patch
pkg_info = None
for p in temp_sdist_dir.rglob('PKG-INFO'):
    pkg_info = p
    break
if pkg_info is not None:
    text = pkg_info.read_text(encoding='utf-8')
    text_clean = clean_metadata_text(text)
    pkg_info.write_text(text_clean, encoding='utf-8')

# Repack sdist
new_sdist = DIST_DIR / 'json_therule0-0.1.0-fixed.tar.gz'
with tarfile.open(new_sdist, 'w:gz') as tar:
    # tar from temp_sdist_dir contents
    for f in sorted(temp_sdist_dir.rglob('*')):
        tar.add(f, arcname=str(f.relative_to(temp_sdist_dir)))

shutil.rmtree(temp_sdist_dir)

print('Patched wheel and sdist created:')
print(new_wheel)
print(new_sdist)
