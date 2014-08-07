from openalea.plantgl.all import NurbsCurve2D, BezierCurve2D, Polyline2D, NurbsPatch

try:
    logger.DEBUG
except NameError:
    from openalea.core import logger
    logger.default_init(level=logger.DEBUG, handlers=["qt"]) #TODO get level from settings
    logger.connect_loggers_to_handlers(logger.get_logger_names(), logger.get_handler_names())

class RedNurbs2D(NurbsCurve2D):
    def __init__(self, ctrlPoint, typename=""):
        super(RedNurbs2D, self).__init__(ctrlPoint)
        self.typename = typename
        
    def __reduce__(self):
        return (RedNurbs2D, (self.ctrlPointList, self.typename,))
        
class RedBezierNurbs2D(BezierCurve2D):
    def __init__(self, ctrlPoint, typename=""):
        super(RedBezierNurbs2D, self).__init__(ctrlPoint)
        self.typename = typename
        
    def __reduce__(self):
        return (RedBezierNurbs2D, (self.ctrlPointList, self.typename,))
        
class RedPolyline2D(Polyline2D):
    def __init__(self, ctrlPoint, typename=""):
        super(RedPolyline2D, self).__init__(ctrlPoint)
        self.typename = typename
        
    def __reduce__(self):
        return (RedPolyline2D, (self.pointList, self.typename,))       
        
class RedNurbsPatch(NurbsPatch):
    def __init__(self, ctrlPoint, typename=""):
        super(RedNurbsPatch, self).__init__(ctrlPoint)
        self.typename = typename
        
    def __reduce__(self):
        return (RedNurbsPatch, (self.ctrlPointMatrix, self.typename,))  

def geometry_2_piklable_geometry(manager, obj):
    """
    Transform a geometry object from PlantGL in picklable object.
    
    Rem: name of object is not changed
    :param manager: manager of object to transform
    :param obj: object to transform
    
    :return: tuple(transformed object, name_of_new_object)
    """         
    geom = obj
    name = str(geom.getName())
    if isinstance(geom, NurbsPatch):
        new_obj = RedNurbsPatch(geom.ctrlPointMatrix, manager.typename)
        logger.debug("Transform NurbsPatch into RedNurbsPatch")
    elif isinstance(geom, Polyline2D):
        new_obj = RedPolyline2D(geom.pointList, manager.typename)
        logger.debug("Transform Polyline2D into RedPolyline2D")
    elif isinstance(geom, NurbsCurve2D):
        new_obj = RedNurbs2D(geom.ctrlPointList, manager.typename)
        logger.debug("Transform NurbsCurve2D into RedNurbs2D")
    elif isinstance(geom, BezierCurve2D):
        new_obj = RedBezierNurbs2D(geom.ctrlPointList, manager.typename)
        logger.debug("Transform BezierCurve2D into RedBezierNurbs2D")
    else:
        new_obj = obj
        new_obj.typename = manager.typename
        logger.debug("Transform Nothing %s"%str(geom))
    
    return(new_obj,name)         

"""
def curve():
    return NurbsCurve2D([(-0.5,0,1),(-0.198198,0.40991,1),(0.198198,-0.220721,1),(0.5,0,1)])

c = curve() # No Picklable

cu = RedNurbs2D(c.ctrlPointList) # Picklable
"""
