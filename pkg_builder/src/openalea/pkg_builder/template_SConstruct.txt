# -*-python-*-

import os
from openalea.sconsx import config, environ


ALEASolution = config.ALEASolution

pj = os.path.join

SConsignFile()

options = Variables(['../options.py', 'options.py'], ARGUMENTS)
tools = ['']

env = ALEASolution(options, tools)

# Set build directory
prefix = env['build_prefix']

# Build stage
SConscript(pj(prefix,"src/cpp/SConscript"), exports="env")
SConscript(pj(prefix,"src/wrapper/SConscript"), exports="env")

Default("build")
