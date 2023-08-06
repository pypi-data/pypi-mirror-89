# -*- coding: utf-8 -*-

from abc import ABC


class IFacadeService(ABC):

    def get_root_path(self) -> str:
        raise NotImplementedError('Method from interface definition')

    def register_middleware(self, action):
        raise NotImplementedError('Method from interface definition')

    def register_middleware_for_path(self, path: str, action):
        raise NotImplementedError('Method from interface definition')

    def register_route(self, method: str, route: str, action):
        raise NotImplementedError('Method from interface definition')

    def register_route_with_auth(self, method: str, route: str, action, authorize):
        raise NotImplementedError('Method from interface definition')
