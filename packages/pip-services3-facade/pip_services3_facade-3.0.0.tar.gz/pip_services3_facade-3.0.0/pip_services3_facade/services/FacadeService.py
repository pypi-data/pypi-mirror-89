# -*- coding: utf-8 -*-

import bottle
from beaker.middleware import SessionMiddleware

from pip_services3_commons.config import IConfigurable, ConfigParams
from pip_services3_commons.refer import IReferences, IReferenceable, DependencyResolver
from pip_services3_components.log import CompositeLogger

from .IFacadeService import IFacadeService


class FacadeService(IConfigurable, IReferenceable, IFacadeService):
    _root_path = ''
    _partition = SessionMiddleware(bottle.Bottle(catchall=True, autojson=True)).app
    _dependency_resolver = DependencyResolver()
    _logger = CompositeLogger()

    def configure(self, config):
        self._root_path = config.get_as_string_with_default('root_path', self._root_path)
        if len(self._root_path) > 0 and not (self._root_path.startswith('/')):
            self._root_path = '/' + self._root_path

    def set_references(self, references):
        self._dependency_resolver.set_references(references)
        self._logger.set_references(references)

    def get_root_path(self):
        return self._root_path

    def register_middleware(self, action):
        self._partition.add_hook('before_request', action)

    def register_middleware_for_path(self, path, action):
        self._partition.add_hook('before_request', lambda: action() if not (
                path is not None and path != '' and bottle.request.url.startswith(path)) else None)

    def register_route(self, method, route, action):
        if method == 'del':
            method = 'delete'

        self._logger.debug(None, 'Registering route {} {}', method, self.get_root_path() + route)
        self._partition.route(route, method, action)

    def register_route_with_auth(self, method, route, action, authorize):
        if method == 'del':
            method = 'delete'

        self._logger.debug(None, 'Registering route {} {}', method, self.get_root_path() + route)
        self._partition.route(route, method, action, authorize=authorize)
