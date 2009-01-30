"""SCons.Tool.yacc

Tool-specific initialization for yacc.

There normally shouldn't be any need to import this module directly.
It will usually be imported through the generic SCons.Tool.Tool()
selection method.

"""

__license__ = "Cecill-C"
__revision__ =" $Id$"

#
# Copyright (c) 2001, 2002, 2003, 2004 The SCons Foundation
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

__revision__ = "/home/scons/scons/branch.0/baseline/src/engine/SCons/Tool/yacc.py 0.96.1.D001 2004/08/23 09:55:29 knight"

import os.path

import SCons.Defaults
import SCons.Tool
import SCons.Util

try:
    YaccAction= SCons.Defaults.YaccAction
except:
    YaccAction = SCons.Action.Action("$YACCCOM", "$YACCCOMSTR")
    
yy_suffix=['.y','.yy']

def _yaccEmitter(target, source, env, ysuf, hsuf):
    # If -d is specified on the command line, yacc will emit a .h
    # or .hpp file as well as a .c or .cpp file, depending on whether
    # the input file is a .y or .yy, respectively.
    if len(source) and '-d' in SCons.Util.CLVar(env.subst("$YACCFLAGS")):
        base, ext = os.path.splitext(SCons.Util.to_String(source[0]))
        if ext in ysuf:
            base, ext = os.path.splitext(SCons.Util.to_String(target[0]))
            target.append(base + hsuf)
    return (target, source)

def yEmitter(target, source, env):
    return _yaccEmitter(target, source, env, '.y', '.h')

def yyEmitter(target, source, env):
    if env.subst( "BISON_HPP" ):
      return _yaccEmitter(target, source, env, yy_suffix, '.hpp')
    else: 
      return _yaccEmitter(target, source, env, yy_suffix, '.cpp.h')

def generate(env):
    """Add Builders and construction variables for yacc to an Environment."""
    c_file, cxx_file = SCons.Tool.createCFileBuilders(env)

    c_file.add_action('.y', YaccAction)
    for yy in yy_suffix:
      cxx_file.add_action(yy, YaccAction)
    c_file.add_emitter('.y', yEmitter)
    for yy in yy_suffix:
      cxx_file.add_emitter(yy, yyEmitter)

    env['YACC']      = env.Detect('bison') or 'yacc'
    env['YACCFLAGS'] = SCons.Util.CLVar('')
    env['YACCCOM']   = '$YACC $YACCFLAGS -o $TARGET $SOURCES'

def exists(env):
    return env.Detect(['bison', 'yacc'])
