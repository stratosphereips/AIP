from os import scandir, path
from importlib import import_module
from aip.utils.autoload import models

s = scandir(path.abspath(path.dirname(__file__)))
files = []
for f in s:
    if f.name.endswith('.py') and f.name != 'base.py' and f.name != '__init__.py':
        files.append(f)

for f in files:
    import_module(f'aip.models.{f.name[:-3]}')
