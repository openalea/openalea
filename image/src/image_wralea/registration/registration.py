# -*- python -*-
#
#       image: image registration
#
#       Copyright 2006 INRIA - CIRAD - INRA  
#
#       File author(s): Eric Moscardi <eric.moscardi@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
"""
This module import functions to registration images
"""

__license__= "Cecill-C"
__revision__ = " $Id:  $ "

import numpy as np
from openalea.core import Node
from openalea.core import Factory, IFileStr, IInt, IBool, IFloat, \
    ISequence, IEnumStr, IStr, IDirStr, ITuple, IDict
from openalea.image import cp2transfo, SpatialImage, angles2transfo
from openalea.asclepios import baladin


def wra_points2transfo (image1,points1,image2,points2) :

    points1 = np.array(points1)
    points2 = np.array(points2)

    if not isinstance(image1,SpatialImage) :
	image1 = SpatialImage(image1)

    if not isinstance(image2,SpatialImage) :
	image2 = SpatialImage(image2)
    
    vrx = image1.resolution[0]
    vry = image1.resolution[1]
    vrz = image1.resolution[2]
    vfx = image2.resolution[0]
    vfy = image2.resolution[1]
    vfz = image2.resolution[2]

    # explain in the voxel world
    points1[:,0] *= vrx
    points1[:,1] *= vry
    points1[:,2] *= vrz
    points2[:,0] *= vfx
    points2[:,1] *= vfy
    points2[:,2] *= vfz

    transformation = cp2transfo(points1,points2)

    return transformation



def wra_angles2transfo (image1, image2, angleX, angleY, angleZ) :
    return angles2transfo(image1, image2, angleX, angleY, angleZ)


