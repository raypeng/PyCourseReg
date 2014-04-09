from distutils.core import setup
import py2exe, sys

setup(
    options = {'py2exe': {'bundle_files': 1, 'compressed': True}},
    windows = [{'script': "Scheduler.py"}],
    zipfile = None,
)