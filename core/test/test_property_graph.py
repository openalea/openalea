
__license__ = "Cecill-C"
__revision__ = " $Id$ "

# Test node module
from openalea.core.graph.property_graph import PropertyGraph


def test_propertygraph():
    """Test property graph"""
    g = PropertyGraph()
    vid1 = g.add_vertex()
    vid2 = g.add_vertex()
    eid = g.add_edge((vid1, vid2))

    g.add_vertex_property("vtest")
    assert len(list(g.vertex_property_names()))==1
    assert "vtest" in list(g.vertex_property_names())
    assert len(g.vertex_property("vtest"))==0

    g.add_edge_property("etest")
    g.add_edge_property(1)
    assert len(list(g.edge_property_names()))==2
    assert "etest" in list(g.edge_property_names())
    assert 1 in list(g.edge_property_names())
    assert len(g.edge_property("etest"))==0
    assert len(g.edge_property(1))==0

    prop=g.vertex_property("vtest")
    prop[vid1]="toto"
    assert vid1 in g.vertex_property("vtest")
    assert vid2 not in g.vertex_property("vtest")
    assert g.vertex_property("vtest")[vid1]=="toto"

    prop=g.edge_property(1)
    prop[eid]=10.
    assert eid in g.edge_property(1)
    assert g.edge_property(1)[eid]==10.

    gb=PropertyGraph(g)
    assert "vtest" in list(gb.vertex_property_names())
    assert "etest" in list(gb.edge_property_names())
    assert 1 in list(gb.edge_property_names())
    assert vid1 in gb.vertex_property("vtest")
    assert vid2 not in gb.vertex_property("vtest")
    assert gb.vertex_property("vtest")[vid1]=="toto"

    gb.remove_edge(eid)
    assert "etest" in list(gb.edge_property_names())
    assert 1 in list(gb.edge_property_names())
    assert len(gb.edge_property("etest"))==0
    assert len(gb.edge_property(1))==0

    gb=PropertyGraph(g)
    gb.remove_vertex(vid2)
    assert "vtest" in list(gb.vertex_property_names())
    assert vid1 in gb.vertex_property("vtest")
    assert vid2 not in gb.vertex_property("vtest")
    assert gb.vertex_property("vtest")[vid1]=="toto"
    assert len(gb.edge_property(1))==0

    gb=PropertyGraph(g)
    g.remove_vertex_property("vtest")
    assert "vtest" not in list(g.vertex_property_names())
    g.remove_edge_property(1)
    assert 1 not in list(g.edge_property_names())

    g.edge_property("etest")[eid]="a"
    g.add_vertex_property("vtest")
    g.vertex_property("vtest")[vid1]=12
    g.extend(gb)
    assert "vtest" in list(g.vertex_property_names())
    assert "etest" in list(g.edge_property_names())
    assert 1 in list(g.edge_property_names())

    assert len(g.vertex_property("vtest"))==2
    assert len(g.edge_property("etest"))==1
    assert len(g.edge_property(1))==1
