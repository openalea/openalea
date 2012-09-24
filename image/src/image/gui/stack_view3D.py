#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
# -*- python -*-
#
#       openalea.image.analysis.gui.stack_view3D
#
#       Copyright 2010-2011 INRIA - CIRAD - INRA - ENS-Lyon
#
#       File author(s): Vincent Mirabet - Frederic Boudon
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#       http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
################################################################################
__license__= "Cecill-C"
__revision__=" $Id$ "

# import libraries
import sys
import copy
import math
import vtk

import numpy as np
import scipy.ndimage as nd

from openalea.image.serial.basics import imread
from openalea.image.spatial_image import SpatialImage
from openalea.image.algo.analysis import SpatialImageAnalysis3D

#compatibility
try:
    from tvtk.tools import ivtk
    from tvtk.api import tvtk
except ImportError:
    from enthought.tvtk.tools import ivtk
    from enthought.tvtk.api import tvtk
    from enthought.mayavi.core import lut_manager


from colormaps import black_and_white, rainbow_full, rainbow_green2red, rainbow_red2blue
import warnings
#TODO : decorateurs


def img2polydata_simple(image, dictionnaire=None, verbose=True):
    """
    Convert a |SpatialImage| to a PolyData object with cells surface

    : Parameters :
    dictionnaire : cell->scalar dictionary
    """

    labels_provi = list(np.unique(image))
    #ici on filtre déjà les listes
    #~ labels= [i for i in labels_provi if i not in list_remove]
    labels= labels_provi

    try:      labels.remove(0)
    except:   pass
    try:      labels.remove(1)
    except:   pass

    #print image.shape

    xyz = {}
    if verbose:print "on récupère les bounding box"
    bbox = nd.find_objects(image)
    #print labels
    for label in xrange(2,max(labels)+1):
        if not label in labels: continue
        if verbose:print "% until cells are built", label/float(max(labels))*100
        slices = bbox[label-1]
        label_image = (image[slices] == label)
        #here we could add a laplacian function to only have the external shape
        mask = nd.laplace(label_image)
        label_image[mask!=0] = 0
        mask = nd.laplace(label_image)
        label_image[mask==0]=0
        # compute the indices of voxel with adequate label
        a = np.array(label_image.nonzero()).T
        a+=[slices[0].start, slices[1].start, slices[2].start ]
        #print a.shape
        if a.shape[1] == 4:
            #print a
            pass
        else:
            xyz[label] = a

    vx,vy,vz = image.resolution

    polydata = tvtk.AppendPolyData()
    polys = {}
    filtre=[i for i in xyz.keys() if i in dictionnaire.keys()]
    k=0.0
    for c in filtre:
        if verbose: print "% until first polydata is built", k/float(len(filtre))*100
        k+=1.
        p=xyz[c]
        p=p.astype(np.float)
        pd = tvtk.PolyData(points=xyz[c].astype(np.float))
        pd.point_data.scalars = [float(dictionnaire[c]) for i in xrange(len(xyz[c]))]    
        f=tvtk.VertexGlyphFilter(input=pd)
        f2=tvtk.PointDataToCellData(input=f.output)
        polys[c]=f2.output
        polydata.add_input(polys[c])
        polydata.set_input_array_to_process(0,0,0,0,0)

    return polydata



