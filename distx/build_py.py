import os, sys
from distutils.command.build_py import build_py as _build_py
from distutils.util import convert_path
from glob import glob

class build_py(_build_py):
    """Enhanced 'build_py' command that includes package platform library
    files with packages
    """

    def find_data_files (self, package, src_dir):
        """Return filenames for package's data files in 'src_dir'"""
        globs = (self.package_data.get('', [])
                 + self.package_data.get(package, []))

        if('win' in sys.platform and self.distribution.include_package_lib):
            globs += [ '*.pyd', '*.dll']
        if('posix' in os.name and self.distribution.include_package_lib):
            globs += [ '*.pyd', '*.so']
        
        files = []
        for pattern in globs:
            # Each pattern has to be converted to a platform-specific path
            filelist = glob(os.path.join(src_dir, convert_path(pattern)))
            # Files that match more than one pattern are only added once
            files.extend([fn for fn in filelist if fn not in files])
        return files

