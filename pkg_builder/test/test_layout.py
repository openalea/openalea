from openalea.pkg_builder import PackageBuilder

from openalea.core.path import path
testpkg = path('testpkg')
if testpkg.exists():
    testpkg.rmtree()

def test():
    pkg = PackageBuilder(name='TestPkg', project='alinea')
    pkg.check_name()
    pkg.set_languages(cpp=False, c=False, fortran=False)
    pkg.set_languages(cpp=True, c=True, fortran=True)
    pkg.mkdirs()
    pkg.mkfiles()
    pkg.template_legal()
    pkg.template_setup()
    pkg.template_scons()
    pkg.template_wralea()
    pkg.template_doc()



def test_valid_project():
    try:
        pkg = PackageBuilder(name='TestPkg', project='dummy')
    except:
        assert True

    pkg = PackageBuilder(name='TestPkg', project='OpenALEA')


def test_run():

    import openalea.pkg_builder.layout as layout
    try:
        layout.main()
    except:
        assert True

    import sys
    sys.argv.append('--name')
    sys.argv.append('TestPkg')
    sys.argv.append('--project')
    sys.argv.append('Alinea')
    sys.argv.append('--language')
    sys.argv.append('cpp')
    layout.main()

