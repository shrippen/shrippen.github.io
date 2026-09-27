#!/usr/bin/env python3
"""Checks that every project has the current demo world. Same as tools/sync-demo.py --check."""
import runpy
import sys

sys.argv = [sys.argv[0], "--check", *sys.argv[1:]]
runpy.run_path(str(__import__("pathlib").Path(__file__).with_name("sync-demo.py")), run_name="__main__")
