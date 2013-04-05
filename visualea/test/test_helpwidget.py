"""
Author: Thomas Cokelaer

"""
from openalea.visualea.helpwidget import *

text1 = "This is a simple docstring"
rst1 = """<div class="document">
<p>This is a simple docstring</p>
</div>
"""

text2 = "This is a simple docstring\n\n:param a: test"

rst2 = """<div class="document">
<p>This is a simple docstring</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field"><th class="field-name">param a:</th><td class="field-body">test</td>
</tr>
</tbody>
</table>
</div>
"""



def test_rst2alea():
    #if docutils and sphinx are install, the first assert must be true, otherwise, the second one must be true. 
    res = rst2alea(text1)
    assert (res == rst1) or (res == text1+"\n")
    res = rst2alea(text2)
    assert (res == rst2) or (res == text2.replace("\n", "<br />")+"\n"), res

from openalea.vpltk.qt import QtGui
app = QtGui.QApplication([])

def test_helpwidget():
    help = HelpWidget()
    help.set_rst(text1)
    assert text1 in help.toHtml()



test_rst2alea()
#test_helpwidget()

