import sys
import os

sys.path.append(os.path.abspath('../../misc'))
from openalea.misc import sphinx_tools



filenames = ['./deploygui/openalea_deploygui_alea_install_gui_ref.rst']
for file in filenames:
    process = sphinx_tools.PostProcess(file)
    process.remove_inheritance()


filenames = ['./deploygui/openalea_deploygui_postinstall_ref.rst']
for file in filenames:
    process = sphinx_tools.PostProcess(file)
    process.remove_header(nline=2, start=4)
    process.no_namespace_in_automodule()
