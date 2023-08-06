# -*- coding: utf-8 -*-
import socket
import sys
import time
from threading import Thread

from bottle import response, request

from pip_services3_commons.config import ConfigParams
from pip_services3_commons.errors import ConfigException
from pip_services3_commons.refer import IReferences
from pip_services3_commons.run import IOpenable
from pip_services3_components.auth import CredentialParams, CredentialResolver
from pip_services3_components.connect import ConnectionParams, ConnectionResolver

from pip_services3_rpc.services import SSLCherryPyServer

from .FacadeService import FacadeService


class MainFacadeService(FacadeService, IOpenable):
    _default_config = ConfigParams.from_tuples(
        'root_path', '',

        'connection.protocol', 'http',
        'connection.hostname', '0.0.0.0',
        'connection.port', 8080,

        'credential.ssl_key_file', None,
        'credential.ssl_crt_file', None,
        'credential.ssl_ca_file', None,

        'options.debug', True,
        'options.maintenance_enabled', False,
        'options.max_sockets', 50,
        'options.max_req_size', '1mb'
    )

    __server = None
    __service = None
    __http = None
    __connection_resolver = ConnectionResolver()
    __credential_resolver = CredentialResolver()

    __debug = True
    __maintance_enabled = False
    __max_sockets = 50
    __max_req_size = '1mb'

    def __init__(self):
        super(MainFacadeService, self).__init__()
        self._root_path = ''
        # bottle app
        self.__service = super()._partition

    def is_maintance_enabled(self) -> bool:
        return self.__maintance_enabled

    def set_maintance_enabled(self, value: bool):
        self.__maintance_enabled = True

    def configure(self, config):
        config = config.set_defaults(MainFacadeService._default_config)
        self.__connection_resolver.configure(config)
        self.__credential_resolver.configure(config)

        self._root_path = config.get_as_string_with_default('root_path', self._root_path)
        if len(self._root_path) > 0 and not (self._root_path.startswith('/')):
            self._root_path = '/' + self._root_path

        self.__debug = config.get_as_boolean_with_default('options.debug', self.__debug)
        self.__maintance_enabled = config.get_as_boolean_with_default('options.maintenance_enabled',
                                                                      self.__maintance_enabled)
        self.__max_sockets = config.get_as_integer_with_default('options.max_sockets', self.__max_sockets)
        self.__max_req_size = config.get_as_string_with_default('options.max_req_size', self.__max_req_size)

    def set_references(self, references):
        super().set_references(references)
        self.__connection_resolver.set_references(references)
        self.__credential_resolver.set_references(references)

    def is_open(self):
        return self.__http is not None

    def open(self, correlation_id):
        if self.__http is not None:
            return

        connection = self._get_connetcion(correlation_id)
        credential = self._get_credential(correlation_id, connection)
        self.__server = self.__create_server(connection, credential)
        self.__configure_service()
        host = connection.get_host()
        host_name = socket.gethostname()
        port = connection.get_port()
        self.__server.host = host
        self.__server.port = port

        def start_server():
            try:
                self.__service.run(server=self.__server, debug=self.__debug)
            except Exception as ex:
                self._logger.error(correlation_id, ex, 'Failed to start HTTP server at {}:{}', host_name, port)

        # Start server in thread
        Thread(target=start_server, daemon=True).start()
        # Time for start server
        time.sleep(0.01)
        self._logger.info(correlation_id, 'Started HTTP server {}:{}', host_name, port)

    def close(self, correlation_id):
        try:
            if self.__server is not None:
                self.__server.shutdown()
                self.__service.close()
                self._logger.debug(correlation_id, "Closed HTTP server")

            self.__server = None
            self.__service = None

        except Exception as ex:
            self._logger.warn(correlation_id, "Failed while closing HTTP server: " + str(ex))

    def _get_connetcion(self, correlation_id):
        connection = self.__connection_resolver.resolve(correlation_id)

        # Check for connection
        if connection is None:
            raise ConfigException(correlation_id, "NO_CONNECTION", "Connection for REST client is not defined")
        else:
            # Check for type
            protocol = connection.get_protocol('http')
            if 'http' != protocol and 'https' != protocol:
                raise ConfigException(
                    correlation_id, "WRONG_PROTOCOL", "Protocol is not supported by REST connection").with_details(
                    "protocol", protocol)
            # Check for host
            elif connection.get_host() is None:
                raise ConfigException(correlation_id, "NO_HOST", "No host is configured in REST connection")
            # Check for port
            elif connection.get_port() == 0:
                raise ConfigException(correlation_id, "NO_PORT", "No port is configured in REST connection")

        return connection

    def _get_credential(self, correlation_id, connection):
        # Credentials are not required unless HTTPS is used
        if connection.get_protocol('http') != 'https':
            return

        credential = self.__credential_resolver.lookup(correlation_id)
        # Check for connection
        if credential is None:
            raise ConfigException(correlation_id, "NO_CREDENTIAL",
                                  "SSL certificates are not configured for HTTPS protocol")
        else:
            if credential.get_as_nullable_string('ssl_key_file') is None:
                raise ConfigException(correlation_id, "NO_SSL_KEY_FILE",
                                      "SSL key file is not configured in credentials")
            elif credential.get_as_nullable_string('ssl_crt_file') is None:
                raise ConfigException(correlation_id, "NO_SSL_CRT_FILE",
                                      "SSL crt file is not configured in credentials")

        return credential

    def __create_server(self, connection, credential):
        if connection.get_protocol('http') == 'https':

            if connection.get_protocol('http') == 'https':
                ssl_key_file = credential.get_as_nullable_string('ssl_key_file')
                with open(ssl_key_file, 'rb') as file:
                    private_key = file.read()

                ssl_crt_file = credential.get_as_nullable_string('ssl_crt_file')
                with open(ssl_crt_file, 'rb') as file:
                    certfile = file.read()

                # ca = []
                #
                # ssl_ca_file = credential.get_as_nullable_string('ssl_ca_file')
                # if ssl_ca_file is not None:
                #     with open(ssl_ca_file, 'rb') as file:
                #         ca_text = file.read()
                #         while ca_text is not None and len(ca_text.strip()) > 0:
                #             crt_index = ca_text.rindex(b'-----BEGIN CERTIFICATE-----')
                #             if crt_index > -1:
                #                 ca.append(ca_text[crt_index:])
                #                 ca_text = ca_text[0:crt_index]

                return SSLCherryPyServer(certfile=certfile,
                                         keyfile=private_key,
                                         request_queue_size=self.__max_sockets,
                                         max_request_body_size=self.__max_req_size)

        return SSLCherryPyServer(request_queue_size=self.__max_sockets,
                                 max_request_body_size=self.__max_req_size)

    def __configure_service(self):
        self.__service.config['catchall'] = True
        self.__service.config['autojson'] = True

        # Enable CORS requests
        self.__service.add_hook('after_request', self.__enable_cors)

        self.__service.add_hook('after_request', self.__do_maintance)
        self.__service.add_hook('after_request', self.__no_cache)

    def __enable_cors(self):
        response.headers['Access-Control-Max-Age'] = '5'
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
        response.headers[
            'Access-Control-Allow-Headers'] = 'Authorization, Origin, Accept, Content-Type, X-Requested-With'

    def __do_maintance(self):
        """
        :return: maintenance error code
        """
        # Make this more sophisticated
        if self.__maintance_enabled:
            response.headers['Retry-After'] = 3600
            response.status = 503

    def __no_cache(self):
        """
        Prevents IE from caching REST requests
        """
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = 0
