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



/* WRAPPER Boost.python for scene_container class */

#include "export_scene_container.h"

#include <boost/python.hpp>
using namespace boost::python;


// Define python module "scenecontainer"
BOOST_PYTHON_MODULE(_scenecontainer)
{
  // add scene_container wrapper
  class_scene_container();

}
