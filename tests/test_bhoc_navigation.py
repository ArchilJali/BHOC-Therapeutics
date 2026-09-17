"""Use the user-approved knowledge-map tests; keep legacy checks for old layout."""
from pathlib import Path
import runpy
root=Path(__file__).resolve().parents[1]
name='test_knowledge_map.py' if (root/'bhoc/knowledge-map-baseline.json').exists() else 'test_bhoc_navigation_legacy.py'
runpy.run_path(str(root/'tests'/name),run_name='__main__')
