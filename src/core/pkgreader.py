# -*- python -*-
#
#       OpenAlea.Core: OpenAlea Core
#
#       Copyright or (C) or Copr. 2006 INRIA - CIRAD - INRA  
#
#       File author(s): Christophe Pradal <christophe.prada@cirad.fr>
#                       Samuel Dufour-Kowalski <samuel.dufour@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#

__doc__="""
This module contains abstration to read and write configuration files.
Configuration can be read from python files or XML files
and written to xml file

"""

__license__= "Cecill-C"
__revision__=" $Id$ "


from xml.dom.minidom import parse
from core import Package, NodeFactory
from subgraph import SubGraphFactory
import os
import sys
import imp

class FormatError(Exception):
    def __init__(self, str):
        Exception.__init__(self, str)

################################################################################

# READERS


class PackageReader(object):
    """ Default base class (define the interface) """

    def __init__(self, filename):
        """ filename : the file path to read"""
        
        self.filename = filename

    def register_packages(self, pkgmanager):
        """ Load packages in pkgmanager """

        # Function must be overloaded
        raise RuntimeError()

    def register_session(self, session):
        """ Load session data """

        # Function must be overloaded
        raise RuntimeError()

        

class PyPackageReader(PackageReader):
    """ Read package as a Python file """

    def __init__(self, filename):
        """ 
        Filename must be relative to a python sys path
        """
        
        PackageReader.__init__(self, filename)


    def filename_to_module (self, filename):
        """ Transform the filename ending with .py to the module name """

        # delete the .py at the end
        if(filename.endswith('.py')):
            modulename = filename[:-3]

        l = modulename.split(os.path.sep)
        modulename = '.'.join(l)

        return modulename


    def register_packages(self, pkgmanager):
        """ Execute Wralea.py """

        retlist = []

        basename = os.path.basename(self.filename)
        basedir = os.path.abspath( os.path.dirname( self.filename ))

        if(not basedir in sys.path):
            sys.path.append(basedir)
        
        modulename = self.filename_to_module(basename)

        (file, pathname, desc) = imp.find_module(modulename,  [basedir])
        wraleamodule = imp.load_module(modulename, file, pathname, desc)

        wraleamodule.register_packages( pkgmanager )
        
        if(file) :
            file.close()



