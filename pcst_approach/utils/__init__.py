# Backwards-compatibility shim: the code now lives in the robust_pcst package.
# Keeps imports such as `from pcst_approach.utils.ppi import read_ppi` working.
import importlib
import os
import pkgutil
import sys

try:
    import robust_pcst
except ImportError:
    # Not installed: fall back to the repository root.
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
    import robust_pcst

from robust_pcst import *

for _module in pkgutil.walk_packages(robust_pcst.__path__, 'robust_pcst.'):
    if _module.name in ('robust_pcst.__main__', 'robust_pcst.cli'):
        continue
    sys.modules[__name__ + _module.name[len('robust_pcst'):]] = importlib.import_module(_module.name)
