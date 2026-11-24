"""pyrun.py - run a repo script with the engine's embedded Python (kit\\py.cmd uses it).

The embedded Python ignores PYTHONPATH and does not put the script's folder on sys.path, so the tools' sibling
imports (localboxes, headroom, modelstore ...) would fail. This adds that folder, then runs the script as __main__.
"""
import os
import runpy
import sys

if len(sys.argv) < 2:
    sys.exit("usage: kit\\py.cmd <script.py> [args ...]")
script = os.path.abspath(sys.argv[1])
sys.argv = [script] + sys.argv[2:]
sys.path.insert(0, os.path.dirname(script))
runpy.run_path(script, run_name="__main__")
