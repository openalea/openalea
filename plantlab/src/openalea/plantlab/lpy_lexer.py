# -*- coding: utf-8 -*-
"""
    pygments.lexers.lpy
    ~~~~~~~~~~~~~~~~~~~~~

    Lexers for L-Py language.

    :copyright: Copyright 2006-2013 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
    :authors: Julien COSTE, Guillaume BATY, Frederic BOUDON, Christophe PRADAL
    :homepage: http://openalea.gforge.inria.fr/wiki/doku.php?id=packages:vplants:lpy:main
"""

from pygments.lexers.agile import PythonLexer
from pygments.lexer import inherit, include
from pygments.token import Text, Keyword, Name, Generic

__all__ = ['LPyLexer']


class LPyLexer(PythonLexer):

    """
    Lexer for LPy language.
    """
    name = 'LPy'
    aliases = ['lpy', 'Lpy', 'LPy', 'l-py', 'L-py', 'L-Py', ]
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
        'root': [
            include('lpykeywords'),
            inherit
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
        'module': [
            (r'(\w*)(\(.*\))', module_callback),
            (r'( )(\w*)( |$)', module_callback),
            (r'(:| )', Text),
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
