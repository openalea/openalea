def test_has_ipython():
	from openalea.vpltk.check.ipython import has_ipython
	result = has_ipython()
	assert result is True
	
def test_has_pygments():
	from openalea.vpltk.check.ipython_deps import has_pygments
	result = has_pygments()
	assert result is True
	
def test_has_zmq():
	from openalea.vpltk.check.ipython_deps import has_zmq
	result = has_zmq()
	assert result is True