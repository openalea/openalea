"""Tree Concept."""

from graphconcept import * #IGNORE:W0614


class RootedTreeConcept(VertexListGraphConcept):
    """Rooted Tree interface.
 
    depth(vid), depth() and sub_tree(vid) can be extenal algorithms.
    """

    def set_root(self, vtx_id):
        """ Set the tree root.

        :param vtx_id: The vertex identifier.
        """
        raise NotImplementedError

    def get_root(self): 
        """ Return the tree root.

        :returns: vertex identifier

        """
        raise NotImplementedError


    root = property( get_root, set_root )

    def parent(self, vtx_id):
        """
        Return the parent of `vtx_id`.

        :param vtx_id: The vertex identifier.
        :returns: vertex identifier
        """
        raise NotImplementedError

    def children(self, vtx_id):
        """
        Return a vertex iterator

        :param vtx_id: The vertex identifier.
        :returns: iter of vertex identifier
        """
        raise NotImplementedError


    def nb_children(self, vtx_id):
        """
        Return the number of children

        :param vtx_id: The vertex identifier.
        :rtype: int
        """
        raise NotImplementedError


    def siblings(self, vtx_id):
        """
        Return an iterator of vtx_id siblings.
        vtx_id is not include in siblings.

        :param vtx_id: The vertex identifier.
        :returns: iter of vertex identifier
        """
        raise NotImplementedError


    def nb_siblings(self, vtx_id):
        """
        Return the number of siblings

        :returns: int
        """
        raise NotImplementedError


    def is_leaf(self, vtx_id):
        """
        Test if `vtx_id` is a leaf.

        :returns: bool
        """
        raise NotImplementedError



class OrderedTreeConcept(RootedTreeConcept):
    """
    An ordered tree is a rooted tree where an order relation is 
    defined between chidren.
    """

    def first_child(self, vid): 
        """
        Return the first child of vid

        :param vid: The vertex identifier.
        :returns: vid
        """
        raise NotImplementedError


    def last_child(self, vid):
        """
        Return the last child of vid

        :param vid: The vertex identifier.
        :returns: vid
        """
        raise NotImplementedError


    def previous_sibling(self, vid):
        """
        Return previous sibling

        :param vid: The vertex identifier.

        :returns: vid
        """
        raise NotImplementedError


    def next_sibling(self, vid):
        """
        Return next sibling

        :param vid: The vertex identifier.

        :returns: vid
        """
        raise NotImplementedError


class MutableTreeConcept(RootedTreeConcept, MutableVertexGraphConcept):
    """
    A mutable rooted tree. 
    The substitute method is defined outside the interface.
    substitute(self,vid,tree)
    """

    def add_child(self, parent, child ): 
        """
        Add a child at the end of children

        :param parent: The parent identifier.
        :param child: The child identifier.
        """
        raise NotImplementedError


    def insert_sibling(self, vid1, vid2): 
        """
        Insert vid2 before vid1.

        :param vid1: a vertex identifier
        :param vid2: the vertex to insert
        """
        raise NotImplementedError 

    def insert_parent(self, vtx_id, parent_id): 
        """
        Insert parent_id between vtx_id and its actual parent.

        :param vtx_id: a vertex identifier
        :param parent_id: a vertex identifier
        """
        raise NotImplementedError


class EditableTreeConcept(MutableTreeConcept):

    def sub_tree(self, vtx_id):
        """
        Return a reference of the tree rooted on `vtx_id` in O(1).

        :returns: Editable Tree
        """
        raise NotImplementedError

    def insert_sibling_tree(self, vid, tree ): 
        """
        Insert a tree before the vid.
        vid and the root of the tree are siblings.
        Complexity have to be O(1) if tree comes from the actual tree
        ( tree= sef.sub_tree() )

        :param vid: vertex identifier
        :param tree: a rooted tree
        """
        raise NotImplementedError 

    def add_child_tree(self, parent, tree): 
        """
        Add a tree after the children of the parent vertex.
        Complexity have to be O(1) if tree == sub_tree()

        :param parent: vertex identifier
        :param tree: a rooted tree
        """
        raise NotImplementedError


def traverse_tree(tree, vtx_id, visitor):
    """ 
    Traverse a tree in a prefix or postfix way.
  
    We call a visitor for each vertex.
    This is usefull for printing, cmputing or storing vertices 
    in a specific order. 
  
    See boost.graph.
    """

    visitor.pre_order(vtx_id)

    sons = tree.children(vtx_id)
    for v in sons:
        traverse_tree(tree, v, visitor)

    visitor.post_order(vtx_id)


class Visitor(object):
    """ Used during a tree traversal. """

    def pre_order(self, vtx_id):
        """todo"""
        raise NotImplementedError

    def post_order(self, vtx_id): 
        """todo"""
        raise NotImplementedError

