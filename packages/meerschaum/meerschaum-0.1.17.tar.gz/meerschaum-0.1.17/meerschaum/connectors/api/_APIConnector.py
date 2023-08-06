#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""
Interact with the Meerschaum WebAPI with the APIConnector
"""

from meerschaum.connectors._Connector import Connector

required_attributes = {
    'host',
}

class APIConnector(Connector):

    from ._post import post
    from ._patch import patch
    from ._get import get, wget
    from ._actions import get_actions, do_action
    from ._pipes import (
        register_pipe,
        fetch_pipes_keys,
        edit_pipe,
        sync_pipe,
        delete_pipe,
        get_pipe_data,
        get_backtrack_data,
        get_pipe_id,
        get_pipe_attributes,
        get_sync_time,
        pipe_exists,
        create_metadata,
    )
    from ._fetch import fetch
    from ._plugins import register_plugin, install_plugin, get_plugins
    from ._users import get_users, login, edit_user, get_user_id, delete_user, register_user

    def __init__(
        self,
        label : str = 'main',
        debug : bool = False,
        **kw
    ):
        super().__init__('api', label=label, **kw)
        if 'protocol' not in self.__dict__:
            self.protocol = 'http'
        if 'port' not in self.__dict__:
            self.port = 8000
        self.verify_attributes(required_attributes)
        self.url = (
            self.protocol + '://' +
            self.host + ':' +
            str(self.port)
        )
        import requests, requests.auth
        self.auth = None
        self._token = None
        if 'username' in self.__dict__ and 'password' in self.__dict__:
            self.auth = requests.auth.HTTPBasicAuth(
                self.username,
                self.password
            )
        self.session = requests.Session()

    @property
    def token(self):
        if self._token is None:
            self.login()
        return self._token

