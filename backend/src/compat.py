"""Python 3.14 compatibility fixes."""
import sys

# Python 3.14 removed deprecated audio modules - create stubs to prevent import errors
if sys.version_info >= (3, 14):
    import types
    for module_name in ['aifc', 'audioop', 'sunau', 'wave']:
        if module_name not in sys.modules:
            stub = types.ModuleType(module_name)
            sys.modules[module_name] = stub
