from openalea.core import Factory, IInt, IStr, Package

def register_packages(pkgmanager):
    package = Package("jcd_test", {})

    nf = Factory( name="dbg", 
                description="debug", 
                category="display", 
                inputs=(dict(name='in', interface=None, value=None), ),
                outputs=(dict(name='out', interface=None), ),
                nodemodule="jcd_node",
                nodeclass="DebugNode",
                )
    package.add_factory( nf )
    
    nf = Factory( name="cid", 
                description="cells scale", 
                category="creator", 
                inputs=(),
                outputs=(dict(name='scale', interface=IInt), ),
                nodemodule="jcd_node",
                nodeclass="CidNode",
                )
    package.add_factory( nf )
    
    nf = Factory( name="wid", 
                  description="walls scale", 
                  category="creator", 
                  inputs=(),
                  outputs=(dict(name='scale', interface=IInt),),
                  nodemodule="jcd_node",
                  nodeclass="WidNode",
                )
    package.add_factory( nf )
    
    nf = Factory( name="eid", 
                description="edges scale", 
                category="creator", 
                inputs=(),
                outputs=(dict(name='scale', interface=IInt),),
                nodemodule="jcd_node",
                nodeclass="EidNode",
                )
    package.add_factory( nf )
    pkgmanager.add_package(package)


