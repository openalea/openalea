/* -*-c++-*- 
 *-----------------------------------------------------------------------------
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

#ifndef __STARTER_SCENE_CONTAINER_H__
#define __STARTER_SCENE_CONTAINER_H__

// Project header files are prefixed with 'starter' directory for exportation compatibility
#include "starter/config.h"
#include "starter/scene_object.h"
#include "starter/refcountptr.h"

#include <list>


/**
 * namespace scenecontainer 
*/

namespace scenecontainer
{

  /** \class scene
      \brief A scene_object container.
  */


  class SCENECONT_EXPORT scene
  {
    
  public:
    /// @name Constructors
    //@{

    //! Default constructor
    scene();
    //@}

    /// @name Destructor
    //@{

    //! Destructor (must be virtual)
    virtual ~scene();
    //@}

    /// @name Container functions
    //@{

    //! Add a scene object to the scene.
    //! Increment object reference counter.
    //! @param o a scene_object pointer.
    void add_object( sceneobject::scene_object* o);

    //! Return the number of contained objects
    int get_size()
    {
      return m_object_list.size();
    }

    //@}

    /// @name Display
    //@{

    //! Display all objects of the scene.
    void display_scene();
    //@}

  private:
    std::list<sceneobject::scene_object*> m_object_list;
    
  };
};





#endif