def img2polydata_complexe(image, list_remove=[], sc=None, verbose=False):
    """
    Convert a |SpatialImage| to a PolyData object with cells surface

    : Parameters :
    list_remove : a list of cells to be removed from the tissue before putting it on screen
    sc : if you give a parameter here, it will use it as scalar. you need to give a
    cell->scalar dictionary
    """

    labels_provi = list(np.unique(image))
    #ici on filtre déjà les listes
    #~ labels= [i for i in labels_provi if i not in list_remove]
    labels= labels_provi

    try:      labels.remove(0)
    except:   pass
    try:      labels.remove(1)
    except:   pass

    #print image.shape

    xyz = {}
    if verbose:print "on récupère les bounding box"
    bbox = nd.find_objects(image)
    #print labels
    for label in xrange(2,max(labels)+1):
        if not label in labels: continue
        if verbose:print "% until cells are built", label/float(max(labels))*100
        slices = bbox[label-1]
        label_image = (image[slices] == label)
        #here we could add a laplacian function to only have the external shape
        mask = nd.laplace(label_image)
        label_image[mask!=0] = 0
        mask = nd.laplace(label_image)
        label_image[mask==0]=0
        # compute the indices of voxel with adequate label
        a = np.array(label_image.nonzero()).T
        a+=[slices[0].start, slices[1].start, slices[2].start ]
        #print a.shape
        if a.shape[1] == 4:
            #print a
            pass
        else:
            xyz[label] = a


    vx,vy,vz = image.resolution

    polydata = tvtk.AppendPolyData()
    polys = {}
    filtre=[i for i in xyz.keys() if i not in list_remove]
    k=0.0
    for c in filtre:
        if verbose: print "% until first polydata is built", k/float(len(filtre))*100
        k+=1.
        p=xyz[c]
        p=p.astype(np.float)
        pd = tvtk.PolyData(points=xyz[c].astype(np.float))
        if sc:
            try:
                pd.point_data.scalars = [float(sc[c]) for i in xrange(len(xyz[c]))]
            except:
                pd.point_data.scalars = [float(0) for i in xrange(len(xyz[c]))]
        else:
            pd.point_data.scalars = [float(c) for i in xrange(len(xyz[c]))]
        f=tvtk.VertexGlyphFilter(input=pd)
        f2=tvtk.PointDataToCellData(input=f.output)
        polys[c]=f2.output
        polydata.add_input(polys[c])
        polydata.set_input_array_to_process(0,0,0,0,0)


    try:
        labels_not_in_sc = list(set(list(np.unique(image)))-set(sc))
    except TypeError:
        labels_not_in_sc=[]

    if 0 in labels_not_in_sc: labels_not_in_sc.remove(0)
    if 1 in labels_not_in_sc: labels_not_in_sc.remove(1)
    filtre=[i for i in xyz.keys() if i in list_remove or i in labels_not_in_sc]
    if filtre!=[]:
        polydata2 = tvtk.AppendPolyData()
        polys2 = {}    
        k=0.0
        for c in filtre:
            if verbose: print "% until second polydata is built", k/float(len(filtre))*100
            k+=1.
            p=xyz[c]
            p=p.astype(np.float)
            pd = tvtk.PolyData(points=xyz[c].astype(np.float))
            pd.point_data.scalars = [0. for i in xrange(len(xyz[c]))]
            f=tvtk.VertexGlyphFilter(input=pd)
            f2=tvtk.PointDataToCellData(input=f.output)
            polys2[c]=f2.output
            polydata2.add_input(polys2[c])
    else:
        polydata2=tvtk.AppendPolyData()
        polydata2.set_input_array_to_process(0,0,0,0,0)
        polys2 = {}
        pd = tvtk.PolyData()
        polydata2.add_input(pd)
    return polydata, polydata2


def rootSpI(img, list_remove=[], sc=None, lut_range = False, verbose=False):
    """
    case where the data is a spatialimage
    """
    # -- cells are positionned inside a structure, the polydata, and assigned a scalar value.
    polydata,polydata2 = img2polydata_complexe(img, list_remove=list_remove, sc=sc, verbose=verbose)
    m = tvtk.PolyDataMapper(input=polydata.output)
    m2 = tvtk.PolyDataMapper(input=polydata2.output)
    
    # -- definition of the scalar range (default : min to max of the scalar value).
    if sc:
        ran=[sc[i] for i in sc.keys() if i not in list_remove]
        if (lut_range != None) and (lut_range != False):
            print lut_range
            m.scalar_range = lut_range[0],lut_range[1]
        else:
            m.scalar_range = np.min(ran), np.max(ran)
    else:
        m.scalar_range=np.min(img), np.max(img)
    
    # -- actor that manage changes of view if memory is short.
    a = tvtk.QuadricLODActor(mapper=m)
    a.property.point_size=8
    a2 = tvtk.QuadricLODActor(mapper=m2)
    a2.property.point_size=8
    #scalebar
    if lut_range != None:
        sc=tvtk.ScalarBarActor(orientation='vertical',lookup_table=m.lookup_table)
    return a, a2, sc, m, m2


