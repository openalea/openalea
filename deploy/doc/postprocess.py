""" clean up tool

The reST files are automatically generated using sphinx_tools.

However, there are known issus which require cleaning.

This code is intended at cleaning these issues until a neat 
solution is found.

:known problem:

- in ./deploy/openalea_deploy_binary_deps_ref.rst, the automodule 
includes the module binary_deps.py but there is only one
function inside this module. The automodule fails. To prevent this failure
switch the automodule to autofunction and remove all the fields below 
'.. autofunction::' that are not required anymore.
"""
import os

print 'Fixing the binary_deps_ref.rst case.'
text = open('./deploy/openalea_deploy_binary_deps_ref.rst','r').read()
if text.find('.. automodule::')!=-1:

    foutput = open('./deploy/openalea_deploy_binary_deps_ref.rst','w')
    foutput.write(text.split(".. automodule::")[0])
    text = text.split(".. automodule::")[1]
    foutput.write('.. autofunction:: ' + text.split('\n')[0])
    foutput.close()
else:
    print 'Seems to be done already.'
    
print 'Try python setup.py build_sphinx now.'

