# -*- coding: utf-8 -*-

from abc import ABC

from pip_services3_commons.config import IConfigurable, ConfigParams
from pip_services3_commons.data import FilterParams, PagingParams
from pip_services3_commons.errors import BadRequestException, UnauthorizedException, NotFoundException, \
    ConflictException, UnknownException
from pip_services3_commons.refer import IReferences, IReferenceable, DependencyResolver
from pip_services3_components.count import CompositeCounters
from pip_services3_components.log import CompositeLogger
from pip_services3_rpc.services import HttpResponseSender


class FacadeOperations(ABC, IConfigurable, IReferenceable):
    _logger = CompositeLogger()
    _counters = CompositeCounters()
    _dependencyResolver = DependencyResolver()

    def configure(self, config):
        self._dependencyResolver.configure(config)

    def set_references(self, references):
        self._logger.set_references(references)
        self._counters.set_references(references)
        self._dependencyResolver.set_references(references)

    def _get_correlation_id(self, req):
        return req.query.get("correlation_id")

    def _get_filter_params(self, req):
        key_value_req = {}

        for key, value in req.query.items:
            if key not in ['skip', 'take', 'total']:
                key_value_req[key] = value

        filter = FilterParams.from_value(key_value_req)

        return filter

    def _get_paging_params(self, req):
        key_value_req = {}

        for key, value in req.query.items:
            if key in ['skip', 'take', 'total']:
                key_value_req[key] = value

        filter = FilterParams.from_value(key_value_req)

        return filter

    def _send_result(self, res):
        return HttpResponseSender.send_result(res)

    def _send_empty_result(self, res):
        return HttpResponseSender.send_empty_result(res)

    def _send_created_result(self, res):
        return HttpResponseSender.send_created_result(res)

    def _send_deleted_result(self, res):
        return HttpResponseSender.send_deleted_result(res)

    def _send_error(self, err):
        HttpResponseSender.send_error(err)

    def _send_bad_request(self, req, err, message):
        correlation_id = self._get_correlation_id(req)
        error = BadRequestException(correlation_id, 'BAD_REQUEST', message)
        self._send_error(error)

    def _send_unauthorized(self, req, message):
        correlation_id = self._get_correlation_id(req)
        error = UnauthorizedException(correlation_id, 'UNAUTHORIZED', message)
        self._send_error(error)

    def _send_not_found(self, req, message):
        correlation_id = self._get_correlation_id(req)
        error = NotFoundException(correlation_id, 'NOT_FOUND', message)
        self._send_error(error)

    def _send_conflict(self, req, message):
        correlation_id = self._get_correlation_id(req)
        error = ConflictException(correlation_id, 'CONFLICT', message)
        self._send_error(error)

    def _send_session_expired(self, req, message):
        correlation_id = self._get_correlation_id(req)
        error = UnknownException(correlation_id, 'SESSION_EXPIRED', message)
        error.status = 440
        self._send_error(error)

    def _send_internal_error(self, req, message):
        correlation_id = self._get_correlation_id(req)
        error = UnknownException(correlation_id, 'INTERNAL', message)
        self._send_error(error)

    def _send_server_unavailable(self, req, message):
        correlation_id = self._get_correlation_id(req)
        error = ConflictException(correlation_id, 'SERVER_UNAVAILABLE', message)
        error.status = 503
        self._send_error(error)
