#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""
Manage plugins via the API connector
"""

def plugin_r_url(
        plugin : 'meerschaum.Plugin or str'
    ) -> str:
    """
    Generate a relative URL path from a Pipe's keys.
    """
    return f'/mrsm/plugins/{plugin}'

def register_plugin(
        self,
        plugin : 'meerschaum.Plugin',
        make_archive : bool = True,
        debug : bool = False
    ) -> tuple:
    """
    Register a plugin and upload its archive
    """
    import json
    if make_archive: archive_path = plugin.make_tar(debug=debug)
    else: archive_path = plugin.archive_path
    file_pointer = open(archive_path, 'rb')
    files = {'archive' : file_pointer}
    metadata = {
        'version' : plugin.version,
        'attributes': json.dumps(plugin.attributes),
    }
    r_url = plugin_r_url(plugin)
    try:
        response = self.post(r_url, files=files, params=metadata)
    except:
        success, msg = False, f"Failed to register plugin '{plugin}'"
    finally:
        file_pointer.close()

    try:
        success, msg = json.loads(response.text)
    except:
        success, msg = False, response.text

    return success, msg

def install_plugin(
        self,
        name : str,
        debug : bool = False
    ) -> tuple:
    """
    Download and attempt to install a plugin from the API
    """
    import os, pathlib
    from meerschaum import Plugin
    from meerschaum.config._paths import PLUGINS_TEMP_RESOURCES_PATH
    from meerschaum.utils.debug import dprint
    r_url = plugin_r_url(name)
    dest = pathlib.Path(os.path.join(PLUGINS_TEMP_RESOURCES_PATH, name + '.tar.gz'))
    if debug: dprint(f"Fetching from '{r_url}' to '{dest}'")
    archive_path = self.wget(r_url, dest) 
    plugin = Plugin(name, archive_path=archive_path)
    return plugin.install(debug=debug)

def get_plugins(
        self,
        debug : bool = False
    ) -> list:
    """
    Return a list of registered plugins
    """
    import json
    from meerschaum.utils.warnings import warn, error
    response = self.get('/mrsm/plugins')
    plugins = json.loads(response.text)
    if not isinstance(plugins, list): error(response.text)
    return plugins

