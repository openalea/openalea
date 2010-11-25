from openalea.core import logger

def test1():
    log = logger.get_logger('test.logger')
    log.info('-> test1')
    for i in range(10):
      log.debug('    i= %d'%i)
    log.info('<- test1')

def test2():
    debug = logger.debug
    info = logger.info
    info('-> test1')
    for i in range(10):
      debug('    i= %d'%i)
    info('<- test1')


