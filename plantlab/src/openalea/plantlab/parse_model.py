# -*- python -*-
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2014 INRIA - CIRAD - INRA
#
#       File author(s): Julien Coste <julien.coste@inria.fr>
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


def parse_lpy(string):
    """
    Take a lpy string_file, parse it and return only the docstring of the file.

    :param string: string representation of lpy file
    :return: docstring of the file if exists (must be a multiline docstring!). If not found, return None.

    :use:
        >>> f = open(lpyfilename, "r")
        >>> lpystring = f.read()
        >>> f.close()
        >>>
        >>> docstring = parse_lpy(lpystring)
        >>>
        >>> from openalea.oalab.model.parse import parse_doc
        >>> if docstring is not None:
        >>>     model, inputs, outputs = parse_doc(docstring)
        >>>     print "model : ", model
        >>>     print "inputs : ", inputs
        >>>     print "outputs : ", outputs
    """
    # TODO: need a code review
    begin = None
    begintype = None
    doclines = string.splitlines()
    i = 0
    for docline in doclines:
        i += 1
        if docline == '"""':
            begin = i
            begintype = '"""'
            break
        elif docline == "'''":
            begin = 1
            begintype = "'''"
            break
        elif docline == '"""':
            begin = 2
            begintype = '"""'
            break
        elif docline == "'''":
            begin = 2
            begintype = "'''"
            break

    if begin is not None:
        end = begin - 1
        for docline in doclines[begin:]:
            end += 1
            if docline == begintype:
                docstrings = doclines[begin:end]
                return "\n".join(docstrings)
    return None

