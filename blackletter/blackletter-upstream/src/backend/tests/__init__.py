"""Test package for backend module.

Adjusts Python path so tests can import the ``backend`` package when run
from the repository root.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