class BlockMatching(Node):
    """ VisuAlea version of baladin
    """

    def __init__(self):
        Node.__init__(self,

        inputs = [  {"name" : "reference_image", "interface" : None},
                    {"name" : "floating_image", "interface" : None},
                    {"name" : "initial_matrix", "interface" : None},

                    {"name" : "low_threshold_floating", "interface" : IInt, "value" : -100000, "hide" : True},
                    {"name" : "high_threshold_floating", "interface" : IInt, "value" : 100000, "hide" : True},
                    {"name" : "low_threshold_reference", "interface" : IInt, "value" : -100000, "hide" : True},
                    {"name" : "high_threshold_reference", "interface" : IInt, "value" : 100000, "hide" : True},
                    {"name" : "fraction_block-reference", "interface" : IFloat, "value" : 0.5, "hide" : True},
                    {"name" : "fraction-block-floating", "interface" : IFloat, "value" : 0.5, "hide" : True},

                    {"name" : "transformation", "interface" : IEnumStr(["Rigid","Similitude","Affine"]), "value" : "Rigid"},

                    {"name" : "estimator", "interface" : IEnumStr(["Weighted Least Trimmed Squares","Least Trimmed Squares","Weighted Least Squares","Least Squares"]),
                     "value" : "Weighted Least Trimmed Squares"},

                    {"name" : "ltscut", "interface" : IFloat(0.,1.,0.01), "value" : 0.75},

                    {"name" : "similarity-measure", "interface" : IEnumStr(["correlation coefficient","extended correlation coefficient"]), 
                     "value" : "correlation coefficient", "hide" : True},

                    {"name" : "threshold-similarity-measure", "interface" : IFloat, "value" : 0., "hide" : True},
                    {"name" : "max-iterations", "interface" : IInt, "value" : 4, "hide" : True},
                    {"name" : "block-sizes", "interface" : ITuple, "value" : (4,4,4), "hide" : True},
                    {"name" : "block-spacing", "interface" : ITuple, "value" : (3,3,3), "hide" : True},
                    {"name" : "block-borders", "interface" : ITuple, "value" : (0,0,0), "hide" : True},
                    {"name" : "block-neighborhood-sizes", "interface" : ITuple, "value" : (3,3,3), "hide" : True},
                    {"name" : "block-steps", "interface" : ITuple, "value" : (1,1,1), "hide" : True},
                    {"name" : "fraction-variance-blocks", "interface" : IFloat, "value" : 0.75},
                    {"name" : "decrement-fraction-variance-blocks", "interface" : IFloat, "value" : 0.2, "hide" : True},
                    {"name" : "minimum-fraction-variance-blocks", "interface" : IFloat, "value" : 0.5, "hide" : True},

                    {"name" : "pyramid-levels", "interface" : IInt, "value" : 6},

                    {"name" : "pyramid-finest-level", "interface" : IInt, "value" : 1},

                    {"name" : "pyramid-filtered", "interface" : IInt, "value" : 0, "hide" : True},
                    {"name" : "rms", "interface" : IBool, "value" : True, "hide" : True}
                    ],

        outputs = [ {"name" : "block-matching transformation", "interface" : None}])

    def __call__(self, inputs):
        
        reference_image = self.get_input("reference_image")
        floating_image = self.get_input("floating_image")
        initial_matrix = self.get_input("initial_matrix")


        parameters = {}

        parameters["seuil_bas_ref"] = self.get_input("low_threshold_reference")
        parameters["seuil_haut_ref"] = self.get_input("high_threshold_reference")
        parameters["seuil_bas_flo"] = self.get_input("low_threshold_floating")
        parameters["seuil_haut_flo"] = self.get_input("high_threshold_floating")
        parameters["seuil_pourcent_ref"] = self.get_input("fraction_block-reference")
        parameters["seuil_pourcent_flo"] = self.get_input("fraction-block-floating")

        transformation = self.get_input("transformation")
        if transformation == "Rigid":
            parameters["transfo"] = baladin.enumTypeTransfo.RIGIDE  
        elif transformation == "Similitude":
            parameters["transfo"] = baladin.enumTypeTransfo.SIMILITUDE
        elif transformation == "Affine":
            parameters["transfo"] = baladin.enumTypeTransfo.AFFINE

        estimator = self.get_input("estimator")
        if estimator == "Weighted Least Trimmed Squares":
            parameters["use_lts"] = 1
            parameters["estimateur"] = baladin.enumTypeEstimator.TYPE_LSSW
        elif estimator == "Least Trimmed Squares":
            parameters["use_lts"] = 1
            parameters["estimateur"] = baladin.enumTypeEstimator.TYPE_LS
        elif estimator == "Weighted Least Squares":
            parameters["use_lts"] = 0
            parameters["estimateur"] = baladin.enumTypeEstimator.TYPE_LSSW
        elif estimator == "Least Squares":
            parameters["use_lts"] = 0
            parameters["estimateur"] = baladin.enumTypeEstimator.TYPE_LS

        parameters["lts_cut"] = self.get_input("ltscut")

        mesure = self.get_input("similarity-measure")
        if mesure == "correlation coefficient":
            parameters["mesure"] = baladin.enumTypeMesure.MESURE_CC
        elif mesure == "extended correlation coefficient":
            parameters["mesure"] = baladin.enumTypeMesure.MESURE_EXT_CC
        
        parameters["seuil_mesure"] = self.get_input("threshold-similarity-measure")
        parameters["nbiter"] = self.get_input("max-iterations")

        block_sizes = self.get_input("block-sizes")
        if block_sizes is not None:
            bl_dx, bl_dy, bl_dz = block_sizes
            parameters["bl_dx"] = bl_dx
            parameters["bl_dy"] = bl_dy
            parameters["bl_dz"] = bl_dz
        
        block_spacing = self.get_input("block-spacing")
        if block_spacing is not None:
            bl_next_x, bl_next_y, bl_next_z = block_spacing
            parameters["bl_next_x"] = bl_next_x
            parameters["bl_next_y"] = bl_next_y
            parameters["bl_next_z"] = bl_next_z

        block_borders = self.get_input("block-borders")
        if block_borders is not None:
            bl_border_x, bl_border_y, bl_border_z = block_borders
            parameters["bl_border_x"] = bl_border_x
            parameters["bl_border_y"] = bl_border_y
            parameters["bl_border_z"] = bl_border_z

        block_neighborhood_sizes = self.get_input("block-neighborhood-sizes")
        if block_neighborhood_sizes is not None:
            bl_size_neigh_x, bl_size_neigh_y, bl_size_neigh_z = block_neighborhood_sizes
            parameters["bl_size_neigh_x"] = bl_size_neigh_x
            parameters["bl_size_neigh_y"] = bl_size_neigh_y
            parameters["bl_size_neigh_z"] = bl_size_neigh_z

        block_steps = self.get_input("block-steps")
        if block_steps is not None:
            bl_next_neigh_x, bl_next_neigh_y, bl_next_neigh_z = block_steps
            parameters["bl_next_neigh_x"] = bl_next_neigh_x
            parameters["bl_next_neigh_y"] = bl_next_neigh_y
            parameters["bl_next_neigh_z"] = bl_next_neigh_z

        parameters["bl_pourcent_var"] = self.get_input("fraction-variance-blocks")

        parameters["bl_pourcent_var_min"] = self.get_input("minimum-fraction-variance-blocks")
        parameters["bl_pourcent_var_dec"] = self.get_input("decrement-fraction-variance-blocks")

        parameters["pyn"] = self.get_input("pyramid-levels")

        parameters["pys"] = self.get_input("pyramid-finest-level")

        parameters["py_filt"] = self.get_input("pyramid-filtered")
        parameters["rms"] = self.get_input("rms")

        transformation_result = baladin.pyramidal_block_matching(reference_image, floating_image, initial_matrix, parameters)

        return (transformation_result,)
