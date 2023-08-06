# -*- coding: utf-8 -*-

"""Information related functions."""

import os
import platform
from platform import python_version
import types


def map_module_names(key: str) -> str:
    """ Map typical module shortcuts to module names.

    :param key: module shortcut.
    :return: longname of module.
    """
    mapping = {
        'cv2': 'openCV',
        'jcinfo': 'jupyter_commons.info',
        'jcout': 'jupyter_commons.output',
        'xsysutils': 'xutilities.sysutils',
        'np': 'numpy',
        'nx': 'networkX',
        'pd': 'pandas',
        'plt': 'matplotlib.pyplot',
    }
    if key in mapping.keys():
        name = f'{mapping[key]}({key})'
    else:
        name = key
    return name


def get_version(key: str, module: types.ModuleType) -> str:
    """Get version info of module key.

    :param key: module shortcut.
    :param module: the module.
    :return: version info.
    """
    if key == 'plt':
        from matplotlib import __version__ as matplotlib_version
        return matplotlib_version
    if key in ('jcinfo', 'jcout'):
        from jupyter_commons import __version__ as jupyter_commons_version
        return jupyter_commons_version
    if key in ('xsysutils',):
        from xutilities import __version__ as xutilities_version
        return xutilities_version
    return module.__version__


def system_info(globs: dict) -> None:
    """ Print versions of imported packages.

    Looks for select packages if imported and prints version info.

    :param globs: globals() of calling code.
    """
    print("-- System --")
    print("os name: %s" % os.name)
    print("system: %s" % platform.system())
    print("release: %s" % platform.release())
    print()
    print("-- Python --")
    print("version: %s" % python_version())
    print()
    print("-- Python Packages --")
    for key, item in globs.items():
        if isinstance(item, types.ModuleType):
            try:
                base_key = key.split('.')[0]
                name = map_module_names(base_key)
                print(f"{name}=={get_version(key, item)}")
            except AttributeError:
                # Ignore modules w/o __version__ info
                pass
