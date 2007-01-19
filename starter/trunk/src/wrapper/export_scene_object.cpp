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


/* WRAPPER Boost.python scene_object hierarchy */


#include "export_scene_object.h"

#include "starter/scene_object.h"
using namespace sceneobject;

#include <boost/python.hpp>
using namespace boost::python;

#include "starter/refcountptr.h"
#include "rcexport.h"

using namespace std;



// Annexe class to Wrap virtual function in scene_object
// At each virtual function call, we must check if the function has been overriden 
// in a pure python class derivated from C++ base class
struct scene_objectWrap : scene_object, wrapper<scene_object>
{
  // pure virtual function
  const string get_name()
    {
        return this->get_override("get_name")();
    }
  
  // virtual function with default implementation
  void display()
    {
        if (override f = this->get_override("display"))  f(); 
        else scene_object::display();
    }
};


// Export scene_object wrapper
void class_scene_object()
{

  // scene_object class wrapper
  class_<scene_objectWrap, RCPtr<scene_objectWrap>, boost::noncopyable>("SceneObject", "Abstract base class for scene object" )
    .def("display", &scene_object::display, "Display the object name")
    .def("get_name", pure_virtual(&scene_object::get_name), "Return the object name");
  
  // leaf class wrapper
  class_<leaf, bases<scene_object>, RCPtr<leaf> >("Leaf", "Leaf object" );
  
  // trunk class wrapper
  class_<trunk, bases<scene_object>, RCPtr<trunk> >("Trunk", "Trunk Object" );

}
