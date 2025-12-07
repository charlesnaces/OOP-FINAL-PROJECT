import zipfile
from pathlib import Path
p=Path('dist/json_therule0-0.1.0-py3-none-any.whl')
with zipfile.ZipFile(p) as z:
    names=[n for n in z.namelist() if n.endswith('METADATA')]
    print('METADATA files:', names)
    for n in names:
        print('---',n)
        print(z.read(n).decode('utf-8'))