class XmlPackageReader(PackageReader):
    """ Read package as a XML file """

    def __init__(self, filename):
        PackageReader.__init__(self, filename)

        self.__currentNode__ = None
        self.doc = None


    def __del__(self):
        """ Release DOM objects """
        if(self.doc):
            self.doc.unlink()

    def load_xml(self, filename):
        
        from xml.dom.minidom import parse

        if(self.doc): self.doc.unlink()
        self.doc = parse(filename)

    def get_attribute(self, attr_dict, name, default):
        """ Return the ascii string of an attribute
        @param attr dict : minidom attribute dictionnary
        @param name : name of the attribute (string)
        @param default : default value if attribute does not exist
        """

        try:
            return attr_dict[name].value.encode('ascii')
        except:
            return default

    def getText(self, xmlnode, default):
        """
        Return the text of an xmlnode
        @param xmlnode
        @param default : default value
        """

        try:
            val = xmlnode.childNodes[0].nodeValue
            return val.strip()
        except:
            return default

 
    def get_root_element(self):

	if self.__currentNode__ == None:
            self.__currentNode__ = self.doc.documentElement
        return self.__currentNode__


    def get_xml_wraleapath(self, pkgmanager):
        """ parse Xml to retrieve wraleapath
        The new path are added to the pkgmanager
        """

        for path in self.get_root_element().getElementsByTagName("wraleapath"):

            attr = path.attributes
            value = self.get_attribute(attr, "value", None)

            if(value):
                pkgmanager.add_wraleapath(value)


    def get_xml_packages(self, pkgmanager):
        """ Parse Xml to retrieve package info, nodefactory and subgraph
        return the created package list
        """
    
        packagelist = []

        for package in self.get_root_element().getElementsByTagName("package"):

            attr = package.attributes
            name = self.get_attribute(attr, "name", None)
            if(not name):
                raise FormatError("<package> must have name attribute")

            metainfo = {}

            for info in ("license", "version",
                         "authors", "institute", "description", "publication", "url"):

                try:
                    value = self.getText(package.getElementsByTagName(info)[0], None)
                    if(value) : metainfo[info] = value
                except : pass

            pkg = Package(name, metainfo)

            # Build the node factories and add them to the package
            nf_list = self.get_xml_nodefactory(package, pkgmanager)
            if(nf_list) : map( pkg.add_factory, nf_list)

            # Build the subgraph factories and add them to the package
            sg_list = self.get_xml_subgraphfactory(package, pkgmanager)
            if(sg_list) : map( pkg.add_factory, sg_list)

            packagelist.append(pkg)

        return packagelist


    def get_xml_nodefactory(self, xmlnode, pkgmanager):
        """ Parse Xml to retrieve nodefactory info
        Return a list of node factory
        """

        factorylist = []
        for nodefactory in xmlnode.getElementsByTagName("nodefactory"):

            attr = nodefactory.attributes
            name = self.get_attribute(attr, "name", None)
            category = self.get_attribute(attr, "category", None)
            
            if(not name or not category):
                raise FormatError("<nodefactory> must have name and category attributes")

            desc = self.getText(nodefactory.getElementsByTagName("description")[0], "")

            node = nodefactory.getElementsByTagName("node")[0]

            nodename = self.get_attribute(node.attributes, "class", None)
            nodemodule = self.get_attribute(node.attributes, "module", None)
                
            widget = nodefactory.getElementsByTagName("widget")[0]
            widgetname = self.get_attribute(widget.attributes, "class", None)
            widgetmodule = self.get_attribute(widget.attributes, "module", None)

            if(not nodename or not nodemodule):
                raise FormatError('<nodefactory> must have <node module= "..." class="..."/> ')
            
            nf = NodeFactory(name = name, 
                             description = desc, 
                             category  = category, 
                             nodemodule = nodemodule,
                             nodeclass = nodename,
                             widgetmodule = widgetmodule,
                             widgetclass = widgetname, 
                             )

            factorylist.append(nf)

        return factorylist


    def get_xml_subgraphfactory(self, xmlnode, pkgmanager):
        """ Parse Xml to retrieve subgraphfactory info """

        factorylist = []

        for subgraph in xmlnode.getElementsByTagName("subgraph"):
            
            attr = subgraph.attributes
            name = self.get_attribute(attr, "name", None)
            category = self.get_attribute(attr, "category", None)

            if(not name or not category):
                raise FormatError("<subgraph> must have name and category attributes")

            # inputs and outputs
            ninput = int(self.get_attribute(attr, "num_input", 0))
            noutput = int(self.get_attribute(attr, "num_output", 0))
            
            # description
            description= subgraph.getElementsByTagName("description")[0]
            desc = self.getText(description, '')

            sg = SubGraphFactory(pkgmanager, name = name,
                                 description = desc, category = category)
            sg.set_nb_input(ninput)
            sg.set_nb_output(noutput)
            

            for element in subgraph.getElementsByTagName("element"):

                attr = element.attributes

                package_id = self.get_attribute(attr, "package_id", None)
                factory_id = self.get_attribute(attr, "factory_id", None)
                elt_id = self.get_attribute(attr, "id", None)

                if(not package_id or not factory_id or not elt_id): continue

                kdata = {}
                for data_element in element.getElementsByTagName("data"):

                    attr = data_element.attributes
                    key = self.get_attribute(attr, "key", None)
                    value = self.get_attribute(attr, "value", None)

                    try: value = float(value)
                    except : pass
                    
                    if(key and value):
                        kdata[key] = value

                sg.add_nodefactory(elt_id, (package_id, factory_id), kdata)

                
            for connection in subgraph.getElementsByTagName("connect"):
                attr = connection.attributes

                src_id = self.get_attribute(attr, "src_id", None)
                src_port = self.get_attribute(attr, "src_port", None)
                dst_id = self.get_attribute(attr, "dst_id", None)
                dst_port = self.get_attribute(attr, "dst_port", None)

                try:
                    sg.add_connection (src_id, int(src_port), dst_id, int(dst_port) )
                except Exception, e:
                    print e
                    raise FormatError("Invalid <connect>")
                
            factorylist.append(sg)

        return factorylist


    def get_workspaces(self, session, pkgmanager):
        """ Read the workspace informations in the xml document """

        for workspace in self.get_root_element().getElementsByTagName("workspace"):

            attr = workspace.attributes
            pkg_id = self.get_attribute(attr, "pkg_id", None)
            factory_id = self.get_attribute(attr, "factory_id", None)
            
            try:
                pkg = pkgmanager[pkg_id]
                factory = pkg[factory_id]
                node = factory.instantiate()
                session.add_workspace(node)
            except:
                raise FormatError("Invalid <workspace>")

                

    def register_packages(self, pkgmanager):
        """ Read XML file and register package in pkgmanager"""

        self.doc = parse(self.filename)

        pkglist = self.get_xml_packages(pkgmanager)

        # Add package to the manager
        map(pkgmanager.add_package, pkglist)
        
        del(self.doc)
        self.doc = None


    def register_session(self, session):
        """ Read Session data """
        
        self.doc = parse(self.filename)

        self.get_workspaces(session, session.pkgmanager)

        del(self.doc)
        self.doc = None


        


