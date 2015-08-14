
from openalea.oalab.service.drag_and_drop import encode, decode, reload_drag_and_drop_plugins
from openalea.oalab.testing.mimedata import SampleCustomData


def test_codec():
    mimetype = 'custom/data'
    initial = SampleCustomData(1, 'b')
    mimetype, raw_data = encode(initial, mimetype_in=mimetype, mimetype_out=mimetype)
    final, kwds = decode(raw_data, mimetype_in=mimetype, mimetype_out=mimetype)

    assert initial.num == final.num
    assert initial.letter == final.letter
