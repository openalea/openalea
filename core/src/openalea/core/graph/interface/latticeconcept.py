"""Lattice Interface"""

class ScaleLattice:
    """ todo """
    
    def scales(self):
        """
        Return scale_id iterator
        """
        pass

    def nb_scales(self):
        """
        Return the number of scales
        """
        pass

    def coarsest(self):
        """
        Return the coarsest scale identifier
        """
        pass

    def finest(self):
        """
        Return the finest scale identifier
        """
        pass

    def coarser(self, sid):
        """
        Return the coarser scales of sid

        :Parameters:
          - `sid`: scale identifier

        :Return: iter of scale_id
        """
        pass

    def nb_coarser(self, sid):
        """
        Return the number of coarser scale identifier
        """
        pass

    def finer(self, sid):
        """
        Return the coarser scales of sid

        :Parameters:
          - `sid`: scale identifier

        :Return: iter of scale_id
        """
        pass

    def nb_finer(self, sid):
        """
        Return the number of finer scale identifier
        """
        pass

    def min(self, sid1, sid2):
        """
        Return the coarser scale of common finer scales of sid1 and sid2

        :Parameters:
          - `sid1`: scale identifier
          - `sid2`: scale identifier

        :Return: a scale identifier
        """
        pass

    def max(self, sid1, sid2):
        """
        Return the finer scale of common coarser scales of sid1 and sid2

        :Parameters:
          - `sid1`: scale identifier
          - `sid2`: scale identifier

        :Return: a scale identifier
        """
        pass


class MutableScaleLattice(ScaleLattice):
    """
    A mutable scale lattice. (sic)
    """

    def add_scale( self, sid, min_id, max_id ):
        """
        Add a scale `sid` between `min_id` and `max_id`.
        If min_id is coarsest(), add sid after coarsest
        If max_id is finest() then add sid before finest
        Else add sid between min_id and max_id

        :Parameters:
          - `sid`: the scale identifier to add
          - `min_id`: finer scale identifier
          - `max_id`: coarser scale identifier
        """
        pass

    def remove_scale(self,sid):
        """
        Remove a scale `sid`.

        :Parameters:
          - `sid`: the scale identifier to add
        """
        pass

    def scale_id(self):
        """
        Return a free scale identifier

        :Return: a scale identifier
        """
        pass


class Container:
    """
    Container Interface (tree, graph or other data structure)
    """

    def elements(self):
        """
        :Return: iter of element id
        """
        pass

    def nb_elements(self):
        """
        Return the number of elements
        """
        pass

    def has_element(self,eid):
        """
        Test if `eid` exist in self.

        :Parameters:
          - `eid`: element identifier
        :Return: bool
        """
        pass


class MultiscaleContainer(ScaleLattice, Container):
    """
    A multiscale container interface.
    seid= (eid,sid)
    seid: scale and element identifier
    """

    def scale(self, seid):
        """
        Return the scale identifier
        :Return: scale id
        """
        pass

    def element(self, seid):
        """
        Return the element identifier

        :Return: elemet id
        """
        pass

    def components(self, seid, sid):
        """
        Return the components of the complex seid at the scale sid

        :Parameters:
          - `seid`: the complex scale and element identifier
          - `sid`: the components scale identifier

        :Return: iter of seid
        """
        pass

    def nb_components(self, seid, sid):
        """
        Return the number of components of the complex seid at the scale sid

        :Parameters:
          - `seid`: the complex scale and element identifier
          - `sid`: the components scale identifier

        :Return: int
        """
        pass

    def complex(self, seid, sid):
        """
        Return the complex of the component seid at the scale sid

        :Parameters:
          - `seid`: the component scale and element identifier
          - `sid`: the complex scale identifier

        :Return: seid
        """
        pass

    def container(self, sid):
        """
        Return a ref on the container associated to sid.

        :Parameters:
          - `sid`: scale identifier

        :Return: container (a reference, not a copy)
        """
        pass


class MutableMultiscaleContainer(MutableScaleLattice, MultiscaleContainer):
    """
    Interface of a mutable MultiscaleContainer
    """
    pass

class MultiscaleTree(MultiscaleContainer):
    """
    A MultiscaleTree interface.
    """
    pass

class MutableMultiscaleTree(MutableMultiscaleContainer, MultiscaleTree):
    """
    A mutable MultiscaleTree
    """
    pass

