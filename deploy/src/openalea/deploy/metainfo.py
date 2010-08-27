"""Functionalities to parse configuration file"""



compulsary_words = ['project','version','authors','package','release']

def read_metainfo(filename, section='metainfo', verbose=False):
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
    global compulsary_words
    try:
        from openalea.misc.console import nocolor, color_terminal, green
        if not color_terminal():
            nocolor()
    except:
        green =  lambda x: x

    if verbose:
        print green('Reading metainfo ')
    import ConfigParser 
    config = ConfigParser.RawConfigParser()
    res = config.read(filename)
    if len(res)==0:
        raise IOError("Input file %s does not seem to exist" % filename)

    metadata = {}

    for option in config.options(section):
        if verbose:
            print green('...%s: %s' % (option, config.get(section, option)))
        metadata[option] = config.get(section, option)

    if 'project' in metadata.keys():
        if metadata['project'] not in ['vplants','openalea','alinea']:
            raise ValueError('option project (openalea/vplants/alinea) not found in metainfo.ini file')
    else:
        raise ValueError('option project (openalea/vplants/alinea) not found in metainfo.ini file')

    for word in compulsary_words:
        if word not in metadata.keys():
            raise ValueError('%s field not found in metainfo.ini' % word)

    return metadata