################################################################################

    # WRITERS



class XmlWriter(object):
    """ base class for all XML Writer """

    def fill_structure(self, newdoc, top_element):
        """ Fill XML structure in newdoc with top_element as Root """
        raise RuntimeError()


    def write_config(self, filename):
        """ Write configuration on filename """

        from xml.dom.minidom import getDOMImplementation

        impl = getDOMImplementation()

        newdoc = impl.createDocument(None, "openalea", None)
        top_element = newdoc.documentElement

        self.fill_structure(newdoc, top_element)

        f = open(filename, 'w')
        f.write(newdoc.toprettyxml())
        f.close()



class NodeFactoryXmlWriter(XmlWriter):
    """ Class to write a node factory to XML """

    def __init__(self, factory):
        """ Constructor :
        @param factory : the instance to serialize
        """
        
        self.factory = factory
        

    def fill_structure(self, newdoc, top_element):
        """ Fill XML structure in newdoc with top_element as Root """

        nodefactory = self.factory
    
        # <nodefactory>
        nf_elt = newdoc.createElement ('nodefactory')
        nf_elt.setAttribute("name", nodefactory.name)
        nf_elt.setAttribute("category", nodefactory.category)
    
        top_element.appendChild(nf_elt) 

        elt = newdoc.createElement("description")
        node = newdoc.createTextNode(nodefactory.description)
        elt.appendChild(node)
        nf_elt.appendChild(elt)

        elt = newdoc.createElement("node")
        elt.setAttribute("module", str(nodefactory.nodemodule))
        elt.setAttribute("class", str(nodefactory.nodeclass_name))
        nf_elt.appendChild(elt)
        
        elt = newdoc.createElement("widget")
        elt.setAttribute("module", str(nodefactory.widgetmodule))
        elt.setAttribute("class", str(nodefactory.widgetclass_name))
        nf_elt.appendChild(elt)

    

