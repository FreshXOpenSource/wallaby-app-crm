# Copyright (c) by it's authors. 
# Some rights reserved. See LICENSE, AUTHORS.

# this is a namespace package
try:
    import pkg_resources
    pkg_resources.declare_namespace(__name__)
except:
    import pkgutil
    __path__ = pkgutil.extend_path(__path__, __name__)
