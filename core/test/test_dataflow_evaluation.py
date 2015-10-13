from nose.tools import assert_raises
import operator

from openalea.core.dataflow import DataFlow
from openalea.core.dataflow_state import DataflowState
from openalea.core.dataflow_evaluation import (AbstractEvaluation,
                                               BruteEvaluation)
from openalea.core.node import Node, FuncNode


def print_func(*args):
    print args


def fixed_function():
    return 5


def double_fixed_function():
    return 5, 5


def get_dataflow():
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
    pid42 = df.add_out_port(vid4, "out")

    df.connect(pid11, pid31)
    df.connect(pid21, pid32)
    df.connect(pid33, pid41)

    df.set_actor(vid1, FuncNode({}, {}, int))
    df.set_actor(vid2, FuncNode({}, {}, fixed_function))
    df.set_actor(vid3, FuncNode({}, {}, operator.add))
    df.set_actor(vid4, FuncNode({}, {}, print_func))

    return df, (pid10, pid42)


def test_dataflow_evaluation_init():
    df, (pid_in, pid_out) = get_dataflow()
    algo = AbstractEvaluation(df)
    assert_raises(NotImplementedError, lambda: algo.eval(0, None))

    algo = BruteEvaluation(df)
    algo.clear()

    assert len(algo._evaluated) == 0


def test_dataflow_evaluation_eval_init():
    df, (pid_in, pid_out) = get_dataflow()
    algo = BruteEvaluation(df)

    env = 0
    dfs = DataflowState(df)
    assert_raises(UserWarning, lambda: algo.eval(env, dfs))


def test_dataflow_evaluation_eval():
    df, (pid_in, pid_out) = get_dataflow()
    algo = BruteEvaluation(df)

    env = 0
    dfs = DataflowState(df)
    dfs.set_data(pid_in, 1)

    assert not dfs.is_valid()
    algo.eval(env, dfs, df.vertex(pid_out))
    assert dfs.is_valid()


def test_dataflow_evaluation_eval_no_vid():
    df, (pid_in, pid_out) = get_dataflow()
    algo = BruteEvaluation(df)

    env = 0
    dfs = DataflowState(df)
    dfs.set_data(pid_in, 1)

    assert not dfs.is_valid()
    algo.eval(env, dfs)
    assert dfs.is_valid()


def test_dataflow_evaluation_eval_no_vid2():
    df = DataFlow()
    vid0 = df.add_vertex()
    pid0 = df.add_in_port(vid0, "in")
    df.add_out_port(vid0, "out")
    vid1 = df.add_vertex()
    pid1 = df.add_in_port(vid1, "in")
    df.add_out_port(vid1, "out")

    df.set_actor(vid0, FuncNode({}, {}, int))
    df.set_actor(vid1, FuncNode({}, {}, int))

    dfs = DataflowState(df)
    env = 0
    algo = BruteEvaluation(df)

    dfs.set_data(pid0, 0)
    dfs.set_data(pid1, 1)

    assert not dfs.is_valid()
    algo.eval(env, dfs)
    assert dfs.is_valid()


def test_dataflow_evaluation_single_input_single_output():
    df = DataFlow()
    vid = df.add_vertex()
    pid0 = df.add_in_port(vid, "in")
    pid1 = df.add_in_port(vid, "in")
    pid2 = df.add_out_port(vid, "out")

    df.set_actor(vid, FuncNode({}, {}, operator.add))

    dfs = DataflowState(df)
    env = 0
    algo = BruteEvaluation(df)

    dfs.set_data(pid0, 1)
    dfs.set_data(pid1, 2)
    algo.eval(env, dfs, vid)

    assert dfs.get_data(pid0) == 1
    assert dfs.get_data(pid1) == 2
    assert dfs.get_data(pid2) == 3


def test_dataflow_evaluation_single_input_no_output():
    df = DataFlow()
    vid = df.add_vertex()
    pid0 = df.add_in_port(vid, "in")

    df.set_actor(vid, FuncNode({}, {}, print_func))

    dfs = DataflowState(df)
    env = 0
    algo = BruteEvaluation(df)

    dfs.set_data(pid0, 1)
    algo.eval(env, dfs, vid)

    assert dfs.get_data(pid0) == 1

    df.set_actor(vid, FuncNode({}, {}, int))
    dfs.reinit()
    algo.clear()

    assert_raises(UserWarning, lambda: algo.eval(env, dfs, vid))


def test_dataflow_evaluation_no_input_two_outputs():
    df = DataFlow()
    vid = df.add_vertex()
    pid0 = df.add_out_port(vid, "out1")

    df.set_actor(vid, FuncNode({}, {}, double_fixed_function))

    dfs = DataflowState(df)
    env = 0
    algo = BruteEvaluation(df)

    algo.eval(env, dfs, vid)

    assert tuple(dfs.get_data(pid0)) == (5, 5)

    algo.clear()
    dfs.reinit()
    pid1 = df.add_out_port(vid, "out2")
    algo.eval(env, dfs, vid)
    assert dfs.get_data(pid0) == 5
    assert dfs.get_data(pid1) == 5

    algo.clear()
    dfs.reinit()
    pid2 = df.add_out_port(vid, "out3")
    assert_raises(UserWarning, lambda: algo.eval(env, dfs, vid))
