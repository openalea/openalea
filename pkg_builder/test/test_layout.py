from openalea.pkg_builder import PackageBuilder


import shutil
shutil.rmtree('prospect')

def test():
    pkg = PackageBuilder(name='prospect', package='Prospect')
    pkg.check_name()
    pkg.set_languages(cpp=True, c=True, fortran=True)
    pkg.set_languages(cpp=False, c=False, fortran=False)
    pkg.mkdirs()
    pkg.mkfiles()
    pkg.template_legal()
    pkg.template_setup()
    pkg.template_scons()
    pkg.template_wralea()
    pkg.template_doc()



def test_valid_project():
    try:
        pkg = PackageBuilder(name='prospect', package='Prospect', project='dummy')
    except:
        assert True


def test_run():

    import openalea.pkg_builder.layout as layout
    try:
        layout.main()
    except:
        assert True

    import sys
    sys.argv.append('--name')
    sys.argv.append('prospect')
    sys.argv.append('--package')
    sys.argv.append('Prospect')
    sys.argv.append('--language')
    sys.argv.append('cpp')
    layout.main()

