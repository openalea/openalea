from openalea.release.tool import Tool

class setuptools(Tool):
    installable    = False
    exe            = "easy_install"+exe_ext
    default_paths  = [ Tool.PyExecPaths ]