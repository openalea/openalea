

def geometry_2_piklable_geometry(manager, obj):
    """
    Transform a geometry object from PlantGL in picklable object.

    Rem: name of object is not changed
    :param manager: manager of object to transform
    :param obj: object to transform

    :return: tuple(transformed object, name_of_new_object)
    """
    name = str(obj.getName())

    new_obj = None
    for pickler_class in picklers:
        pickler = pickler_class()
        if isinstance(obj, pickler.classes):
            new_obj = pickler.make_picklable(obj, manager)
            break

    if new_obj is None:
        new_obj = obj
        new_obj.typename = manager.typename
        logger.debug("Transform Nothing %s" % str(obj))

    return (new_obj, name)

"""
def curve():
    return NurbsCurve2D([(-0.5,0,1),(-0.198198,0.40991,1),(0.198198,-0.220721,1),(0.5,0,1)])

c = curve() # No Picklable

cu = RedNurbs2D(c.ctrlPointList) # Picklable
"""
