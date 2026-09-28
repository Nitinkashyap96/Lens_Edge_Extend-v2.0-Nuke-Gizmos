import os
import nuke

# Folder of this file (works on every Nuke version; falls back to relative paths)
try:
    _here = os.path.dirname(os.path.abspath(__file__))
except NameError:
    _here = None

for _sub in ('Icons', 'gizmos'):
    if _here:
        _p = os.path.join(_here, _sub)
        if os.path.isdir(_p):
            nuke.pluginAddPath(_p.replace('\\', '/'))
    else:
        nuke.pluginAddPath('./' + _sub)
