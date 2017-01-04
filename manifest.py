import pysvn as ps
import numpy as np
import os
import subprocess as sp
import sys
import glob
import pkg_resources as pr
from openalea.deploy import metainfo
import re

DIRS = """
deploy
deploygui
core
scheduler
grapheditor
visualea
stdlib
sconsx
misc
pkg_builder
image
numpy
pylab
openalea_meta
""".split()

MANIFEST_FILENAME = 'MANIFEST.in'
GEN_SPEC_FILE = 'python setup.py bdist_rpm --spec-only'.split()
GEN_SOURCE_RPM = 'python setup.py bdist_rpm --source-only'.split()
INSTALL_SOURCE_RPM = 'rpm -i {0}'
GEN_BINARY_RPM = 'rpmbuild -ba --nocheck --nodeps {0}'

INSTALL_PATTERN = re.compile('%install(.*?)\n\n', re.DOTALL | re.MULTILINE)

NEW_INSTALL_PART = '''%install
python setup.py install --root=$RPM_BUILD_ROOT --install-lib=%{{python_sitearch}}
cd $RPM_BUILD_ROOT
{install_mkdir_part}{install_mkdir_doc_part}{install_mkdir_example_part}{install_mkdir_share_part}
cd  %{{_builddir}}/%{{name}}-%{{version}}
{install_cp_part}{install_cp_doc_part}{install_cp_example_part}{install_cp_share_part}
'''

FILES_PATTERN = re.compile('%files(.*?)\n\n', re.DOTALL | re.MULTILINE)

NEW_FILES_PART = '''%files
%defattr(-,root,root)
%{_defaultdocdir}/%{name}-%{version}/
%{python_sitearch}/
'''

install_mkdir_part = '''mkdir -p %{buildroot}%{_defaultdocdir}/%{name}-%{version}/'''
install_mkdir_doc_part = '\n' + install_mkdir_part + 'doc'
install_mkdir_example_part = '\n' + install_mkdir_part + 'example'
install_mkdir_share_part = '\n' + install_mkdir_part + 'share'

install_cp_part = '''cp -p *.txt %{buildroot}%{_defaultdocdir}/%{name}-%{version}/'''
install_cp_doc_part = '''\ncp -rp doc/ %{buildroot}%{_defaultdocdir}/%{name}-%{version}/doc'''
install_cp_example_part = '''\ncp -rp example/ %{buildroot}%{_defaultdocdir}/%{name}-%{version}/example'''
install_cp_share_part = '''\ncp -rp share/ %{buildroot}%{_defaultdocdir}/%{name}-%{version}/share'''

parts = {'install_mkdir_part': install_mkdir_part,
         'install_mkdir_doc_part': install_mkdir_doc_part,
         'install_mkdir_example_part': install_mkdir_example_part,
         'install_mkdir_share_part': install_mkdir_share_part,
         'install_cp_part': install_cp_part,
         'install_cp_doc_part': install_cp_doc_part,
         'install_cp_example_part': install_cp_example_part,
         'install_cp_share_part': install_cp_share_part}

curr_dir_bkp = os.getcwd()

client = ps.Client()

for dir_ in DIRS:
    print dir_
    os.chdir(dir_)
    entry_list = client.list('.', depth=ps.depth.infinity)

    filepaths = map(lambda svn_instance: svn_instance.data['path'],
                    np.array(entry_list)[:,0])

    filepaths.pop(0)

    filepaths = np.char.lstrip(filepaths, '/').tolist()

    if MANIFEST_FILENAME not in filepaths:
        filepaths.append(MANIFEST_FILENAME)

    manifest_lines = np.char.add('include ', filepaths)
    manifest_lines = np.char.add(manifest_lines, '\n')

    with open(MANIFEST_FILENAME, 'w') as f:
        f.writelines(manifest_lines)

    retcode = sp.call(GEN_SPEC_FILE)
    if retcode:
        sys.exit('Error generating the spec file of %s' % dir_)

    spec_filepath = glob.glob('./dist/*.spec')[0]

    import shutil
    shutil.copyfile(spec_filepath, spec_filepath + '.old')

    if os.path.isdir('doc') and os.listdir('doc'):
        parts['install_mkdir_doc_part'] = install_mkdir_doc_part
        parts['install_cp_doc_part'] = install_cp_doc_part
    else:
        parts['install_mkdir_doc_part'] = ''
        parts['install_cp_doc_part'] = ''

    if os.path.isdir('example') and os.listdir('example'):
        parts['install_mkdir_example_part'] = install_mkdir_example_part
        parts['install_cp_example_part'] = install_cp_example_part
    else:
        parts['install_mkdir_example_part'] = ''
        parts['install_cp_example_part'] = ''

    if os.path.isdir('share') and os.listdir('share'):
        parts['install_mkdir_share_part'] = install_mkdir_share_part
        parts['install_cp_share_part'] = install_cp_share_part
    else:
        parts['install_mkdir_share_part'] = ''
        parts['install_cp_share_part'] = ''

    new_install_part = NEW_INSTALL_PART.format(**parts)

    with open(spec_filepath, 'r') as spec_file:
        spec_str = spec_file.read() + '\n'

    spec_str = INSTALL_PATTERN.sub(new_install_part + '\n', spec_str)

    try:
        metadata = metainfo.read_metainfo('metainfo.ini', verbose=True)
        name = metadata['name']
    except IOError:
        name = 'OpenAlea.' + dir_

    try:
        entry_map = pr.get_entry_map(name)
    except:
        entry_map = {}

    if 'console_scripts' in entry_map:
        console_script_names = entry_map['console_scripts'].keys()
    else:
        console_script_names = []

    if 'gui_scripts' in entry_map:
        gui_script_names = entry_map['gui_scripts'].keys()
    else:
        gui_script_names = []

    new_files_part = NEW_FILES_PART

    for script_name in console_script_names + gui_script_names:
        new_files_part += '%{_bindir}/' + script_name + '\n'

    spec_str = FILES_PATTERN.sub(new_files_part + '\n', spec_str)

    with open(spec_filepath, 'w') as spec_file:
        spec_file.write(spec_str)

    retcode = sp.call(GEN_SOURCE_RPM)
    if retcode:
        sys.exit('Error generating the source rpm of %s' % dir_)

    source_rpm_filepath = glob.glob('./dist/*.src.rpm')[0]
    install_source_rpm = INSTALL_SOURCE_RPM.format(source_rpm_filepath)
    retcode = sp.call(install_source_rpm.split())
    if retcode:
        sys.exit('Error installing the source rpm of %s' % dir_)

    gen_binary_rpm = GEN_BINARY_RPM.format(spec_filepath)
    retcode = sp.call(gen_binary_rpm.split())
    if retcode:
        sys.exit('Error generating the binary rpm of %s' % dir_)

    os.chdir(curr_dir_bkp)
