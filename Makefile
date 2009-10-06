# DESCRIPTION: a simple Linux makefile to help building
# packages and their documentation. It will iterate through a
# list of packages that is hardcoded within make_develop.py, 
# a python module inside the misc package 
#
# AUTHOR: Thomas Cokelaer, 
#
# USAGE:	help, type : make
#			
#

Executable=python ./misc/src/openalea/misc/make_develop.py
Project=openalea

main:
	
	@echo '============== $(Project) Makefile==========================================='
	@echo 'This is a simple Makefile that calls the script make_develop.py to run a     '
	@echo 'command in a list of directories (see misc/src/openalea/misc/make_develop.py '
	@echo 'This script has the following options:                                       '
	@echo '		develop  :  alias to  "python setup.py develop"                			'
	@echo '		undevelop:  alias to  "python setup.py develop -u"             			'
	@echo '		install  :  alias to  "python setup.py install"                			'
	@echo '		release  :  alias to  "python setup.py bdist_egg -d ../../dist sdist -d ../../dist'
	@echo '		html     :  alias to  "python setup.py build_sphinx -b html -E 			'
	@echo '		latex    :  alias to  "python setup.py build_sphinx -b latex -E			'
	@echo '		pdf      :  alias to  "cd doc/latex; make 					   			'
	@echo '		sphinx_upload : alias to "python setup.py sphinx_upload        			'
	@echo '============================================================================='


develop:
	$(Executable) develop -p $(Project) -d .

nosetests:
	$(Executable) nosetests -p $(Project) -d .

bdist:
	$(Executable) bdist -p $(Project) -d .

bdist_egg:
	$(Executable) bdist_egg -p $(Project) -d .

sdist:
	$(Executable) sdist -p $(Project) -d .

release:
	$(Executable) release -p $(Project) -d .
 
undevelop:
	$(Executable) undevelop -p $(Project) -d .

install:
	$(Executable) install -p $(Project) -d .

clean:
	$(Executable) clean -p $(Project) -d .

html:
	$(Executable) html -p $(Project) -d . 
	cd doc;	make html;	cd ..

latex:
	$(Executable) latex -p $(Project) -d . 
	cd doc;	make latex;	cd ..

pdf:
	$(Executable) pdf -p $(Project) -d . 
	cd doc/build/latex;	make;	cd ../../..

sphinx_upload: 
	$(Executable) sphinx_upload -p $(Project) 
	#python ./doc/sphinx_upload.py -u cokelaer

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
	tar cvfz OpenAlea.Source-0.7.0.r1793.tar.gz ./openalea_source
