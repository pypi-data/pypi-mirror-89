"""The :mod:`unimatrix.runtime` package provides a common interface to set
up the application runtime environment.
"""
import pkg_resources

import ioc


IS_CONFIGURED = False


def get_entrypoints(name):
    entrypoints = [
        (entry_point.name, entry_point.load())
        for entry_point
        in pkg_resources.iter_entry_points(name)
    ]
    return sorted(entrypoints, key=lambda x: getattr(x[1], 'WEIGHT', 0))


def setup():
    """Setup all :mod:`unimatrix` components."""
    global IS_CONFIGURED
    if IS_CONFIGURED:
        return

    ioc.setup()

    IS_CONFIGURED = True


def teardown():
    """Teardown all :mod:`unimatrix` components."""
    for name, module in get_entrypoints('unimatrix.runtime'):
        if not hasattr(module, 'on_teardown'):
            continue
        module.on_teardown()
