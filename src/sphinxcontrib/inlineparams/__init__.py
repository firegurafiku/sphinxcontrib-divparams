import os as _os
from . import implementation as _impl


def get_path():
    """
    Returns path to directory where `inlineparams` extension is installed.
    This directory contains template files and stylesheets, and therefore must
    be added to `template` configuration variable.

    :rtype: str
    :return:
    Absolute path to directory directory where the source code of this
    Python module is located.
    """
    return _os.path.dirname(_os.path.abspath(__file__))


def setup(app):
    """

    :param app:
    :return:
    """
    app.connect("build-finished", _impl.process_build_finished)
    return {'version': "1.1",
            'parallel_read_safe': True}
