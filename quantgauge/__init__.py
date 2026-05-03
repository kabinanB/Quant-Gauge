# quantgauge/__init__.py

from . import model

# Import model classes to trigger @register decorators
from .model import merton_jd, kou_jd

# Then import option API
from . import option

__all__ = ['option', 'model', 'merton_jd', 'kou_jd']