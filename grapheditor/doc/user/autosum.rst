.. _grapheditor_reference:

Reference guide
###############
.. contents::

Class Inheritance diagram
=========================
.. .. inheritance-diagram:: #openalea.grapheditor.SimpleGraph.main
.. .. inheritance-diagram:: #openalea.grapheditor.SimpleGraph.custom_graph_model
.. .. inheritance-diagram:: #openalea.grapheditor.SimpleGraph.custom_graph_view
.. .. inheritance-diagram:: openalea.grapheditor.edgefactory
.. .. inheritance-diagram:: openalea.grapheditor.dataflowview.edge
.. .. inheritance-diagram:: openalea.grapheditor.dataflowview.anno
.. .. inheritance-diagram:: openalea.grapheditor.dataflowview.painting
.. .. inheritance-diagram:: openalea.grapheditor.dataflowview.adapter
.. .. inheritance-diagram:: openalea.grapheditor.dataflowview.vertex
.. .. inheritance-diagram:: openalea.grapheditor.baselisteners
.. .. inheritance-diagram:: openalea.grapheditor.qtutils
.. .. inheritance-diagram:: openalea.grapheditor.qtgraphview
.. .. inheritance-diagram:: openalea.grapheditor.interfaces

.. currentmodule:: openalea.grapheditor.edgefactory

:mod:`openalea.grapheditor.edgefactory` module
==============================================

Download the source file :download:`../../src/grapheditor/edgefactory.py`.


.. automodule:: openalea.grapheditor.edgefactory
    :members:
    :undoc-members:
    :inherited-members:
    :show-inheritance:
    :synopsis: synopsis to be provided

====> Interface testing IGraphViewStrategies : <class 'openalea.grapheditor.dataflowview.Strategy'>
	=> Testing for get_edge_widget_types...  true
	=> Testing for get_vertex_widget_types...  true
	=> Testing for get_graph_model_type...  true
	=> Testing for get_vertex_widget_factory...  true
	=> Testing for get_connector_types...  true
	=> Testing for get_graph_adapter_type...  true
	=> Testing for get_edge_widget_factory...  true
====> Interface testing IGraphAdapter : <class 'openalea.grapheditor.dataflowview.adapter.GraphAdapter'>
	=> Testing for remove_vertex...  true
	=> Testing for get_vertex_input...  true
	=> Testing for get_vertex...  true
	=> Testing for is_output...  true
	=> Testing for get_vertex_types...  true
	=> Testing for get_edge_types...  true
	=> Testing for get_vertex_output...  true
	=> Testing for get_vertex_outputs...  true
	=> Testing for is_input...  true
	=> Testing for get_vertex_inputs...  true
	=> Testing for remove_vertices...  true
	=> Testing for add_edge...  true
	=> Testing for add_vertex...  true
	=> Testing for remove_edge...  true
====> Interface testing IGraphViewElement : <class 'openalea.grapheditor.dataflowview.anno.GraphicalAnnotation'>
	=> Testing for remove_from_view...  true
	=> Testing for position_changed...  true
	=> Testing for notify...  true
	=> Testing for add_to_view...  true
====> Interface testing IGraphViewElement : <class 'openalea.grapheditor.dataflowview.vertex.GraphicalVertex'>
	=> Testing for remove_from_view...  true
	=> Testing for position_changed...  true
	=> Testing for notify...  true
	=> Testing for add_to_view...  true
====> Interface testing IGraphViewConnectable : <class 'openalea.grapheditor.dataflowview.vertex.GraphicalPort'>
	=> Testing for set_highlighted...  true
	=> Testing for get_scene_center...  true
====> Interface testing IGraphViewEdge : <class 'openalea.grapheditor.dataflowview.edge.GraphicalEdge'>
	=> Testing for update_line_source...  true
	=> Testing for update_line_destination...  true
	=> Testing for notify...  true
	=> Testing for remove_from_view...  true
	=> Testing for position_changed...  true
	=> Testing for notify...  true
	=> Testing for add_to_view...  true
