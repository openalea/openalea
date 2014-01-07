from openalea.vpltk.project.script import Scripts
from openalea.core.path import path

def test_add_script():
	scripts_manager = Scripts()
	scripts_manager.add_script("1", "blablabla")
	scripts_manager.add_script("2", "blablabla2")
	scripts_manager.add_script("3", "blablabla3")
	scripts_manager.add_script("4", "blablabla4")
	assert len(scripts_manager) == 4
	assert len(scripts_manager.ez_name) == 4
	assert len(scripts_manager.name) == 4
	assert scripts_manager.is_project() is False
	assert scripts_manager.is_script() is True
	
def test_rm_script():
	scripts_manager = Scripts()
	scripts_manager.add_script("1", "blablabla")
	scripts_manager.add_script("2", "blablabla2")
	scripts_manager.add_script("3", "blablabla3")
	scripts_manager.rm_script("2")
	assert len(scripts_manager) == 2
	assert len(scripts_manager.ez_name) == 2
	assert len(scripts_manager.name) == 2

def test_rm_script_by_ez_name():
	scripts_manager = Scripts()
	scripts_manager.add_script(str(path("../1").abspath()), "blablabla")
	scripts_manager.add_script(str(path("../2").abspath()), "blablabla2")
	scripts_manager.add_script(str(path("3").abspath()), "blablabla3")
	scripts_manager.rm_script_by_ez_name("2")
	assert len(scripts_manager) == 2
	assert len(scripts_manager.ez_name) == 2
	assert len(scripts_manager.name) == 2
	
def test_rename():
	scripts_manager = Scripts()
	scripts_manager.add_script("1", "blablabla")
	scripts_manager.rename_script("1","2")
	assert scripts_manager["2"] == "blablabla"
	assert len(scripts_manager) == 1
	assert len(scripts_manager.ez_name) == 1
	assert len(scripts_manager.name) == 1
	
