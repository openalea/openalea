/* -*-c++-*- 
 *------------------------------------------------------------------------------
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

#ifndef __STARTER_SCENE_OBJECT_H__
#define __STARTER_SCENE_OBJECT_H__

#include <string>

// Project header files are prefixed with 'starter' directory for exportation compatibility
#include "starter/config.h"
#include "starter/refcountptr.h"


/**
  namespace sceneobject.
 
  Group scene objects hierarchy.  The scene objects define simple
  biological objects which can be displayed in a scene (ex: leaf,
  trunk)
*/

namespace sceneobject
{
  /** \class scene_object.
      \brief Abstract base class for all scene objects.

      A scene object reprents the a generic object which can be
      included in a scene.  All scene object will inherit from this
      class which defines the default interface.

      scene_object inherits from RefCountObject in order to manager
      reference counting and the object lifetime.
  */
  

  class SCENEOBJ_EXPORT scene_object : public  RefCountObject
  {
    
  public:

    /// @name Constructors
    //@{

    /// Default constructor
    scene_object();
    
    //@}

    /// @name Destructor
    //@{

    /// Destructor (must be virtual)
    virtual ~scene_object();

    //@}


    /// @name Accessors
    //@{

    /// Abstract virtual fonction 
    /// Return the name of the object
    virtual const std::string get_name()=0;

    //@}

    
    /// @name Display function
    //@{

    /// Display the object name to the standard output
    virtual void display();
    
    //@}

  };


  /** \class leaf.
      \brief represents a tree leaf.
  */
 
  class SCENEOBJ_EXPORT leaf : public scene_object 
  {

  public:
    /// @name Constructors
    //@{

    /// Default constructor
    leaf();
    //@}

    /// @name Destructor
    //@{
    /// Destructor
    virtual ~leaf();
    //@}

    /// @name Accessors
    //@{
    /// Get the object name
    /// Return the name of the object
    virtual const std::string get_name();
    //@}
  };


  /** \class trunk.
      \brief represents a tree trunk.
  */
  
  class SCENEOBJ_EXPORT trunk : public scene_object 
  {

  public:
    /// @name Constructors
    //@{

    /// Default Constructor
    trunk();
    //@}

    /// @name Destructor
    //@{

    /// Destructor
    virtual ~trunk();
    //@}

    /// @name Accessors
    //@{

    /// Get the object name
    /// Return the name of the object
    virtual const std::string get_name();
    //@}

  };

};

#endif
