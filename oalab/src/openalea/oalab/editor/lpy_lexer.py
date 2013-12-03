# -*- python -*-
# 
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2013 INRIA - CIRAD - INRA
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
__revision__ = ""

from pygments.lexers.agile import PythonLexer
from pygments.token import Name, Generic

"""
:TODO: search from pygments.lexer.RegexLexer or ExtendedRegexLexer
Pygments repo: https://bitbucket.org/birkenfeld/pygments-main
Fork: https://bitbucket.org/jcoste/pygments-main
Regexp reader: http://www.regexper.com
"""

class LPyLexer(PythonLexer):
    """
    LPy lexer extend Python lexer for syntax coloring with Pygments
    """
    name = 'LPy'
    aliases = ['lpy','Lpy','LPy','l-py','L-py','L-Py',]
    filenames = ['*.lpy']
    
    LPY_KEYWORDS = ['Axiom','production','homomorphism','interpretation',
                            'decomposition','endlsystem','group','endgroup',
                            'derivation', 'length','maximum depth','produce','nproduce','nsproduce','makestring','-->',
                            'consider','ignore','forward','backward','isForward',
                            'Start','End','StartEach','EndEach','getGroup','useGroup','getIterationNb',
                            'module','-static->','@static','lpyimport']
    
    PROD_KEYWORDS = ['Axiom','module','produce','nproduce','nsproduce','makestring','-->','-static->','ignore','consider']

    DELIMITERS_KEYWORDS = '[](){}+-*/:<>='

    def get_tokens_unprocessed(self, text):
        for index, token, value in PythonLexer.get_tokens_unprocessed(self, text):
            #if token is Name and value in self.PROD_KEYWORDS:
            #    yield index, Generic.Heading, value
            if token is Name and value in self.LPY_KEYWORDS:
                yield index, Generic.Subheading, value
            else:
                yield index, token, value

'''
from pygments.lexer import RegexLexer
from pygments.lexers import PythonLexer
class LPyLexer(RegexLexer):
    name = 'LPy'
    aliases = ['lpy']
    filenames = ['*.lpy']

    tokens = {
        'root': [
            (r' .*\n', Text),
            (r'\+.*\n', Generic.Inserted),
            (r'-.*\n', Generic.Deleted),
            (r'@.*\n', Generic.Subheading),
            (r'Axiom.*\n', Generic.Heading),
            (r'=.*\n', Generic.Heading),
            (r'.*\n', Text),
        ]
    }'''
