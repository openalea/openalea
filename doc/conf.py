import os,sys

# read sphinx conf.py file
from openalea.misc.sphinx_configuration import *
from openalea.misc.sphinx_tools import sphinx_check_version
from openalea.deploy.metainfo import read_metainfo

sphinx_check_version()                      # check that sphinx version is recent
version = '0.8'
project = 'openalea.doc'    # this variable is used by the layout.html do not change it or no main page will be linked 
release = '0.8.0'
authors = 'Openalea Consortium'

# by product that need to be updated:
latex_documents = [('contents', 'main.tex', project + ' documentation', authors, 'manual')]