====> Interface testing IGraphViewFloatingEdge : <class 'openalea.grapheditor.dataflowview.edge.FloatingEdge'>
	=> Testing for consolidate...  true
	=> Testing for get_connections...  true
	=> Testing for __init__...  true
	=> Testing for remove_from_view...  true
	=> Testing for position_changed...  true
	=> Testing for notify...  true
	=> Testing for add_to_view...  true

.. currentmodule:: openalea.grapheditor.dataflowview.edge

:mod:`openalea.grapheditor.dataflowview.edge` module
====================================================

Download the source file :download:`../../src/grapheditor/dataflowview/edge.py`.


.. automodule:: openalea.grapheditor.dataflowview.edge
    :members:
    :undoc-members:
    :inherited-members:
    :show-inheritance:
    :synopsis: synopsis to be provided


.. currentmodule:: openalea.grapheditor.dataflowview.anno

:mod:`openalea.grapheditor.dataflowview.anno` module
====================================================

Download the source file :download:`../../src/grapheditor/dataflowview/anno.py`.


.. automodule:: openalea.grapheditor.dataflowview.anno
    :members:
    :undoc-members:
    :inherited-members:
    :show-inheritance:
    :synopsis: synopsis to be provided


.. currentmodule:: openalea.grapheditor.dataflowview.painting

:mod:`openalea.grapheditor.dataflowview.painting` module
========================================================

Download the source file :download:`../../src/grapheditor/dataflowview/painting.py`.


.. automodule:: openalea.grapheditor.dataflowview.painting
    :members:
    :undoc-members:
    :inherited-members:
    :show-inheritance:
    :synopsis: Dataflow painting strategies


.. currentmodule:: openalea.grapheditor.dataflowview.adapter

:mod:`openalea.grapheditor.dataflowview.adapter` module
=======================================================

Download the source file :download:`../../src/grapheditor/dataflowview/adapter.py`.


.. automodule:: openalea.grapheditor.dataflowview.adapter
    :members:
    :undoc-members:
    :inherited-members:
    :show-inheritance:
    :synopsis: synopsis to be provided


.. currentmodule:: openalea.grapheditor.dataflowview.vertex

:mod:`openalea.grapheditor.dataflowview.vertex` module
======================================================

Download the source file :download:`../../src/grapheditor/dataflowview/vertex.py`.


.. automodule:: openalea.grapheditor.dataflowview.vertex
    :members:
    :undoc-members:
    :inherited-members:
    :show-inheritance:
    :synopsis: synopsis to be provided


.. currentmodule:: openalea.grapheditor.baselisteners

:mod:`openalea.grapheditor.baselisteners` module
================================================

Download the source file :download:`../../src/grapheditor/baselisteners.py`.


.. automodule:: openalea.grapheditor.baselisteners
    :members:
    :undoc-members:
    :inherited-members:
    :show-inheritance:
    :synopsis: Generic Graph Widget


.. currentmodule:: openalea.grapheditor.qtutils

:mod:`openalea.grapheditor.qtutils` module
==========================================

Download the source file :download:`../../src/grapheditor/qtutils.py`.


.. automodule:: openalea.grapheditor.qtutils
    :members:
    :undoc-members:
    :inherited-members:
    :show-inheritance:
    :synopsis: synopsis to be provided


.. currentmodule:: openalea.grapheditor.qtgraphview

:mod:`openalea.grapheditor.qtgraphview` module
==============================================

Download the source file :download:`../../src/grapheditor/qtgraphview.py`.


.. automodule:: openalea.grapheditor.qtgraphview
    :members:
    :undoc-members:
    :inherited-members:
    :show-inheritance:
    :synopsis: Generic Graph Widget


.. currentmodule:: openalea.grapheditor.interfaces

:mod:`openalea.grapheditor.interfaces` module
=============================================

Download the source file :download:`../../src/grapheditor/interfaces.py`.


.. automodule:: openalea.grapheditor.interfaces
    :members:
    :undoc-members:
    :inherited-members:
    :show-inheritance:
    :synopsis: Interfaces for the generic graph view module. The graph view ...

