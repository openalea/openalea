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
#include "starter/scene_container.h"



using namespace sceneobject;
using namespace std;

namespace scenecontainer
{

  //! Class scene.
  //! a scene_object container.

  //! Default constructor
  scene::scene()
    :m_object_list()
  {

  }

  //! Destructor (must be virtual)
  scene::~scene()
  {
    // destroy the stored objects
    list<scene_object*>::iterator it(m_object_list.begin());
    
    while(it!=m_object_list.end())
      {
	if(*it) (*it)->removeReference();
	it++;
      }
   
    m_object_list.clear();
  }
    
  //! Add a scene object to the scene
  //! keep a copy of the object o
  //! @param o a scene_object pointer
  void scene::add_object(scene_object* o)
  {
    if(o) 
      {
	o->addReference();
	m_object_list.push_back(o);
      }
  }

  //! Display all objects of the scene 
  void scene::display_scene()
  {
    list<scene_object*>::iterator it(m_object_list.begin());
    
    while(it!=m_object_list.end())
      {
	if((*it)) (*it)->display();
	else std::cout<<"None"<<std::endl;
	it++;
      }
  }

};