class SubGraphFactoryXmlWriter(XmlWriter):
    """ Class to write a subgraph to XML """

    def __init__(self, factory):
        """ Constructor :
        @param factory : the instance to serialize
        """
        
        self.factory = factory

    def fill_structure(self, newdoc, top_element):
        """ Fill XML structure in newdoc with top_element as Root """

        factory = self.factory
    
        # <subgraph>
        sg_elt = newdoc.createElement ('subgraph')
        sg_elt.setAttribute("name", factory.name)
        sg_elt.setAttribute("category", factory.category)
        sg_elt.setAttribute("num_input", str(factory.nb_input))
        sg_elt.setAttribute("num_output", str(factory.nb_output))
        top_element.appendChild(sg_elt) 

        elt = newdoc.createElement('description')
        node = newdoc.createTextNode(factory.description)
        elt.appendChild(node)
        sg_elt.appendChild(elt)

        elt = newdoc.createElement('doc')
        node = newdoc.createTextNode(factory.doc)
        elt.appendChild(node)
        sg_elt.appendChild(elt)

        for (id, (package_id, factory_id)) in factory.elt_factory.items():

            elt = newdoc.createElement ('element')
            elt.setAttribute("package_id", package_id)
            elt.setAttribute("factory_id", factory_id)
            elt.setAttribute("id", id)

            # Write Data
            for key in factory.elt_data[id].keys():

                value = factory.elt_data[id][key]
                data_elt = newdoc.createElement('data')
                data_elt.setAttribute("key", key)
                data_elt.setAttribute("value", str(value))
                elt.appendChild(data_elt)

            sg_elt.appendChild(elt)

        for ( (dst_id, dst_port), (src_id, src_port) ) in factory.connections.items():

            elt = newdoc.createElement ('connect')
            elt.setAttribute("src_id", src_id)
            elt.setAttribute("src_port", str(src_port))
            elt.setAttribute("dst_id", dst_id)
            elt.setAttribute("dst_port", str(dst_port))
            sg_elt.appendChild(elt)


class PackageXmlWriter(XmlWriter):
    """ Class to write a subgraph to XML """

    def __init__(self, package):
        """ Constructor :
        @param package : the package to serialize
        """
        self.pkg = package

        
    def fill_structure(self, newdoc, top_element):
        """ Fill Xml structure with package data """

        package = self.pkg
        
        # <package>
        pkg_elt = newdoc.createElement('package')
        pkg_elt.setAttribute("name", package.name)
        top_element.appendChild(pkg_elt) 

        for info in package.metainfo:

            elt = newdoc.createElement(info)
            node = newdoc.createTextNode(package.metainfo[info])
            elt.appendChild(node)
            pkg_elt.appendChild(elt)

        for n in package.get_names():
            nf = package.get_factory(n)

            writer = nf.get_xmlwriter()
            writer.fill_structure(newdoc, pkg_elt)



class SessionWriter(XmlWriter):
    """ Class to write the Session"""

    def __init__(self, session):
        """
        Constructor:
        @param session : a session instance
        """
        self.session = session
        

    def fill_structure(self, newdoc, top_element):
        """ Fill XML structure in newdoc with top_element as Root """

#         for path in self.pmanager.wraleapath:
#             elt = newdoc.createElement('wraleapath')
#             elt.setAttribute("value", str(path))
#             top_element.appendChild(elt) 

#         # for each package object
#         for p in self.pmanager.values():
#             writer= PackageXmlWriter(p)
#             writer.fill_structure(newdoc, top_element)

        # Save User package

        user_pkg = self.session.user_pkg
        writer = PackageXmlWriter(user_pkg)
        writer.fill_structure(newdoc, top_element)

        # Save Workspaces Data
        for node in self.session.workspaces:
            factory = node.factory
            pkg_id = factory.package.get_id()
            factory_id = factory.get_id()
            workspace_elt = newdoc.createElement('workspace')
            workspace_elt.setAttribute("pkg_id", pkg_id)
            workspace_elt.setAttribute("factory_id", factory_id)
            top_element.appendChild(workspace_elt) 
     

