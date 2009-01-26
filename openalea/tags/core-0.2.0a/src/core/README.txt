11/04/2007 Christophe Pradal <christophe.pradal@cirad.fr>

* Reviewing OpenAlea core package
* DONE core.py: split core.py to node.py and package.py
* FIX core.py (get_inputs_desc): Replace this utility function 
by a class giving function introspection user friendly (see PEP

* DONE interface.py: separate metaclass stuff to interface definition
* DONE observer.py: change RuntimeError to NotImplementedError
* DONE observer.py: modification of notify_listeners implementation.
* TODO observer.py: API?
* FIX initialise -> observed.register_listeners(self)

* DONE path.py: update to the latest version
* DONE change persistence.py name or move implementation to different files (io.py?)
* DONE: change RuntimeError to NotImplementedError
*FIX PyNodeFactoryWriter -> NodeFactory2Python adapter
* DONE Base class Reader & Writer are useless

* DONE pkgmanager.py: get_wralea_[home, path]. Implement these functions based on a user config file.
* FIX Do not refer wralea name in the API. Use package instead.

* TODO all.py: use path.py rather than os.path

* DONE SubGraph.py: SubGraph -> CompositeNode
* DONE class CompositeNode( Graph, Node )
