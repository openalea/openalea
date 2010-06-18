networkx GraphEditor strategy tutorial
######################################
This tutorial describes how to implement a new GraphEditor strategy.
GraphEditor is a system that implements low level mecanisms needed to
do editing of graphs and uses so called "strategies" to describe
specialised behaviours (drawing and editing) for a particuliar graph
implementation.

This means that to implement a Qt view of a graph you just need to subclass
two classes to implement how vertices and egdes behave in the Qt view + a
strategy class that maps a graph type with the vertex and edge class we just
talked about.

To create the strategy we suppose you are familiar with the graph structure
you want to represent and that you know a little bit about PyQt.

GraphEditor architecture summary
================================
GraphEditor is architectured in MVC, where the Model is the graph data
structure, the view is GraphEditor (extended by strategies) and the Controller is
the way the user will interact with the model.

A word about the View and the Controller concepts
-------------------------------------------------
The MVC pattern distinguishes these two concepts but in practice they
are often part of the same thing : the (G)UI. For example, a widget
can show an image and let you edit the image in the same area.
GraphEditor lets you do this (Controller and View mixed in the same widget)
but it is important to understand that the user interaction works like this :

1. the user interacts using the controller (part of the widget)
2. the controller then modifies the model
3. the model accepts the modifications (or not) and notifies its observers.
4. the view (part of the widget) updates accordingly to the notifications

From the model to the view
--------------------------
There are several ways to make the model talk to the views. Graphs are
a composition of vertices and edges. There are three logical classes there:

1. A Graph class
2. A Node class
3. An Edge class

These three classes may or may not exist in the implementation (*i.e.* graph class
only, or graph and node). But whatever the data structure, GraphEditor expects the
following observed-observer mapping:

* **Graph model** *is viewed by* **Graph observer**
* **Node model** *is viewed by* **Node observer**
* **Edge model** *is viewed by* **Edge observer**

This means that sometimes you have to build proxy observers.

The basic problem
=================
NetworkX doesn't provide any sort of callback system to allow us to insert *observed*
behaviours to the graph structure so we first need to wrap the graph
structure in order to emit basic signals.

As we will manipulate graphs, nodes and edges, we will create three
wrappers for these:
* A node will be seen as
