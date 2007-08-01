# Script which wrap easy install with some post-processing

__requires__ = 'setuptools'
import sys, os


def main(argv=None, **kw):
    from setuptools import setup
    from setuptools.dist import Distribution
    import distutils.core
    
    USAGE = """\
usage: %(script)s [options] requirement_or_url ...
   or: %(script)s --help
"""

    def gen_usage (script_name):
        script = os.path.basename(script_name)
        return USAGE % vars()

    def with_ei_usage(f):
        old_gen_usage = distutils.core.gen_usage
        try:
            distutils.core.gen_usage = gen_usage
            return f()
        finally:
            distutils.core.gen_usage = old_gen_usage

    class DistributionWithoutHelpCommands(Distribution):
        def _show_help(self,*args,**kw):
            with_ei_usage(lambda: Distribution._show_help(self,*args,**kw))

    if argv is None:
        argv = sys.argv[1:]

    with_ei_usage(lambda:
        setup(
            script_args = ['-q','alea_install', '-v']+argv,
            script_name = sys.argv[0] or 'alea_install',
            distclass=DistributionWithoutHelpCommands, **kw
        )
    )

