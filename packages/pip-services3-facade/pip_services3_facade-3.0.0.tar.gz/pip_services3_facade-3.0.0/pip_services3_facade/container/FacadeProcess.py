# -*- coding: utf-8 -*-

from pip_services3_container.ProcessContainer import ProcessContainer

from ..build.FacadeFactory import FacadeFactory


class FacadeProcess(ProcessContainer):

    def __init__(self):
        super(FacadeProcess, self).__init__('facade', 'Client facade microservice')
        self._factories.add(FacadeFactory())
