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
from pygments.lexer import inherit, include
from pygments.token import Text, Keyword, Name, Generic

class LPyLexer(PythonLexer):
    """
    LPy lexer extend Python lexer for syntax coloring with Pygments.
    """
    name = 'LPy'
    aliases = ['lpy','Lpy','LPy','l-py','L-py','L-Py',]
    filenames = ['*.lpy']
    mimetypes = ['text/x-python', 'application/x-python']
    
    def module_callback(lexer, match):
        """
        Permit to detect and stock words after special words "axiom" and "module".
        This words are then colourized like other keywords.
        """
        possible_words = match.group().split(" ")
        for possible_word in possible_words:
            w = possible_word.split("(")[0]
            if w is not u"":
                # Stock "lpy modules"
                lexer.lpy_modules.append(w)
        # Colourize words after "axiom" and "module" in the same line.
        yield match.start(), Keyword, match.group()
    
    tokens = {
        'root':[
          include('lpykeywords'), 
          inherit #inherit from PythonLexer
          ],
        'lpykeywords': [
            (r'(^Axiom|^module)', Generic.Subheading, 'module'),
            (r'(^derivation length|-->|-static->|decomposition|'
             r'^production|produce|homomorphism|^interpretation|group|'
             r'^endlsystem|endgroup|maximum depth|nproduce|nsproduce|'
             r'makestring|consider|ignore|forward|backward|isForward|'
             r'StartEach|EndEach|Start|End|getGroup|useGroup|getIterationNb|'
             r'module|@static|lpyimport)', Generic.Subheading),
            ],
        'module':[
            (r'(\w*)(\(.*\))',module_callback),
            (r'( )(\w*)( |$)',module_callback),
            (r'(:| )',Text),
        ]
        }
        
    def __init__(self, **options):
        super(LPyLexer, self).__init__(**options)
        # Add list to stock "lpy modules"
        self.lpy_modules = list()
     
    def get_tokens_unprocessed(self, text):
        for index, token, value in PythonLexer.get_tokens_unprocessed(self, text):
            if token is Name and value in self.lpy_modules:
               # Colourize previously detected modules
               yield index, Keyword, value
            else:
               yield index, token, value