# quantgauge/__init__.py

from . import base
from . import option
# CRITICAL: This line forces Python to run the decorators in your models
import quantgauge.model.black_sholes