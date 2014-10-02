
from docutils.nodes import Inline, TextElement
from docutils.parsers.rst.roles import register_generic_role

class checkbox(Inline, TextElement): pass

def visit_input_html(self, node):
    self.body.append(self.starttag(node, 'input', type='checkbox', value='true'))
def depart_input_html(self, node):
    self.body.append('</input>')

def setup(app):
    """Install the plugin.

    :param app: Sphinx application context.
    """
    app.add_node(checkbox, html=(visit_input_html, depart_input_html))
    register_generic_role('checkbox', checkbox)
