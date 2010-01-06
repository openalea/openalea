Quick Start
###########

First,you need to install **Sphinx**. This can be simply done using easy_install as follows::

    easy_install -U sphinx          # use sudo under Linux systems

Then, you need to initiate a new project. Type::

    sphinx-quickstart

and follow the instructions. Most of the time you simply need to press enter. You will have to enter the project name. Once done, the information provided have been put inside the file **conf.py** that you can edit at any time. 

In principle you should now have a file called **con.py**, a file called **index.rst** and some directories. 

Edit **index.rst** and change it to your need. 

In order to compile the documentation, type (under linux)::

    make html

or::

    make latex


To build a PDF version, type the previous command and then::

    cd _build
    make all-pdf

