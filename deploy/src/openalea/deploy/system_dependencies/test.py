


import distributions, dependency

osname = dependency.get_platform()
software = "openalea"
fake = True
theOs = dependency.OsInterfaceFactory().create(osname)
dependencies = dependency.DependencySolver(software, osname)
print str(dependencies)

theOs.install_packages(dependencies.runtime_distribution_packages(), fake)
