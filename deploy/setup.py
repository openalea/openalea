# -*- coding: utf-8 -*-
__revision__ = "$Id$"

# Install setuptools if necessary
try:
    from ez_setup import use_setuptools
    use_setuptools()
except:
    pass


from setuptools import setup, find_packages
from os.path import join as pj

try:
    from openalea.deploy.metainfo import read_metainfo
except:
    import sys
    sys.path.append('src/openalea/deploy')
    from metainfo import read_metainfo


metadata = read_metainfo('metainfo.ini', verbose=True)
for key,value in metadata.iteritems():
    exec("%s = '%s'" % (key, value))

keywords = ['setuptools', 'shared lib']

print project
print package

setup(
    # Metadata for PyPi
    name = name,
    version = version,
    author = authors,
    author_email = authors_email,
    description = description,
    license = license,
    keywords = keywords,
    url = url,

    namespace_packages = ["openalea"],
    packages = find_packages('src'),
    package_dir = { '' : 'src', },
    include_package_data = True,
    zip_safe = True,

    entry_points = {
              "distutils.setup_keywords": [
                 "lib_dirs = openalea.deploy.command:validate_bin_dirs",
                 "inc_dirs = openalea.deploy.command:validate_bin_dirs",
                 "bin_dirs = openalea.deploy.command:validate_bin_dirs",
                 "share_dirs = openalea.deploy.command:validate_share_dirs",
                 "cmake_scripts = openalea.deploy.command:validate_cmake_scripts",
                 "scons_scripts = openalea.deploy.command:validate_scons_scripts",
                 "pylint_packages = openalea.deploy.command:validate_pylint_packages",
                 "pylint_options = openalea.deploy.command:validate_pylint_options",
                 "scons_parameters = setuptools.dist:assert_string_list",
                 "create_namespaces = openalea.deploy.command:validate_create_namespaces",
                 "postinstall_scripts = openalea.deploy.command:validate_postinstall_scripts",
                 "add_plat_name = openalea.deploy.command:validate_add_plat_name",
                 ],

              "egg_info.writers": [
                 "lib_dirs.txt = openalea.deploy.command:write_keys_arg",
                 "inc_dirs.txt = openalea.deploy.command:write_keys_arg",
                 "bin_dirs.txt = openalea.deploy.command:write_keys_arg",
                 "postinstall_scripts.txt = setuptools.command.egg_info:write_arg",
                 ],

              "distutils.commands":[
                 "cmake = openalea.deploy.command:cmake",
                 "scons = openalea.deploy.command:scons",
                 "create_namespaces = openalea.deploy.command:create_namespaces",
                 "alea_install = openalea.deploy.command:alea_install",
                 "alea_upload = openalea.deploy.command:alea_upload",
                 "upload_sphinx = openalea.deploy.command:upload_sphinx",
                 "pylint = openalea.deploy.command:pylint",
                 "clean = openalea.deploy.command:clean",
                 "egg_upload = openalea.deploy.command:egg_upload",
                 "system_deploy = openalea.deploy.command:system_deploy",
                 ],

              "console_scripts": [
                 "alea_install = openalea.deploy.alea_install:main",
                # "alea_uninstall = openalea.deploy.alea_update:uninstall_egg",
                 "alea_config = openalea.deploy.alea_config:main",
                 "alea_clean = openalea.deploy.alea_update:clean_version",
                 "alea_update_all = openalea.deploy.alea_update:update_all",
                 ],

              },

    #install_requires = plat_requires,
)

