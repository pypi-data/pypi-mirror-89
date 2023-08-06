# -*- coding: utf-8 -*-

from abc import abstractmethod

from pip_services3_commons.config import ConfigParams
from pip_services3_commons.refer import IReferences, Descriptor

from .IFacadeService import IFacadeService
from .FacadeService import FacadeService


class PartitionFacadeService(FacadeService):
    _parent: IFacadeService

    def __init__(self):
        super(PartitionFacadeService, self).__init__()
        self._dependency_resolver.put('parent', Descriptor('pip-services', 'facade-service', 'default', '*', '*'))

    def configure(self, config):
        super().configure(config)
        self._dependency_resolver.configure(config)

    def set_references(self, references):
        super().set_references(references)
        self._parent = self._dependency_resolver.get_one_required('parent')
        self._parent.register_middleware_for_path(self._root_path, self._partition)
        self._register()

    def get_root_path(self):
        return self._parent.get_root_path() + self._root_path

    def _register(self):
        """
        Override in child classes
        """
