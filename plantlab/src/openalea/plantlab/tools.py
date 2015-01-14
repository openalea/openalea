# -*- coding: utf-8 -*-
# -*- python -*-
#
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2014 INRIA - CIRAD - INRA
#
#       File author(s): Guillaume Baty <guillaume.baty@inria.fr>
#
#       File contributor(s):
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################


def to_color(material_list):
    """
    Material(name='C0', ambient=Color3(65,45,15)) -> ('C0', (65,45,15))
    """
    color_list = []
    for material in material_list:
        d = material.diffuse
        a = material.ambient
        color = (material.name, (a.red, a.green, a.blue), d)
        color_list.append(color)
    return color_list


def to_material(color_list):
    """
    ('C0', (65,45,15)) -> Material(name='C0', ambient=Color3(65,45,15))
    """

    from openalea.plantgl.all import Material, Color3
    material_list = []
    for color in color_list:
        material = Material(color[0], Color3(*color[1][:3]))
        material.diffuse = color[2]
        material_list.append(material)
    return material_list