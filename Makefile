Executable=python ./misc/make_develop.py
Project=openalea

main:
	
	@echo '============== $(Project) Makefile========================================='
	@echo 'This is a simple Makefile that calls the script make_develop.py'
	@echo 'This script has the following options:' 
	@echo '					develop'
	@echo '					undevelop'
	@echo '					install'
	@echo '					release'
	@echo '					html'
	@echo '					latex'
	@echo '					upload_sphinx'
	@echo '==========================================================================='

develop:
	$(Executable) develop -p $(Project) -d .

undevelop:
	$(Executable) undevelop -p $(Project) -d .

install:
	$(Executable) install -p $(Project) -d .

dist:
	$(Executable) release -p $(Project) -d .

html:
	$(Executable) html -p $(Project) -d .

latex:
	$(Executable) latex -p $(Project) -d .

upload_sphinx: 
	$(Executable) upload_sphinx -p $(Project) -d . 
	
