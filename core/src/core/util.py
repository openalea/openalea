import warnings
import datetime
import traceback
import os

def warn_deprecated(old_name, new_name, date=None):
    """
    :param date: (yyyy, mm, dd) ex: (2014, 9, 25) for 2014, 25th of september
    """
    tb = traceback.extract_stack()
    if date:
        final_date = datetime.date(*date) + datetime.timedelta(30) # deleted after 30 days
        datemsg = 'on %s' % (final_date)
    else:
        datemsg = 'soon'

    if 'OA_CLICOLOR' in os.environ:
        msg = "\n\033[93m%r is deprecated and will be removed \033[91m%s.\033[0m. Use %r instead. " % (old_name, datemsg, new_name)
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


