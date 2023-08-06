import six

if six.PY3:
    from border_secure_core.py3_core import *
else:
    from border_secure_core.py2_core import *