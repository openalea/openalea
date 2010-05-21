from openalea.pkg_builder import PackageBuilder

pkg = PackageBuilder('prospect')
pkg.check_name()
pkg.mkdirs()
pkg.mkfiles()
pkg.template_wralea()

