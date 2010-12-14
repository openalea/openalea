"""f2py Tool

Tool-specific initialization for f2py.

There normally shouldn't be any need to import this module directly.
It will usually be imported through the generic SCons.Tool.Tool()
selection method.

"""

import os
from os.path import join as pjoin, dirname as pdirname, \
                    basename as pbasename, splitext
import re
import sys
import subprocess

import SCons.Action
import SCons.Scanner
import SCons.Tool
import SCons.Util
from SCons.Node.FS import default_fs

CGEN_TEMPLATE   = '%smodule'
FOBJECT_FILE    = 'fortranobject.c'
FWRAP_TEMPLATE  = '%s-f2pywrappers.f'

# Those regex are copied from build_src in numpy.distutils.command
F2PY_MODNAME_MATCH = re.compile(r'\s*python\s*module\s*(?P<name>[\w_]+)',
                                re.I).match
F2PY_UMODNAME_MATCH = re.compile(r'\s*python\s*module\s*(?P<name>[\w_]*?'\
                                     '__user__[\w_]*)',re.I).match
# End of copy

def get_f2py_modulename_from_txt(source):
    """This returns the name of the module from the pyf source file.

    source is expected to be one string, containing the whole source file
    code."""
    name = None
    for line in source.splitlines():
        m = F2PY_MODNAME_MATCH(line)
        if m:
            if F2PY_UMODNAME_MATCH(line): # skip *__user__* names
                continue
            name = m.group('name')
            break
    return name

def get_f2py_modulename_from_node(source):
    """This function returns the module name of the pyf file.

    The argument should be a scons node. This should work even if the node is
    generated from another scons builder."""
    # See email on scons-users from 6th April 2008 (Dmitry Mikhin).
    name = None
    node = source.rfile()
    if node.exists() or not node.is_derived():
        name = get_f2py_modulename_from_txt(node.get_contents())
    else:
        try:
            # XXX: I don't understand this part
            snode = source.sources[0].rfile()
            if snode.is_derived():
                snode = snode.sources[0].rfile()
            cnt = snode.get_contents()
            name = get_f2py_modulename_from_txt(cnt)
        except AttributeError:
            pass
    if name is None:
        raise ValueError("f2py file %s not found ?" % str(source))
    return name

def F2pyEmitter(target, source, env):
    build_dir = pdirname(str(target[0]))
    if is_pyf(str(source[0])):
        # target is (in this order):
        # - the C file which will contain the generated code
        # - the fortranobject.c file
        # - the f2py fortran wrapper
        basename = get_f2py_modulename_from_node(source[0])
        ntarget = []

        cgename = (CGEN_TEMPLATE % basename) + env['CFILESUFFIX']
        ntarget.append(default_fs.Entry(pjoin(build_dir, cgename)))

        fobj = pjoin(build_dir, mangle_fortranobject(basename, FOBJECT_FILE))
        ntarget.append(default_fs.Entry(fobj))

        f2pywrap = pjoin(build_dir, FWRAP_TEMPLATE % basename)
        ntarget.append(default_fs.Entry(f2pywrap))
    else:
        ntarget = target
        fobj = pjoin(build_dir, mangle_fortranobject(str(target[0]),
                     FOBJECT_FILE))
        ntarget.append(default_fs.Entry(fobj))
    return (ntarget, source)

def mangle_fortranobject(targetname, filename):
    basename = pbasename(targetname).split('module')[0]
    return '%s_%s' % (basename, filename)

def is_pyf(source_file):
    return splitext(source_file)[1] == '.pyf'

def f2py_cmd_exec(cmd):
    """Executes a f2py command.

    The point to execute f2py in a new process instead of using f2py.mainto
    avoid race issues when using multible jobs with scons.

    cmd should be a sequence. """
    f2py_cmd = [sys.executable, '-c',
                '"from numpy.f2py.f2py2e import run_main;run_main(%s)"' \
                % repr(cmd)]
    p = subprocess.Popen(" ".join(f2py_cmd), shell = True, stdout =
                         subprocess.PIPE)
    for i in p.stdout.readlines():
        print i.rstrip('\n')
    return p.wait()

def pyf2c(target, source, env):
    import numpy.f2py
    import shutil

    # We need filenames from source/target for path handling
    target_file_names = [str(i) for i in target]
    source_file_names = [str(i) for i in source]

    # Get source files necessary for f2py generated modules
    d = os.path.dirname(numpy.f2py.__file__)
    source_c = pjoin(d, 'src', FOBJECT_FILE)

    # Copy source files for f2py generated modules in the build dir
    build_dir = pdirname(target_file_names[0])

    # XXX: blah
    if build_dir == '':
        build_dir = '.'

    try:
        cpi = mangle_fortranobject(target_file_names[0], FOBJECT_FILE)
        shutil.copy(source_c, pjoin(build_dir, cpi))
    except IOError, e:
        msg = "Error while copying fortran source files (error was %s)" % str(e)
        raise IOError(msg)

    basename = os.path.basename(str(target[0]).split('module')[0])

    # XXX: handle F2PYOPTIONS being a string instead of a list
    if is_pyf(source_file_names[0]):
        # XXX: scons has a way to force buidler to only use one source file
        if len(source_file_names) > 1:
            raise NotImplementedError("FIXME: multiple source files")

        wrapper = pjoin(build_dir, FWRAP_TEMPLATE % basename)

        cmd = env['F2PYOPTIONS'] + \
              [source_file_names[0], '--build-dir', build_dir]
        st = f2py_cmd_exec(cmd)

        if not os.path.exists(wrapper):
            f = open(wrapper, 'w')
            f.close()
    else:
        cmd = env['F2PYOPTIONS'] + source_file_names + \
              ['--build-dir', build_dir]
        # fortran files, we need to give the module name
        cmd.extend(['--lower', '-m', basename])
        st = f2py_cmd_exec(cmd)

    return 0


def generate(env):
    """Add Builders and construction variables for swig to an Environment."""
    import numpy.f2py
    d = pdirname(numpy.f2py.__file__)

    f2pyac = SCons.Action.Action(pyf2c, '$F2PYCOMSTR')

    c_file, cxx_file = SCons.Tool.createCFileBuilders(env)

    c_file.add_action('.pyf', SCons.Action.Action(f2pyac))
    c_file.add_emitter('.pyf', F2pyEmitter)

    env['F2PYOPTIONS']      = SCons.Util.CLVar('--quiet')
    env['F2PYBUILDDIR']     = ''
    env['F2PYINCLUDEDIR']   = pjoin(d, 'src')

    if not (env.has_key("F2PY_NOT_ADD_INCLUDEDIR") and env["F2PY_NOT_ADD_INCLUDEDIR"]):
        env.Prepend(CPPPATH = env["F2PYINCLUDEDIR"])

    if not env.has_key('F2PYCOMSTR'):
        env['F2PYCOMSTR']       = "f2py: generating $TARGET from $SOURCE"

    # XXX: adding a scanner using c_file.add_scanner does not work...
    expr = '(<)include_file=(\S+)>'
    scanner = SCons.Scanner.ClassicCPP("F2PYScan", ".pyf", "F2PYPATH", expr)
    env.Append(SCANNERS = scanner)

    env['BUILDERS']['F2py'] = SCons.Builder.Builder(action = f2pyac,
            emitter = [F2pyEmitter])

def exists(env):
    try:
        import numpy.f2py
        st = 1
    except Exception, e:
        #print "Warning : f2py tool not found, error was %s" % e
        st = 0

    return st

