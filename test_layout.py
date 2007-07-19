import layout

pkg = layout.PackageLayout('toto')
pkg.check_name()
pkg.mkdirs()
pkg.mkfiles()
pkg.template_wralea()