#~ def rootSpIA(img, list_remove=[], sc=None, verbose=False):
    #~ """
    #~ case where the data is a spatialimageanalysis
    #~ """ 
    #~ if verbose:
        #~ print "Type of image: SpatialImageAnalisys."
    #~ #cells are positionned inside a structure, the polydata, and assigned a scalar value
    #~ polydata = img2polydata_complexe(img.image, list_remove=list_remove, sc=sc, verbose=verbose)
    #~ m = tvtk.PolyDataMapper(input=polydata.output)
    #~ #definition of the scalar range (default : min to max of the scalar value)
    #~ if sc:
        #~ ran=[sc[i] for i in sc.keys() if i not in list_remove]
        #~ m.scalar_range=np.min(ran), np.max(ran)
    #~ #actor that manage different views if memory is short
    #~ a = tvtk.QuadricLODActor(mapper=m)
    #~ a.property.point_size=8
    #~ #scalebar
    #~ sc=tvtk.ScalarBarActor(orientation='vertical',lookup_table=m.lookup_table)
    #~ return a, sc, m


def create_labels(img, render):
    liste=list(img.labels())
    xmin = 0
    xLength = 1000
    xmax = xmin + xLength
    ymin = 00
    yLength = 1000
    ymax = ymin + yLength
    # Create labels for barycenters
    m=tvtk.PolyData()
    vertex = tvtk.Points()
    provi1=tvtk.LongArray()
    p=0
    cell_barycentre=img.center_of_mass()
    x,y,z=img.image.resolution
    for c,toto in enumerate(liste):
        vertex.insert_point(p, cell_barycentre[c][0]/x, cell_barycentre[c][1]/y,cell_barycentre[c][2]/z )
        provi1.insert_value(p, toto)
        p+=1

    m.points=vertex
    m.point_data.scalars=provi1
    vtkLabels=m
    #here the idea is to mask labels behind surfaces
    visPts = tvtk.SelectVisiblePoints()
    visPts.input=vtkLabels
    visPts.renderer=render
    visPts.selection_window=1
    visPts.selection=(xmin, xmin+xLength, ymin, ymin+yLength)
    # Create the mapper to display the point ids.  Specify the format to
    # use for the labels.  Also create the associated actor.
    ldm = tvtk.LabeledDataMapper()
    # ldm.SetLabelFormat("%g")
    ldm.input=visPts.output
    ldm.label_mode='label_scalars'
    vtk_labels = tvtk.Actor2D()
    vtk_labels.mapper=ldm
    return vtk_labels


def display3D(img, list_remove=[], dictionary=None, lut=black_and_white, lut_range = False, cell_separation = False, verbose=False, labels=False):
    """
    paramètres :
        - img (SpatialImage ou SpatialImageAnalysis) : segmented tissu
        - list_remove (list) : une liste des cellules à enlever lors de l'affichage
        - dictionary (dict) : dictionnaire cells->scalar
        - lut : -Look-Up Table- disponibles dans 'colormaps.py'
        - lut_range (list) : list of 2 values defing the range (min, max) of the lut.
        - cell_separation (bool) : if True add a "separation" between cells.
        - verbose (bool) : pour afficher ou non les progressions
        - labels (bool) : display labels of cell in 3D.

    Examples : 
        im1 = imread('/home/vince/softs/vplants/vplants/trunk/vtissue/imaging/mars_alt/test/data/segmentation/imgSeg.inr.gz')
        im1a=SpatialImageAnalysis(im1)
        dictionary=dict(zip(im1a.labels(), im1a.volume()))
        labs=im1a.labels()
        L1=im1a.L1()[1]
        filtre=[i for i in labs if i not in L1]
        display3D(im1, verbose=True)

    Fonction maitre en deux parties :
        1. Gestion du format de l'objet donné en paramètre;
        2. Gestion de l'affichage.
    """
    if cell_separation:
        # -- Management of file format
        if isinstance(img,SpatialImageAnalysis3D):
            im = compute_cell_separation(img.image)
        elif isinstance(img,SpatialImage):
            im = compute_cell_separation(img)
        else:
            print "for now this file format is not managed by display3D"
            return None

    # -- Management of file format
    if isinstance(img,SpatialImageAnalysis3D):
        if list_remove == None:
            list_remove = img._ignoredlabels
        a, a2, sc, m, m2 = rootSpI(img.image, list_remove = list_remove, sc = dictionary, lut_range = lut_range, verbose=verbose)
    elif isinstance(img,SpatialImage):
        a, a2, sc, m, m2 = rootSpI(img, list_remove = list_remove, sc = dictionary, lut_range = lut_range, verbose=verbose)
    else:
        print "for now this file format is not managed by display3D"
        return None

    # -- choice of colormap
    m.lookup_table = lut(m.lookup_table)
    from openalea.image.all import black_and_white
    m2.lookup_table = black_and_white(m2.lookup_table)
    # -- switching on the viewer and loading the object and the scalarbar
    viewer = ivtk.viewer()
    viewer.scene.add_actor(a)
    viewer.scene.add_actor(a2)
    if dictionary != None and lut_range != None:
        viewer.scene.add_actor(sc)
    if labels:
        if isinstance(img,SpatialImageAnalysis3D):
            lab=create_labels(img, viewer.scene.renderer)
            viewer.scene.add_actor(lab)


