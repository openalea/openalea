from openalea.misc import sphinx_configuration


def test_sphinx():
    assert sphinx_configuration.openalea
    extensions = [
        'sphinx.ext.autodoc',
        'sphinx.ext.autosummary',
        'sphinx.ext.coverage',
        'sphinx.ext.graphviz',
        'sphinx.ext.doctest',
        'sphinx.ext.intersphinx',
        'sphinx.ext.todo',
        'sphinx.ext.coverage',
        'sphinx.ext.pngmath',
        'sphinx.ext.ifconfig',
        'sphinx.ext.inheritance_diagram',
        'sphinx.ext.viewcode',
        'numpyext.only_directives',
        'matplotlib.sphinxext.plot_directive',
        'openalea.misc.dataflow_directive'
        ]

    for extension in extensions:
        assert extension in sphinx_configuration.extensions
