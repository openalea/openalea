from openalea.vpltk.project.manager import ProjectManager


def test_discover():
    pm = ProjectManager()
    pm.discover()

    assert len(pm.projects) > 0


def test_discover_not_add_twice_by_discover_twice():
    pm = ProjectManager()
    pm.discover()

    projects_nb = len(pm.projects)
    pm.discover()

    assert len(pm.projects) == projects_nb


def test_discover_not_add_twice():
    pm = ProjectManager()
    pm.discover()

    nb = len(pm.projects)
    nb2 = int(nb / 2)
    assert nb > 1
    assert nb2 > 0
    assert str(pm.projects[nb - 1].name) != str(pm.projects[nb2 - 1].name)


def test_add_path():
    pm = ProjectManager()
    pm.discover()

    nb = len(pm.projects)
    pm.find_links.append(pm.find_links[0])
    pm.discover()

    nb2 = len(pm.projects)
    assert nb == nb2


def test_search():
    pm = ProjectManager()
    pm.discover()
    projs = pm.search()
    assert type(projs) is list
    assert projs is pm.projects


def test_load_default():
    pm = ProjectManager()
    pm.discover()
    proj = pm.load_default()
    proj2 = pm.default()
    assert type(proj) is type(proj2)
    assert str(proj.name) == "temp"
