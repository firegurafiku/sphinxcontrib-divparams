import os as _os
from . import implementation as _impl


def get_templates_path():
    """
    Returns path to directory where `divparams` extension has HTML template
    files installed. This directory must be added to `templates_path`
    configuration variable for the extension to operate properly.

    :rtype: str
    """
    return _os.path.join(
        _os.path.dirname(_os.path.abspath(__file__)), "_templates")


def get_static_path():
    """
    Returns path to directory where `divparams` extension has static
    files installed. This directory must be added to `html_static_path`
    configuration variable for the extension to operate properly.

    :rtype: str
    """
    return _os.path.join(
        _os.path.dirname(_os.path.abspath(__file__)), "_static")


def setup(app):
    app.connect("build-finished", _impl.process_build_finished)
