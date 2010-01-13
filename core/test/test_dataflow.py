"""Dataflow Tests"""

__license__ = "Cecill-C"
__revision__ = " $Id$ "

from openalea.core.dataflow import DataFlow, PortError


def test_dataflow():
    """ test dataflow"""
    df=DataFlow()
    vid1=df.add_vertex()
    pid11=df.add_out_port(vid1, "out")
    vid2=df.add_vertex()
    pid21=df.add_out_port(vid2, "out")

    vid3=df.add_vertex()
    pid31=df.add_in_port(vid3, "in1")
    pid32=df.add_in_port(vid3, "in2")
    pid33=df.add_out_port(vid3, "res")

    vid4=df.add_vertex()
    pid41=df.add_in_port(vid4, "in")

    eid1=df.connect(pid11, pid31)
    eid2=df.connect(pid21, pid32)
    eid3=df.connect(pid33, pid41)

    assert df.source_port(eid1)==pid11
    assert df.target_port(eid2)==pid32
    assert set(df.out_ports(vid1))==set((pid11, ))
    assert set(df.in_ports(vid3))==set((pid31, pid32))
    assert set(df.ports(vid3))==set((pid31, pid32, pid33))
    assert df.is_in_port(pid31)
    assert df.is_out_port(pid11)
    assert df.vertex(pid11)==vid1
    assert set(df.connected_ports(pid11))==set((pid31, ))
    assert set(df.connected_edges(pid21))==set((eid2, ))
    assert df.out_port(vid1, "out")==pid11
    assert df.in_port(vid3, "in1")==pid31

    test=False
    try:
        dummy=df.connect(pid11, pid33)
    except PortError:
        test=True
    assert test


    df.remove_port(pid33)
    assert set(df.connected_ports(pid41))==set()
    assert set(df.out_edges(vid3))==set()
    test=False
    try:
        dummy=df.port(pid33)
    except PortError:
        test=True
    assert test
