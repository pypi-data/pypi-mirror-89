# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

from pip_services3_commons.config import IConfigurable, ConfigParams
from pip_services3_commons.refer import Descriptor, IReferences, IReferenceable, DependencyResolver
from pip_services3_components.count import CompositeCounters
from pip_services3_components.log import CompositeLogger

from ..services.IFacadeService import IFacadeService


class FacadeRoutes(ABC, IConfigurable, IReferenceable):
    _logger = CompositeLogger()
    _counters = CompositeCounters()
    _dependencyResolver = DependencyResolver()
    _service: IFacadeService

    def __init__(self):
        self._dependencyResolver.put("service", Descriptor("pip-services-facade", "service", "*", "*", "*"))

    def configure(self, config):
        self._dependencyResolver.configure(config)

    def set_references(self, references):
        self._logger.set_references(references)
        self._counters.set_references(references)
        self._dependencyResolver.set_references(references)
        self._service = self._dependencyResolver.get_one_required('service')

        self._register()

    def instrument(self, correlation_id, method, route):
        self._logger.debug(correlation_id, "Calling {} {}", method, route)
        self._counters.increment_one(route + "." + method + ".calls")

    def get_correlation_id(self, req):
        return req.query.get("correlation_id")

    def register_route(self, method, route, action):

        def action_curl(req=None, res=None):
            correlation_id = self.get_correlation_id(req)
            self.instrument(correlation_id, method, route)
            action(req, res)

        self._service.register_route(method, route, action_curl)

    @abstractmethod
    def _register(self):
        pass
