"""Pytest configuration - automatically loaded before tests."""
import sys
import os

# Add src, tests, and project root to path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
src_path = os.path.join(project_root, 'src')
tests_path = os.path.join(project_root, 'tests')

for path in [src_path, tests_path, project_root]:
    if path not in sys.path:
        sys.path.insert(0, path)
