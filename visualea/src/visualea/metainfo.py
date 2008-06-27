# Configuration file 


def get_version():

    import pkg_resources
    dists = pkg_resources.require("openalea.visualea")
    return dists[0].version

url = "http://openalea.gforge.inria.fr"

def get_copyrigth():

    return u"Copyright \xa9  2006-2008 INRIA - CIRAD - INRA\n"
