#!/bin/sh

# Version: $Id$
#
#

# Commentary:
#
#

# Change Log:
#
#

# Code:

cd core/test
nosetests --exclude="(test_package.py|test_packagemanager.py)"
cd ../../oalab/test
nosetests
cd ../../grapheditor/test
nosetests
cd ../../visualea/test
nosetests
cd -

#
# travis-tests.sh ends here
