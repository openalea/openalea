from openalea.release.tool import Tool

class openalea_deploy(Tool):
    installable    = False
    exe            = "alea_install"+exe_ext
    default_paths  = [ Tool.PyExecPaths  ]