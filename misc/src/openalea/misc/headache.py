"""Script to automatically generate headers in files of the openalea and vplants modules.
"""

import os
from types import ModuleType
from collections import Sequence
from tempfile import NamedTemporaryFile
from ConfigParser import ConfigParser
from datetime import datetime
from exceptions import StandardError

class MetainfoError(StandardError):
  """Class for exceptions raised during metainfo extraction
  """

def generate(mod, tab='  '):
  """Generate module file headers
  
  :Parameter:
    `mod` (:class:`type.ModuleType`) - The module in which files will be considered
  """
  if not isinstance(mod, ModuleType):
    raise TypeError('`mod` parameter')
  rootpath = mod.__path__
  if isinstance(rootpath, Sequence):
    if len(rootpath) > 1:
      raise ValueError('`mod` parameter')
    rootpath = rootpath[0]
  if not isinstance(rootpath, basestring):
    raise ValueError('`mod` parameter')
  rootpath = path(rootpath)
  
  while len(rootpath) > 0 and not str(rootpath.name) == 'src':
    rootpath = rootpath.parent
  rootpath = rootpath.parent
  from ConfigParser import ConfigParser
  configparser = ConfigParser()
  configparser.read(rootpath/'metainfo.ini')
  config = dict(configparser.items('metainfo'))
  
  headerhandler = NamedTemporaryFile(delete=False)
  try:
    headerhandler.file.write(tabs+config['project']+'.'+config['package'])
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
        headerhandler.file.write(tabs+'File contributor: '+config['contributors'].pop())
      headerhandler.write('\n'+tabs+'\n')
    headerhandler.file.write(tab+'Distributed under the '+config['license']+'Cecill-C License.\n')
    headerhandler.file.write(tab+'See accompanying file LICENSE.txt')
    if not config['license_url'] == '':
      headerhandler.file.write(' or copy at\n'+tabs+tabs+config['license_url'])
    headerfile.file.write('\n'+tab+'\n'+tab+'WebSite: ')
    headerfile.file.write(config['url'])
  except:
    headerhandle.close()
    os.remove(headerhandle.name)
    raise
  else:
    headerfile.close()

  confighandler = NamedTemporaryFile(delete=False)
  confighandler.file.write('| \".*\\\\.h\" -> frame open:\"/*\" line:\"*\" close:\"*/\"')
  confighandler.file.write('| \".*\\\\.hpp\" -> frame open:\"/*\" line:\"*\" close:\"*/\"')
  confighandler.file.write('| \".*\\\\.c\" -> frame open:\"/*\" line:\"*\" close:\"*/\"')
  confighandler.file.write('| \".*\\\\.cpp\" -> frame open:\"/*\" line:\"*\" close:\"*/\"')
  confighandler.file.write('| \".*\\\\.py\" -> frame open:\"#\" line:\"#\" close:\"#\"')
  confighandler.close()

  os.system('headache -c '+confighandler.name+' -h '+headerhandle.name+' '+' '.join(path(mod.__path__).parent.walkfiles(pattern='*.py|*.h*|*.c*')))

  os.remove(confighandler.name)
  os.remove(headerhandle.name)
