# Add header here
__all__ = ['get_plotters', 'register_plotter']
__registry = []


def register_plotter(plotter):
    """
    Register an instance of plotter (use for 3D Viewer)
    """
    __registry.append(plotter)


def get_plotters():
    return __registry