#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""
Generic interface for plugins
"""

import sys
from meerschaum.config._paths import PLUGINS_RESOURCES_PATH
if PLUGINS_RESOURCES_PATH not in sys.path: sys.path.append(str(PLUGINS_RESOURCES_PATH))
from meerschaum.connectors._Connector import Connector

class PluginConnector(Connector):

    def __init__(
        self,
        label : str,
        debug : bool = False,
        **kw
    ):
        super().__init__('plugin', label=label, **kw)

        import os, pathlib
        from meerschaum.utils.warnings import error, warn
        self.resource_path = None
        for _plugin in os.listdir(PLUGINS_RESOURCES_PATH):
            plugin = _plugin.replace('.py', '')
            if plugin == self.label:
                self.resource_path = pathlib.Path(os.path.join(PLUGINS_RESOURCES_PATH, plugin))
        if not self.resource_path:
            error(f"Plugin '{self.label}' cannot be found. Is it installed?")

        self.fetch = None
        try:
            exec(f'from {self.label} import fetch; self.fetch = fetch')
        except:
            pass

        self.sync = None
        try:
            exec(f'from {self.label} import sync; self.sync = sync')
        except:
            pass

        if self.fetch is None and self.sync is None:
            error(f"Could not import `fetch()` or `sync()` methods for plugin '{self.label}'")

