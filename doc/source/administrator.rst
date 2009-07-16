

Gforge
======

When developes decide to upload their package, they will use the **python setup build_sphinx** command, which calls the command.py module in the deploy package. There, there is a class called sphinx_upload that will scp the **html** and **latex** directories into the gforge. 


The files will be copied into http://openalea.gforge.inria.fr/doc/.

All vplants pacakges will be copied under  http://openalea.gforge.inria.fr/doc/vplants

All openalea pacakges will be copied under  http://openalea.gforge.inria.fr/doc/openalea

All alinea pacakges will be copied under  http://openalea.gforge.inria.fr/doc/alinea

finally, the main index, corresponding to openalea/doc directory, which is not a package, will be copied into  http://openalea.gforge.inria.fr/doc/openalea/doc


.. warning:: to be able to upload the html and latex directories in the gforge, the **doc** directory must contain a directory that is called <package>/doc in the gforge. The admnistrator should do that. In the case of the special case of openalea/doc , which is not a package: create a build directory in the  http://openalea.gforge.inria.fr/doc/openalea/doc dirctory and use the script sphinx_upload.py in ./openalea/doc

The reason for such a structure is that it is a copy of the local strucutre, therefore you can create the documentation locally as well, having exactly the same structure as on the web.

.. warning::
   when a new package needs to be uploaded, you must create a directory in the remote directory. For instance, if you have a package called **test**, then the administrator must create a directory /home/groups/openalea/htdocs/doc/openalea/**test**/doc
