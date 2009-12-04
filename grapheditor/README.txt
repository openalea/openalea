====== GraphEditor =====

**Authors** : Daniel Barbeau

**Institutes** : INRIA / CIRAD 

**Status** : Python package 

**License** : Cecill-C

**URL** : http://openalea.gforge.inria.fr

===== About =====

=== Description ===

The grapheditor package is an attempt to provide a general framework for graph visualisation
and editing. The goal is to generalise as much as can be of the visualisation and interaction
process so the users of this package can more easily define how a tree or a dataflow should be
viewed and interacted with.
To acheive this, we make more heavy use of the observer/observed system from openalea.core and
define contracts that need to be satisfied by both the observers and the observed so that they
collaborate nearly out-of-the-box.
We also create a mapping between graph types and viewing strategies. If the graph is a dataflow
we will choose the dataflow viewing strategy.
  
=== Content ===

The grapheditor package contains :

  * generic graph observer and interaction classes and interfaces. 
  * a canvas for Qt
  * an implementation of a dataflow viewer.

=== Requirements ===

* OpenAlea.Core


=== Using GraphEditor ===

GraphEditor is a framework. It ships with some graph viewing strategies
but if they don't satisfy your needs you can have a look at them or
implement your own. Have also a look at the user and reference guides.





