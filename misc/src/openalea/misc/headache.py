"""Script to automatically generate headers in files of the openalea and vplants modules.
"""

import os, subprocess
from types import ModuleType
from collections import Sequence
from tempfile import NamedTemporaryFile
from ConfigParser import ConfigParser
from datetime import datetime
from exceptions import StandardError
from path import Path

class MetainfoError(StandardError):
  """Class for exceptions raised during metainfo extraction
  """

def generate_headers(mod, patterns=['*.py', '*.h', '*.c*'], tab='  '):
  """Function generating headers in files of an openalea and vplants module

  Headers are

  :Parameters:
   - `mod` (:class:`type.ModuleType`) - The openalea or vplants module in which files will be considered.
   - `patterns` ([:class:`basetring`]) - The pattern for used to limit the header inclusion to files with names that match one of the patterns.
   - `tab` (:class:`basestring`) - The tabulation to use in the header.

  .. seealso:: :func:`fnmatch` for elements of `patterns`
  """
  if not isinstance(patterns, Sequence):
      raise TypeError('`patterns` parameter')
  if not all([isinstance(pattern, basestring) for pattern in patterns]):
      raise ValueError('`patterns` parameter')
  if not isinstance(tab, basestring):
    raise TypeError('`tab` parameter')
  if not isinstance(mod, ModuleType):
    raise TypeError('`mod` parameter')
  rootpath = mod.__path__
  if isinstance(rootpath, Sequence):
    if len(rootpath) > 1:
      raise ValueError('`mod` parameter')
    rootpath = rootpath[0]
  if not isinstance(rootpath, basestring):
    raise ValueError('`mod` parameter')
  rootpath = Path(rootpath)

  while len(rootpath) > 0 and not str(rootpath.name) == 'src':
    rootpath = rootpath.parent
  rootpath = rootpath.parent
  configparser = ConfigParser()
  configparser.read(rootpath/'metainfo.ini')
  config = dict(configparser.items('metainfo'))

  headerhandler = NamedTemporaryFile(delete=False)
  try:
    headerhandler.file.write(tab+config['project']+'.'+config['package'])
    if not config['description'] == '':
      headerhandler.file.write(': '+config['description'])
    headerhandler.file.write('\n'+tab+'\n')
    headerhandler.file.write(tab+'Copyright 1995- '+str(datetime.now().year)+' Inria, Cirad, Inra')
    headerhandler.file.write('\n'+tab+'\n')
    config['authors'] = [i for i in config['authors'].split(', ') if not i == '']
    config['authors_email'] = [i for i in config['authors_email'].split(', ') if not i =='']
    if not len(config['authors']) == len(config['authors_email']):
      raise MetainfoError('`authors` and `authors_email` fields for `mod` parameter are not compatible')
    if len(config['authors']) > 1:
      headerhandler.file.write(tab+'File authors:\n'+tab*2+'* '+('\n'+tab*2+'* ').join([i+' <'+j+'>' if not j == '' else i for i, j in zip(config['authors'], config['authors_email'])]))
    else:
      headerhandler.file.write(tab+'File author: '+config['authors'].pop()+' <'+config['authors_email'].pop()+'>')
    headerhandler.write('\n'+tab+'\n')
    config['contributors'] = [i for i in config['contributors'].split(', ') if not i == '']
    config['contributors_email'] =  [i for i in config['contributors_email'].split(', ') if not i =='']
    if not len(config['contributors']) == len(config['contributors_email']):
      raise MetainfoError('`contributors` and `contributors_email` fields for `mod` parameter are not compatible')
    if len(config['contributors']) > 0:
      if len(config['contributors']) > 1:
        headerhandler.file.write(tab+'File contributors:\n'+tab*2+'* '+('\n'+tab*2+'* ').join([i+' <'+j+'>' if not j == '' else i for i, j in zip(config['contributors'], config['contributors_email'])]))
      else:
        headerhandler.file.write(tab+'File contributor: '+config['contributors'].pop())
      headerhandler.write('\n'+tab+'\n')
    headerhandler.file.write(tab+'Distributed under the '+config['license']+'Cecill-C License.\n')
    headerhandler.file.write(tab+'See accompanying file LICENSE.txt')
    if not config['license_url'] == '':
      headerhandler.file.write(' or copy at\n'+tab*2+config['license_url'])
    headerhandler.file.write('\n'+tab+'\n'+tab+'OpenAlea WebSite: ')
    headerhandler.file.write(config['url'])
  except:
    headerhandler.close()
    os.remove(headerhandler.name)
    raise
  else:
    headerhandler.close()

  confighandler = NamedTemporaryFile(delete=False)
  confighandler.file.write('| \".*\\\\.h\" -> frame open:\"/*\" line:\"*\" close:\"*/\"')
  confighandler.file.write('| \".*\\\\.hpp\" -> frame open:\"/*\" line:\"*\" close:\"*/\"')
  confighandler.file.write('| \".*\\\\.c\" -> frame open:\"/*\" line:\"*\" close:\"*/\"')
  confighandler.file.write('| \".*\\\\.cpp\" -> frame open:\"/*\" line:\"*\" close:\"*/\"')
  confighandler.file.write('| \".*\\\\.py\" -> frame open:\"#\" line:\"#\" close:\"#\"')
  confighandler.close()

  subprocess.call('headache -c '+confighandler.name+' -h '+headerhandler.name+' '+' '.join([file for file in (rootpath/'src').walkfiles() if any([file.fnmatch(pattern) for pattern in patterns])]), shell=True)

  os.remove(confighandler.name)
  os.remove(headerhandler.name)
