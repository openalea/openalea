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


#ifndef __RCEXPORT__
#define __RCEXPORT__

#include <boost/python.hpp>

//We need to tell Boost.Python how to work with your smart pointer.
//Short explanation:
//  "get_pointer" extracts the pointer to the object it manages.
//  "pointee" extracts the type of the object, smart pointer manages.

//You can read more about this functionality in the reference manual:
//http://boost.org/libs/python/doc/v2/pointee.html .

namespace boost{ 

  namespace python{

    template <class T>
      struct pointee< RCPtr<T> >{
        typedef T type;
      };
  } 
  
  
}

template<class T>
inline T * get_pointer(RCPtr<T> const& p){
  return p.toPtr();
}


#endif 
