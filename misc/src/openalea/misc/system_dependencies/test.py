


import os_deploy, os_factory, distributions, dependency

osname = os_factory.BaseOsFactory.get_platform()
software = "openalea"
fake = True
theOs = os_factory.OsFactory().create(osname)
dependencies = dependency.Dependency(software, osname)
print str(dependencies)

theOs.install_packages(dependencies.runtime_distribution_packages(), fake)
