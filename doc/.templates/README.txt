Short explanation of this directory contents (see the sphinx documentation for
more details)

index.html, indexsidebar and layout.html are the main template layouts for the
sphinx output documentation. They are used by all the packages.

The index.html will read extra template files such as openalea_packages if the
project is openalea, vplants_packages if it is vplants and so on. 

common_header and common_footer are used by <project>_packages.html files.

Except if you know what you are doing, you should not touch those files that are used
by all packages when building sphinx !


