/*------------------------------------------------------------------------------
 *                                                                              
 *        OpenAlea.Starter: Example package                                     
 *                                                                              
 *        Copyright 2006 INRIA - CIRAD - INRA                      
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


// INCLUDE
#include <iostream>

// Project header files are prefixed with 'starter' directory for exportation compatibility
#include "starter/scene_object.h"

using namespace std;

namespace sceneobject
{

  /// Class scene_object : base class for all scene objects .
  /// A scene object can be hold in a scene for display purpose. 
  
  
  /// Default Constructor
  scene_object::scene_object()
  { }
  
  /// Destructor
  scene_object:: ~scene_object()
  { }


  /// Display the object name to the standard output
  void scene_object::display() 
  {

    // (use the polymorphic function get_name() )
    std::cout<< this->get_name() <<std::endl;
  }


  /// Class leaf : Represent a tree leaf.
  /// Specialisation of the scene_object abstract class. */

  /// Default Constructor
  leaf::leaf()
    :scene_object()
  {
    //std::cout<<"Leaf constructor"<<std::endl;
  }
  
  /// Default Destructor
  leaf:: ~leaf()
  {
    //std::cout<<"Leaf destructor"<<std::endl;
  }

  /// Return the name of the object
  const string leaf::get_name() 
  {
    return "Leaf";
  }




  /// Class trunk : Represents a tree trunk 
  /// Specialisation of the scene_object abstract class. */
  

  /// Default Constructor
  trunk::trunk()
    :scene_object()
  {
    //std::cout<<"Trunk constructor"<<std::endl;
  }
  
  /// Default Destructor
  trunk:: ~trunk()
  {
    //std::cout<<"Trunk destructor"<<std::endl;
  }

  /// Return the name of the object
  const string trunk::get_name() 
  {
    return "Trunk";
  }

};



