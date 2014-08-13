


def tutorials():
    from openalea.core.path import path
    try:
        from openalea import oalab
        from openalea.deploy.shared_data import shared_data
    except ImportError:
        return []
    else:
        oalab_dir = shared_data(oalab)
        return [path(oalab_dir)]
