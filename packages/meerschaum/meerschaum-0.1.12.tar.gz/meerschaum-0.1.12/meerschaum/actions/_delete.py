#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""
Functions for deleting elements
"""

def delete(
        action : list = [''],
        **kw
    ):
    """
    Delete an element.
    """
    from meerschaum.utils.misc import choose_subaction
    from meerschaum.utils.debug import dprint
    options = {
        'config'  : _delete_config, 
        'pipes'   : _delete_pipes,
        'plugins' : _delete_plugins,
    }
    return choose_subaction(action, options, **kw)

def _delete_pipes(
        debug : bool = False,
        yes : bool = False,
        force : bool = False,
        **kw
    ) -> tuple:
    from meerschaum import get_pipes
    from meerschaum.utils.misc import yes_no
    import pprintpp
    pipes = get_pipes(as_list=True, debug=debug, **kw)
    if len(pipes) == 0:
        return False, "No pipes to delete"
    question = "Are you sure you want to delete these Pipes? THIS CANNOT BE UNDONE!\n"
    for p in pipes:
        question += f" - {p}" + "\n"
    answer = force
    if not yes and not force:
        answer = yes_no(question, default='n')
    if not answer:
        return False, "No pipes deleted."
    for p in pipes:
        success_tuple = p.delete(debug=debug)
        if not success_tuple[0]:
            return success_tuple

    return True, "Success"

def _delete_config(
        yes : bool = False,
        force : bool = False,
        debug : bool = False,
        **kw
    ) -> tuple:
    """
    Delete configuration files
    """
    import os
    from meerschaum.utils.misc import yes_no
    from meerschaum.config._paths import CONFIG_PATH, STACK_COMPOSE_PATH, DEFAULT_CONFIG_PATH
    from meerschaum.utils.debug import dprint
    paths = [CONFIG_PATH, STACK_COMPOSE_PATH, DEFAULT_CONFIG_PATH]
    answer = False
    if not yes:
        sep = '\n' + '  - '
        answer = yes_no(f"Delete files?{sep + sep.join([str(p) for p in paths])}\n", default='n')

    if answer or force:
        for path in paths:
            if debug: dprint(f"Removing {path}...")
            if os.path.isfile(path):
                os.remove(path)
    else:
        msg = "Nothing deleted."
        if debug: dprint(msg)
        return False, msg
    
    return True, "Successfully deleted configuration files"

def _delete_plugins(
        action : list = [''],
        yes : bool = False,
        force : bool = False,
        debug : bool = False,
        **kw
    ) -> tuple:
    import meerschaum.actions
    from meerschaum.actions import _plugins_names, plugins_modules
    from meerschaum.config._paths import PLUGINS_RESOURCES_PATH
    from meerschaum.utils.warnings import warn, error
    from meerschaum.utils.misc import yes_no, reload_package
    import os, shutil

    ### parse the provided plugins and link them to their modules
    modules_to_delete = dict()
    for plugin in action:
        if plugin not in _plugins_names: warn(f"Plugin '{plugin}' is not installed. Ignoring...")
        else:
            for m in plugins_modules:
                if plugin == m.__name__.split('.')[-1]:
                    modules_to_delete[plugin] = m
                    break
    if len(modules_to_delete) == 0: return False, "No plugins to delete."

    ### verify that the user absolutely wants to do this (skips on --force)
    question = "Are you sure you want to delete these plugins?\n"
    for plugin in modules_to_delete:
        question += f" - {plugin}" + "\n"
    answer = force
    if not yes and not force:
        answer = yes_no(question, default='n')
    if not answer:
        return False, "No plugins deleted."

    ### delete the folders or files
    for name, m in modules_to_delete.items():
        try:
            if '__init__.py' in m.__file__:
                shutil.rmtree(m.__file__.replace('__init__.py', ''))
            else:
                os.remove(m.__file__)
        except:
            return False, f"Could not remove plugin '{name}'"

    reload_package(meerschaum.actions)
    return True, "Success"

### NOTE: This must be the final statement of the module.
###       Any subactions added below these lines will not
###       be added to the `help` docstring.
from meerschaum.utils.misc import choices_docstring as _choices_docstring
delete.__doc__ += _choices_docstring('delete')
