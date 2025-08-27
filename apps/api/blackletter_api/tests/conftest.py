import sys
from pathlib import Path

# Ensure `apps/api` is on sys.path so `import blackletter_api` works
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

