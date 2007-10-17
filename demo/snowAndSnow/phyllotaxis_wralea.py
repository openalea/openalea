from openalea.core.core import Package, Factory
#from openalea.core.core import Node
#from openalea.core.core import NodeFactory,Factory
#from openalea.core.interface import IBool, IFloat, IInt, IStr, IDict
#import model as m
#import openalea.mersim.gui.phyllotaxis as phyllotaxis
#import openalea.plotable as plotable



def register_packages(pkgmanager):
    """ Initialisation function
    Return a list of package to include in the package manager.
    This function is called by the package manager when it is updated
    """

    metainfo={ 'version' : '0.0.3',
               'license' : 'CECILL-C',
               'authors' : 'Szymon Stoma',
               'institutes' : 'INRIA/CIRAD',
               'description' : 'Snow&Snow phyllotaxis model',
               }

    if pkgmanager.has_key( "PhyllotaxisModel" ): package = pkgmanager[ "PhyllotaxisModel" ]
    else: package = Package("PhyllotaxisModel", metainfo)
    
    nf = Factory( name= "Snow&Snow phyllotaxis model", 
                      description= "Snow&Snow phyllotaxis model", 
                      category = "Model", 
                      nodemodule = "model_wrapper",
                      nodeclass = "NodeModel",
                      widgetmodule = None,
                      widgetclass = None,
		      parameters=["gamma", "nbr_prims", "discretisation", "visualisation"] 
                      )

    package.add_factory( nf )

    nf = Factory( name= "Prim divergence angles", 
                      description= "Use to generate the divergence angle data. Creates VisualSequence2D.",
                      category = "Model", 
                      nodemodule = "model_wrapper",
                      nodeclass = "NodeDivAngVisualisation",
                      widgetmodule = None,
                      widgetclass = None,
		      parameters=["prim2init_pos"] 
                      )

    package.add_factory( nf )
    
    nf = Factory( name= "Prim absolute angles", 
                      description= "Use to generate the absolute angle data. Creates VisualSequence2D.",
                      category = "Model", 
                      nodemodule = "model_wrapper",
                      nodeclass = "NodeAbsAngVisualisation",
                      widgetmodule = None,
                      widgetclass = None,
		      parameters=["prim2init_pos"] 
                      )

    package.add_factory( nf )

    nf = Factory( name= "Prim time differences", 
                      description= "Use to visualise the time data", 
                      category = "Model", 
                      nodemodule = "model_wrapper",
                      nodeclass = "NodeRelTimeVisualisation",
                      widgetmodule = None,
                      widgetclass = None,
		      parameters=["prim2time"] 
                      )

    package.add_factory( nf )

    nf = Factory( name= "Prim time creation", 
                      description= "Use to visualise the time data", 
                      category = "Model", 
                      nodemodule = "model_wrapper",
                      nodeclass = "NodeAbsTimeVisualisation",
                      widgetmodule = None,
                      widgetclass = None,
		      parameters=["prim2time"] 
                      )

    package.add_factory( nf )

    pkgmanager.add_package(package)


        




        



    
