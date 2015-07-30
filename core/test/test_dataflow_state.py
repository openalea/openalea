from nose.tools import assert_raises

from openalea.core.dataflow import DataFlow, PortError
from openalea.core.dataflow_state import DataflowState
from openalea.core.node import Node


def test_dataflow_state_init():
    df = DataFlow()
    vid1 = df.add_vertex()
    df.add_in_port(vid1, "in")
    pid11 = df.add_out_port(vid1, "out")
    vid2 = df.add_vertex()
    pid21 = df.add_out_port(vid2, "out")

    vid3 = df.add_vertex()
    pid31 = df.add_in_port(vid3, "in1")
    pid32 = df.add_in_port(vid3, "in2")
    pid33 = df.add_out_port(vid3, "res")

    vid4 = df.add_vertex()
    pid41 = df.add_in_port(vid4, "in")

    df.connect(pid11, pid31)
    df.connect(pid21, pid32)
    df.connect(pid33, pid41)

    dfs = DataflowState(df)
    dfs.clear()

    assert len(dfs._state) == 0


def test_dataflow_state_reinit():
    df = DataFlow()
    vid1 = df.add_vertex()
    pid10 = df.add_in_port(vid1, "in")
    pid11 = df.add_out_port(vid1, "out")
    vid2 = df.add_vertex()
    pid21 = df.add_out_port(vid2, "out")

    vid3 = df.add_vertex()
    pid31 = df.add_in_port(vid3, "in1")
    pid32 = df.add_in_port(vid3, "in2")
    pid33 = df.add_out_port(vid3, "res")

    vid4 = df.add_vertex()
    pid41 = df.add_in_port(vid4, "in")

    df.connect(pid11, pid31)
    df.connect(pid21, pid32)
    df.connect(pid33, pid41)

    dfs = DataflowState(df)

    dfs.set_data(pid10, 0)

    for i, pid in enumerate([pid11, pid21, pid33]):
        dfs.set_data(pid, i)

    dfs.reinit()
    assert dfs.is_ready_for_evaluation()
    for pid in (pid11, pid21, pid33):
        assert_raises(KeyError, lambda: dfs.get_data(pid))


def test_dataflow_state_is_ready_for_evaluation():
    df = DataFlow()
    vid1 = df.add_vertex()
    pid10 = df.add_in_port(vid1, "in")
    pid11 = df.add_out_port(vid1, "out")
    vid2 = df.add_vertex()
    pid21 = df.add_out_port(vid2, "out")

    vid3 = df.add_vertex()
    pid31 = df.add_in_port(vid3, "in1")
    pid32 = df.add_in_port(vid3, "in2")
    pid33 = df.add_out_port(vid3, "res")

    vid4 = df.add_vertex()
    pid41 = df.add_in_port(vid4, "in")

    df.connect(pid11, pid31)
    df.connect(pid21, pid32)
    df.connect(pid33, pid41)

    dfs = DataflowState(df)

    assert not dfs.is_ready_for_evaluation()

    dfs.set_data(pid10, 0)

    assert dfs.is_ready_for_evaluation()

    dfs.clear()
    for i, pid in enumerate([pid11, pid21, pid33]):
        dfs.set_data(pid, i)
        assert not dfs.is_ready_for_evaluation()


def test_dataflow_state_is_valid():
    df = DataFlow()
    vid1 = df.add_vertex()
    pid10 = df.add_in_port(vid1, "in")
    pid11 = df.add_out_port(vid1, "out")
    vid2 = df.add_vertex()
    pid21 = df.add_out_port(vid2, "out")

    vid3 = df.add_vertex()
    pid31 = df.add_in_port(vid3, "in1")
    pid32 = df.add_in_port(vid3, "in2")
    pid33 = df.add_out_port(vid3, "res")

    vid4 = df.add_vertex()
    pid41 = df.add_in_port(vid4, "in")

    df.connect(pid11, pid31)
    df.connect(pid21, pid32)
    df.connect(pid33, pid41)

    dfs = DataflowState(df)

    assert not dfs.is_valid()

    dfs.set_data(pid10, 0)

    assert not dfs.is_valid()

    dfs.clear()
    for i, pid in enumerate([pid11, pid21, pid33]):
        dfs.set_data(pid, i)
        assert not dfs.is_valid()

    dfs.set_data(pid10, 'a')
    assert dfs.is_valid()


def test_dataflow_state_get_data():
    df = DataFlow()
    vid1 = df.add_vertex()
    pid10 = df.add_in_port(vid1, "in")
    pid11 = df.add_out_port(vid1, "out")
    vid2 = df.add_vertex()
    pid21 = df.add_out_port(vid2, "out")
    vid5 = df.add_vertex()
    pid51 = df.add_out_port(vid5, "out")

    vid3 = df.add_vertex()
    pid31 = df.add_in_port(vid3, "in1")
    pid32 = df.add_in_port(vid3, "in2")
    pid33 = df.add_out_port(vid3, "res")

    vid4 = df.add_vertex()
    pid41 = df.add_in_port(vid4, "in")

    df.connect(pid11, pid31)
    df.connect(pid21, pid32)
    df.connect(pid33, pid41)
    df.connect(pid51, pid32)

    dfs = DataflowState(df)

    for pid in df.ports():
        assert_raises(KeyError, lambda: dfs.get_data(pid))

    for i, pid in enumerate([pid11, pid21, pid33, pid51]):
        dfs.set_data(pid, i)

    assert_raises(KeyError, lambda: dfs.get_data(pid10))

    dfs.set_data(pid10, 'a')
    assert dfs.get_data(pid10) == 'a'

    for i, pid in enumerate([pid11, pid21, pid33, pid51]):
        assert dfs.get_data(pid) == i

    assert dfs.get_data(pid31) == 0
    assert tuple(dfs.get_data(pid32)) == (1, 3)
    assert dfs.get_data(pid41) == 2

    n2 = Node()
    df.set_actor(vid2, n2)

    assert tuple(dfs.get_data(pid32)) == (1, 3)

    n5 = Node()
    df.set_actor(vid5, n5)
    assert tuple(dfs.get_data(pid32)) == (1, 3)

    n2.get_ad_hoc_dict().set_metadata('position', [10, 0])
    n5.get_ad_hoc_dict().set_metadata('position', [0, 0])
    assert tuple(dfs.get_data(pid32)) == (3, 1)
