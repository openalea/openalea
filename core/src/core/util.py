import warnings
import datetime
import traceback
import os

def camel_case_to_lower(name):
    """

    :Examples:

    >>> camel_case_to_lower('squareRoot')
    'square_root'

    >>> camel_case_to_lower('SquareRoot')
    'square_root'

    >>> camel_case_to_lower('ComputeSQRT')
    'compute_sqrt'

    >>> camel_case_to_lower('SQRTCompute')
    'sqrt_compute'
    """
    lowername = '_'
    index = 0
    while index < len(name):
        if name[index].islower():
            lowername += name[index]
            index += 1
        else:
            if not name[index] == '_':
                if not lowername[-1] == '_':
                    lowername += '_'
                lowername += name[index].lower()
                index += 1
                if index < len(name) and not name[index].islower():
                    while index < len(name) and not name[index].islower():
                        lowername += name[index].lower()
                        index += 1
                    if index < len(name):
                        lowername = lowername[:-1] + '_' + lowername[-1]
            else:
                if not lowername[-1] == '_':
                    lowername += '_'
                index += 1
    lowername = lowername.lstrip('_')
    return lowername

def camel_case_to_upper(name):
    """

    :Examples:

    >>> camel_case_to_upper('squareRoot')
    'SQUARE_ROOT'

    >>> camel_case_to_upper('SquareRoot')
    'SQUARE_ROOT'

    >>> camel_case_to_upper('ComputeSQRT')
    'COMPUTE_SQRT'

    >>> camel_case_to_upper('SQRTCompute')
    'SQRT_COMPUTE'

    >>> camel_case_to_upper('Char_U')
    """
    lowername = '_'
    index = 0
    while index < len(name):
        if name[index].islower():
            lowername += name[index].upper()
            index += 1
        else:
            if not name[index] == '_':
                if not lowername[-1] == '_':
                    lowername += '_'
                lowername += name[index].upper()
                index += 1
                if index < len(name) and not name[index].islower():
                    while index < len(name) and not name[index].islower():
                        lowername += name[index]
                        index += 1
                    if index < len(name):
                        lowername = lowername[:-1] + '_' + lowername[-1]
            else:
                if not lowername[-1] == '_':
                    lowername += '_'
                index += 1
    lowername = lowername.lstrip('_')
    return lowername

def to_camel_case(name):
    """

    :Examples:

    >>> lower_to_camel_case(camel_case_to_lower('squareRoot'))
    'SquareRoot'

    >>> lower_to_camel_case(camel_case_to_lower('SquareRoot'))
    'SquareRoot'

    >>> lower_to_camel_case(camel_case_to_lower('ComputeSQRT'))
    'ComputeSqrt'

    >>> lower_to_camel_case(camel_case_to_lower('SQRTCompute'))
    'SqrtCompute'
    """
    camelname = ''
    index = 0
    while index < len(name):
        if name[index] == '_':
            index += 1
            while index < len(name) and name[index] == '_':
                index += 1
            if index < len(name):
                camelname += name[index].upper()
        else:
            camelname += name[index]
        index += 1
    if camelname[0].islower():
       camelname  = camelname[0].upper() + camelname[1:]
    return camelname

def warn_deprecated(old_name, new_name, date=None):
    """
    :param date: (yyyy, mm, dd) ex: (2014, 9, 25) for 2014, 25th of september
    """
    tb = traceback.extract_stack()
    if date:
        final_date = datetime.date(*date) + datetime.timedelta(100) # deleted after 100 days
        datemsg = 'on %s' % (final_date)
    else:
        datemsg = 'soon'

    if 'OA_CLICOLOR' in os.environ:
        msg = "\n\033[93m%r is deprecated and will be removed \033[91m%s.\033[0m. Use %r instead. " % (
            old_name, datemsg, new_name)
    else:
        msg = "\n%r is deprecated and will be removed %s. Use %r instead. " % (old_name, datemsg, new_name)

    for i in range(0, len(tb) - 3):
        filename, lineno, caller, line = tb[i]
        msg += '\n' + ' ' * i + '%s:%s - %s' % (filename, lineno, line)
    if 'OA_RAISE_ON_WARNING' in os.environ:
        warnings.warn(msg, stacklevel=3)
        raise IOError
    else:
        warnings.warn(msg, stacklevel=3)