def export_vtk(img, filename="default", list_remove=[], dictionary=None, verbose=False):
    """
    paramètres :
    img : SpatialImage ou SpatialImageAnalysis
    filename : le nom de la sortie
    list_remove : une liste des cellules à enlever lors de l'affichage
    dictionary : dictionnaire cells->scalar
    lut : disponibles dans colormaps
    verbose : pour afficher ou non les progressions
    
    ATTENTION, SUR CERTAINES MACHINES LE FICHIER VTK A DES VIRGULES POUR DEFINIR LES DOUBLE, ALORS QUE LES SOFTS ONT BESOIN DE POINTS
    
    """
    #management of file format
    if isinstance(img,SpatialImageAnalysis3D):
        p,p2=img2polydata_complexe(img.image, list_remove = list_remove, sc = dictionary, verbose = verbose)
    elif isinstance(img,SpatialImage):
        p,p2=img2polydata_complexe(img, list_remove = list_remove, sc = dictionary, verbose = verbose)
    else:
        warnings.warn("for now this file format is not managed by export_vtk")
        return
    p.update()
    p2.update()
    w = tvtk.PolyDataWriter()
    w.input=p.output
    #on enlève l'extension de filename si il y en a une
    filename=filename.split(".")[0]
    w.file_name=filename+"_1.vtk"
    w.write()
    w.input=p2.output
    w.file_name=filename+"_2.vtk"
    w.write()


def export_vtk_cut(img, filename="default.vtk", dictionary=None, verbose=False):
    """
    paramètres :
    img : SpatialImage ou SpatialImageAnalysis
    filename : le nom de la sortie
    dictionary : dictionnaire cells->scalar
    lut : disponibles dans colormaps
    verbose : pour afficher ou non les progressions
    
    ATTENTION, SUR CERTAINES MACHINES LE FICHIER VTK A DES VIRGULES POUR DEFINIR LES DOUBLE, ALORS QUE LES SOFTS ONT BESOIN DE POINTS
    
    """
    #management of file format
    if isinstance(img,SpatialImageAnalysis3D):
        p=img2polydata_simple(img.image, dictionnaire=dictionary,verbose = verbose)
    elif isinstance(img,SpatialImage):
        p=img2polydata_simple(img, dictionnaire=dictionary,verbose = verbose)
    else:
        warnings.warn("for now this file format is not managed by export_vtk")
        return
    p.update()
    w = tvtk.PolyDataWriter()
    w.input=p.output
    w.file_name=filename
    w.write()


def compute_cell_separation(mat):
    """
    Function creating a space between cells for display.
    Change the shared voxel between two cell to 0 so you can clearly see the seperations bewteen cells.
    """
    import scipy.nd as nd
    import numpy as np
    import copy
    sep=nd.laplace(mat)
    sep2=copy.copy(sep)
    sep2[np.where(mat==1)]=0
    sep2[np.where(sep==0)]=1
    sep2[np.where(sep!=0)]=0
    mat=mat*sep2
    del sep2,sep
    
    return mat


if __name__ == '__main__':
    im1 = imread('../../../test/segmentation.inr.gz')
    im1a=SpatialImageAnalysis(im1)
    dictionary=dict(zip(im1a.labels(), im1a.volume()))
    labs=im1a.labels()
    L1=im1a.L1()[1]
    filtre=[i for i in labs if i not in L1]
    display3D(im1,filtre, dictionary, rainbow_full)
    
