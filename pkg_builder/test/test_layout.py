from openalea.pkg_builder import PackageBuilder

pkg = PackageBuilder('prospect', 'Prospect')
pkg.check_name()
pkg.set_languages(cpp=False)
pkg.mkdirs()
pkg.mkfiles()
pkg.template_legal()
pkg.template_setup()
pkg.template_scons()
pkg.template_wralea()
pkg.template_doc()

