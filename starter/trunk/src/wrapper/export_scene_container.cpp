/*------------------------------------------------------------------------------
 *                                                                              
 *        OpenAlea.Starter: Example package                                     
 *                                                                              
 *        Copyright or © or Copr. 2006 INRIA - CIRAD - INRA                      
 *                                                                              
 *        File author(s): Christophe Pradal <christophe.prada@cirad.fr>         
 *                        Samuel Dufour-Kowalski <samuel.dufour@sophia.inria.fr>
 *                                                                              
 *        Distributed under the Cecill-C License.                               
 *        See accompanying file LICENSE.txt or copy at                          
 *            http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html       
 *                                                                              
 *        OpenAlea WebSite : http://openalea.gforge.inria.fr                    
 *       
 *        $Id$
 *                                                                       
 *-----------------------------------------------------------------------------*/


#include "export_scene_container.h"

#include "starter/scene_container.h"
using namespace scenecontainer;

#include <boost/python.hpp>
using namespace boost::python;

// export wrapper
void class_scene_container()
{

  // scene_container class wrapper
  class_<scene>("Scene", "Represents a complete scene containing multiple scene objects")
    .def("display_scene", &scene::display_scene, "Display the scene")
    .def("get_size", &scene::get_size, "Return the number of objects in the scene")
    .def("add_object", &scene::add_object, "Add an object to the scene");
}
