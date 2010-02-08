# DESCRIPTION: a simple Linux makefile to help building
# packages and their documentation. It will iterate through a
# list of packages that is hardcoded within multisetup.py, 
#
# AUTHOR: Thomas Cokelaer, 
#
# USAGE:	help, type : make
#			
#

Executable = python multisetup.py

main:
	$(Executable) --help
    
develop:
	$(Executable) develop 
    
nosetests:
	$(Executable) nosetests -w test

bdist:
	$(Executable) bdist 

bdist_egg:
	$(Executable) bdist_egg 

sdist:
	$(Executable) sdist -p

release:
	$(Executable) install nosetests -w test build_sphinx -E bdist_egg -d ../dist sdist -d ../dist

develop_release: 
	$(Executable) develop nosetests -w test build_sphinx -E sdist -d ../dist bdist_egg -d ../dist --keep-going
 
undevelop:
	$(Executable) develop -u 

install:
	$(Executable) install 
	
uninstall:
	echo 'to be done' 

clean:
	$(Executable) clean -a

html:
	$(Executable) build_sphinx -b html  
	cd doc;	make html;	cd ..

latex:
	$(Executable) build_sphinx -b latex 
	cd doc;	make latex;	cd ..

pdf:
	$(Executable)  build_sphinx -b latex
	cd doc/build/latex;	make;	cd ../../..

sphinx_upload: 
	$(Executable) sphinx_upload  
	
doc: html latex pdf	

cleandoc:
	rm -r ./*/doc/html
	rm -r ./*/doc/latex
	rm -r ./doc/build/


source:
	#svn up
	#svn info | grep Revision| awk '{print $$2}'
	rm -rf openalea_source;
	svn export ../openalea openalea_source
	tar cvfz OpenAlea.Source-0.8.0.r2203.tar.gz ./openalea_source
