from openalea.pkg_builder import PackageLayout

pkg = layout.PackageLayout('toto')
pkg.check_name()
pkg.mkdirs()
pkg.mkfiles()
pkg.template_wralea()

