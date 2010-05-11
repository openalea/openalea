
import platform
import warnings
import collections
import dependencies


def Openalea(_platform=False):
    return Dependency("openalea", _platform)
    
def VPlants(_platform=False):
    return Dependency("vplants", _platform)
    
def Alinea(_platform=False):
    return Dependency("alinea", _platform)        

class Dependency(object):
    def __init__(self, package, _platform=False):
        self.__canonical_deps = []
        self.__distribution_deps = []
        self.__compensated_deps = []
        self.__solve_dependencies(package, _platform)
        
        
    def __str__(self):
        return "canonical->%s\ndistribution->%s\ncompensated->%s"%(str(self.__canonical_deps),
                                                                 str(self.__distribution_deps), 
                                                                 str(self.__compensated_deps))

    def packages(self):
        return self.__canonical_deps
    
    def distribution_packages(self):
        return self.__distribution_deps
    
    def egg_packages(self):
        return self.__compensated_deps
    
    ############################################################
    # Dependency solving and distribution translation follows: #
    ############################################################
    def __get_platform(self):
        _platform = None
        system = platform.system().lower()
        if system == "linux":
            dist, number, name = platform.linux_distribution()
            _platform = dist.lower() + " " + number.lower() + " " + name.lower()
        elif system == "windows":
            dist, host, name, number, proc, procinfo = platform.uname()
            _platform = dist.lower() + " " + number.lower() + " " + name.lower() + " "+ proc.lower()
        else:
            warnings.warn("Currently unhandled system : " + system + ". Implement me please.")
        return _platform    

    def __intersect_platform_names(self, platformName, packageList, mapping):
        #find intersection between platformName and de-canonification keys. Gives
        #the actual platform key. Then we map the canonical name with the platform
        #key from the distribution_canonical_mappings.
        good = {}
        bad = []
        intersectablePlatformName = set(platformName.split(" "))
        for pkgNames in packageList:
            distribs = mapping.get(pkgNames, {})
            for k in distribs.iterkeys():            
                inter = intersectablePlatformName & set(k.split(" "))
                if inter:
                    good[pkgNames] = k
                    break;
            else:
                bad.append(pkgNames)
        return good, bad
    
    def __decanonify(self, packageList, platformName):
        decanonifyable, bad = self.__intersect_platform_names(platformName, packageList,
                                                              dependencies.distribution_canonical_mappings)
        decanonified = []
        for cano in packageList:
            if cano in bad:
                continue
            decanoKey = decanonifyable[cano]
            decanonified.append( dependencies.distribution_canonical_mappings[cano][decanoKey] )
            
        return decanonified, bad    
        
    def __compensate_blacklisted(self, packageList, platformName):
        compensatable, bad = self.__intersect_platform_names(platformName, packageList,
                                                             dependencies.distribution_canonical_blacklists)
        compensated = []
        for comp in packageList:
            if comp in bad:
                continue        
            compensationKey = compensatable[comp]
            compensation = dependencies.distribution_canonical_blacklists[comp][compensationKey]
            if compensation:
                compensated.append( compensation )    
        return compensated, bad

        
    def __solve_dependencies(self, package, _platform=False):
        package_deps = dependencies.canonical_dependencies.get(package, None)
        if not package_deps:
            raise Exception("No such package : " + package)
            
        if _platform == False:
            _platform = self.__get_platform()
        if _platform == None:
            warnings.warn("No dependency de-canonification")
                
        # non recursive dependency solving, euler tour.
        pkgList = set()
        ancestors = collections.deque()
        childs = collections.deque()
        currentPkg = package
        currentPkgChilds = package_deps.__iter__()
        while currentPkg:
            #if current package has childs:
            hasChilds = True
            child = None
            try: child = currentPkgChilds.next()
            except: hasChilds = False
            if hasChilds:
            #   store the current package as an ancestor
                ancestors.append(currentPkg)
            #   store the current child iterator as an ancestor child iterator
                childs.append(currentPkgChilds)
            #   the first element of the child iterator becomes the current package    
                currentPkg = child
            #   we get the list of children of this new current package.
                currentPkgChildsList = dependencies.canonical_dependencies.get(currentPkg, None)
                if currentPkgChildsList:
            #   it becomes the new current child iterator    
                    currentPkgChilds = currentPkgChildsList.__iter__()
                else:
                    currentPkgChilds = None
            #else it is a leaf:                    
            else:
            #   if the leaf is different from the original package:
                if currentPkg != package:
            #       store it in the pgkList    
                    pkgList.add(currentPkg)
                    if len(ancestors) >= 1:
            #       retore previous package and iterator
                        currentPkg = ancestors.pop()
                        currentPkgChilds = childs.pop()           
                    else:
                        currentPkg = None #stop the loop
            #   it is the original package (we reached the root): 
                else:
            #       set the currentPkg to none to stop the loop                
                    currentPkg = None                
        
        pkgList = list(pkgList) #convert set to list
        #de-canonification
        if _platform:
            self.__canonical_deps = pkgList
            self.__compensated_deps, others = self.__compensate_blacklisted(pkgList, _platform)
            self.__distribution_deps = self.__decanonify(others, _platform)[0]      
        else:
            self.__canonical_deps = pkgList
            self.__distribution_deps = pkgList
            self.__compensated_deps = pkgList