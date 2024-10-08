# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Graz University of Technology.
#
# Invenio-Curations is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Curations related generators."""

from flask_principal import RoleNeed
from invenio_access.permissions import system_identity
from invenio_records_permissions.generators import ConditionalGenerator, Generator

from ..proxies import current_curations_service


class IfRequestTypes(ConditionalGenerator):
    """Request-oriented generator checking for requests of certain types."""

    def __init__(self, request_types, then_, else_):
        """Constructor."""
        self.request_types = set(request_types)
        super().__init__(then_, else_)

    def _condition(self, request=None, **kwargs):
        """Check if the request type matches a configured type."""
        if request is not None:
            for request_type in self.request_types:
                if isinstance(request.type, request_type):
                    return True

        return False


class IfCurationRequestAccepted(ConditionalGenerator):
    """Request-oriented generator checking if a curation request has been accepted."""

    def __init__(
        self,
        record_access_func=lambda request: request.topic.resolve(),
        then_=None,
        else_=None,
    ):
        """Constructor."""
        self.record_access_func = record_access_func
        super().__init__(then_ or [], else_ or [])

    def _condition(self, request=None, **kwargs):
        """Check if the curation request for the record has been accepted."""
        if request is not None:
            record_to_curate = self.record_access_func(request)
            return (
                current_curations_service.accepted_record(
                    system_identity, record_to_curate
                )
                is not None
            )

        return False


class CurationModerators(Generator):
    """Permission generator that allows users with the `moderation` role."""

    def needs(self, **kwargs):
        """Allow access for the moderation role."""
        return [RoleNeed(current_curations_service.moderation_role_name)]


class IfCurationRequestExists(ConditionalGenerator):
    """Record-oriented generator checking if a curation request exists."""

    def _condition(self, record=None, **kwargs):
        """Check if the record has a curation request or not."""
        if record is not None:
            # We use the system identity here to avoid visibility issues
            request = current_curations_service.get_review(
                identity=system_identity, topic=record
            )
            return request is not None

        return False
