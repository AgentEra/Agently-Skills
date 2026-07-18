from pathlib import Path
import sys


TEMPLATE_ROOT = Path(__file__).resolve().parents[1]
if str(TEMPLATE_ROOT) not in sys.path:
    sys.path.insert(0, str(TEMPLATE_ROOT))
