#!/usr/bin/python
# -*- coding: utf-8 -*-

#This file is part of pyLot library.
#
# pyLot is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyLot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with pyLot.  If not, see <http://www.gnu.org/licenses/>.

__author__ = u'Pierre Puiseux, Guillaume Baty'
__copyright__ = u"Copyright 2011-2012 (C) andheo, Université de Pau et des Pays de l'Adour"
__credits__ = [u'Pierre Puiseux', u'Guillaume Baty']
__license__ = "GNU Lesser General Public License"

__all__ = [
  'generate_pyfile_from_uifile',
  'compile_ui_files'
  ]

import logging
import sys
import os

from pyLot.application import APPLICATION
from pyLot.core import Path, get_data, unicode2

LOGGER = logging.getLogger('pyLot.qtgui')

try :
    if os.environ['QT_API'] == 'pyqt' :
        from PyQt4.uic import compileUi
        compile_args = dict(execute=False, indent=4)
    elif os.environ['QT_API'] == 'pyside' :
        from pysideuic import compileUi
        compile_args = dict(execute=False, indent=4, from_imports=False)
    else :
        raise NotImplementedError
except ImportError :
    LOGGER.critical('You must install %s-tools' % os.environ['QT_API'])

def generate_pyfile_from_uifile (name, src=None, dest=None) :
    u"""
    Function searches ...

    if src is None :
      - <moduledir>/designer/<modulename>.ui
      - OR <moduledir>/<modulename>.ui
    else :
      - src

    File generated is
    if dest is None :
      - _<uifilebase>.py (Ex: mywdget.ui -> _mywidget.py)
    else :
      - dest

    .. warning ::

      To work, this function has to be called in an **imported** module.
      (__name__ must differ from __main__) else, nothing is done !

      Do not edit generated file because all data written here are lost.

    :param filename: the qt-designer ui file name. Ex: options.ui
    :type filename: str

    :return: Qt class (corresponding to filename), Qt type class (type of first value)
    :rtype: couple
    """
    if name == '__main__' :
        return
    paths = []
    if src :
        filepath = Path(src)
        paths.append(filepath)
    else :
        path = u'designer/%s.ui' % name.split(u'.')[-1]
        filepath = Path(get_data(name, path))
        paths.append(filepath)

        path = u'%s.ui' % name.split(u'.')[-1]
        filepath = Path(get_data(name, path))
        paths.append(filepath)

    for path in paths :
        if path.isfile() :
            break

#  tmpdir = mkdtempu()
    if dest is None:
        pyfilename = Path(path.parent, '_' + path.name.replace('.ui', '.py'))
    else :
        pyfilename = Path(dest)

    if not pyfilename.exists() :
        generate = True
    else :
        mtime_py = pyfilename.mtime_datetime()
        mtime_ui = path.mtime_datetime()
        if mtime_py > mtime_ui :
            generate = False
        else :
            generate = True

    if generate or APPLICATION.FORCE_UI_GENERATION :
        module_dir = unicode(path.parent)
        if module_dir not in sys.path :
            sys.path.append(module_dir)

        if APPLICATION.FORCE_UI_GENERATION :
            LOGGER.info(u'construction forcée de %s à partir de %s\n' % (pyfilename, path))
#      uprint(u'pour désactiver la génération forcée:\n')
#      uprint(u' from pyLot.application import APPLICATION\n')
#      uprint(u' APPLICATION.FORCE_UI_GENERATION = False\n')
        else :
            LOGGER.info(u'%s a changé, reconstruction de %s\n' % (path, pyfilename))

        pyfile = open(pyfilename, 'w')
        compileUi(path, pyfile, **compile_args)
        pyfile.close()


def compile_ui_files(module, import_instructions=None):
    u"""
    Reads recursively all *.py files in root directory looking for
    "generate_pyfile_from_uifile" calls.
    If this call is found, execute it in order to compile ui file.

    import_instructions : python code containing required imports.
    example :

    >>> import_instructions = 'from pyLot.qtgui import generate_pyfile_from_uifile\n'

    if None, uses default imports : generate_pyfile_from_uifile, Path, hardbook and get_data
    """
    import ast
    from pyLot_external import codegen

    if import_instructions is None :
        import_instructions = """
    from pyLot.qtgui import generate_pyfile_from_uifile
    from pyLot.core import hardbook, get_data, Path

    """
    if module == 'pyLot' :
        module = '_pylot'
    root = Path(unicode2(__import__(module).__file__)).parent
    for py in root.walkfiles(u'*.py'):
        f = open(py)
        lines = f.readlines()
        f.close()

        code = ''.join(lines)
        try :
            r = ast.parse(code)
        except SyntaxError :
            print 'SYNTAX ERROR: cannot read ...', py
        else :
            for instr in r.body :
                if isinstance(instr, ast.Expr) :
                    value = instr.value
                    if isinstance(value, ast.Call):
                        try :
                            func_name = value.func.id
                        except AttributeError :
                            pass
                        else :
                            if func_name == u'generate_pyfile_from_uifile' :
                                src = codegen.to_source(instr)
                                if py.startswith(u'./') or py.startswith(u'.\\'):
                                    py = Path(py[2:])
                                name = root.parent.relpathto(py).replaceext(u'').replace(os.sep, u'.')
                                src = src.replace('__name__', repr(name))
                                try :
                                    code = compile(import_instructions + src, "<string>", "exec")
                                    exec code
                                except :
                                    print 'COMPILATION ERROR: cannot compile', py
                                    print
