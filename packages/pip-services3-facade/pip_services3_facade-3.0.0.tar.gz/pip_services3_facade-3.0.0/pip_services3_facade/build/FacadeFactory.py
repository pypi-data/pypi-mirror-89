# -*- coding: utf-8 -*-
from pip_services3_commons.refer.Descriptor import Descriptor
from pip_services3_components.build import Factory

from ..services.MainFacadeService import MainFacadeService
from ..services.PartitionFacadeService import PartitionFacadeService

from ..operations.AboutOperations import AboutOperations


class FacadeFactory(Factory):
    descriptor = Descriptor("pip-services", "factory", "facade", "default", "1.0")
    main_facade_service_descriptor = Descriptor("pip-services", "facade-service", "default", "*", "1.0")
    partition_facade_service_descriptor = Descriptor("pip-services", "facade-partition", "default", "*", "1.0")
    auth_manager_descriptor = Descriptor("pip-service", "facade-authorization", "default", "*", "1.0")
    session_manager_descriptor = Descriptor("pip-services", "facade-session", "default", "*", "1.0")
    about_operations_descriptor = Descriptor("pip-services", "facade-operations", "about", "*", "1.0")

    def __init__(self):
        super(FacadeFactory, self).__init__()
        self.register_as_type(FacadeFactory.main_facade_service_descriptor, MainFacadeService)
        self.register_as_type(FacadeFactory.partition_facade_service_descriptor, PartitionFacadeService)
        self.register_as_type(FacadeFactory.about_operations_descriptor, AboutOperations)
