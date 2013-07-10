from openalea.release.tool import Tool

class cmake(Tool):
    url            = "http://www.cmake.org/files/v2.8/cmake-2.8.7-win32-x86.zip"
    arch_name_ext  = "zip"
    archive_subdir = r"cmake*\bin"
    exe            = "cmake.exe"
    default_paths  = [ "c:\\Program Files (x86)\\cmake*\\bin\\",
                       "c:\\Program Files\\cmake*\\bin\\",
                       "c:\\CMake*\\bin\\"]