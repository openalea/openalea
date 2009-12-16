"""Functionalities to parse configuration file"""



def read_metainfo(filename, section='metainfo'):
    """Parse a section in a given file using ConfigParser module

    This function read a file (called `filename`), which must have a format 
    compatible with ConfigParser::

        [metainfo]
        option1 = string1
        option2 = string2
        ...

    Then, it parses the section [metainfo] that must be present and returns a dictionary
    containing all these options.

    :param filename: a filename with ConfigParser format
    :param section: a section to look for in the file
    :mode sphinx: a string in ["sphinx", "setup"] to return different information

    :Example:

        read_metainfo('metainfo.ini', metainfo='metainfo')

    :author: Thomas Cokelaer <Thomas Cokelaer __at__ sophis inria fr>
    """
    from openalea.misc.console import nocolor, red, color_terminal, blue, green, purple
    if not color_terminal():
        nocolor()

    print green('Reading metainfo ')
    import ConfigParser 
    config = ConfigParser.RawConfigParser()
    res = config.read(filename)
    if len(res)==0:
        raise IOError("Input file %s does not seem to exist" % filename)

    metadata = {}

    for option in config.options(section):
        print green('...%s: %s' % (option, config.get(section, option)))
        metadata[option] = config.get(section, option)

    return metadata
