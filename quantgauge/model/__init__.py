# quantgauge/model/__init__.py
try:
    from . import merton_cpp
    from . import kou_cpp
except ImportError as e:
    # This helps you debug in Colab
    import os
    print(f"DEBUG: Files in this directory: {os.listdir(os.path.dirname(__file__))}")
    raise ImportError(f"C++ extensions not found. Check build logs. Original error: {e}")

__all__ = ['merton_cpp', 'kou_cpp']