# -*- coding: utf-8 -*-
# -*- python -*-
#
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2015 INRIA - CIRAD - INRA
#
#       File author(s): Guillaume Baty <guillaume.baty@inria.fr>
#
#       File contributor(s):
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################

from openalea.core.customexception import CustomException


class MimeConversionError(CustomException):
    title = u'Error: this data cannot be dropped here'
    message = u'%(data)s (%(mimetype_in)s) cannot be converted to %(mimetype_out)s'
    desc = "\n".join([
        "This error is raised because the data format dropped ",
        "is not supported by application or not completely supported",
        "System raised: \n%(exception)s"
    ])

    def _kargs(self):
        return dict(
            data=unicode(self._args[0].__class__.__name__),
            mimetype_in=self._args[1],
            mimetype_out=unicode(self._args[2]),
            exception=self._args[3]
        )
