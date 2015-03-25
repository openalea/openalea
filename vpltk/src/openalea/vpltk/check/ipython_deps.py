def has_zmq():
    """
    Check if User can import Python ZeroMQ

    :return: True if user can use Python ZeroMQ. Else False.
    """
    try:
        import zmq
        return True
    except ImportError:
        return False


def has_pygments():
    """
    Check if User can import Pygments

    :return: True if user can use Pygments. Else False.
    """
    try:
        import pygments
        return True
    except ImportError:
        return False


def has_full_deps():
    """
    Check if User can use IPython shell embeded in OpenAlea.

    Check zmq, pygments

    :return: True if user has zmq and pygments. Else False.
    """
    # Check Python ZeroMQ
    zmq = has_zmq()
    # Check Pygments
    pgm = has_pygments()

    return zmq & pgm

has_full_deps()
