"""Package initialization for src module."""
import sys

# Python 3.14 compatibility: stub out removed deprecated audio modules
if sys.version_info >= (3, 14):
    import types
    for module_name in ['aifc', 'audioop', 'sunau', 'wave']:
        if module_name not in sys.modules:
            sys.modules[module_name] = types.ModuleType(module_name)