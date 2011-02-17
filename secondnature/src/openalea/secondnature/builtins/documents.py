# -*- python -*-
#
#       OpenAlea.Secondnature
#
#       Copyright 2006-2011 INRIA - CIRAD - INRA
#
#       File author(s): Daniel Barbeau <daniel.barbeau@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################


from openalea.secondnature.extendable_objects import Document


#LOGGER
from openalea.core.logger import LoggerOffice
model = LoggerOffice().get_handler("qt")
logger = Document("Logger", "Openalea", "Logger", model, category="system")


def get_builtins():
    return [logger]
