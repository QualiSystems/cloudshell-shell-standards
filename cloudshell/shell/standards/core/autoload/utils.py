#!/usr/bin/python
# -*- coding: utf-8 -*-
import warnings

from cloudshell.shell.core.driver_context import (
    AutoLoadAttribute,
    AutoLoadDetails,
    AutoLoadResource,
)


class AutoloadDetailsBuilder(object):
    def __init__(self, resource_model, filter_empty_modules=False):
        """Autoload Details Builder.

        :param cloudshell.shell_standards.autoload_generic_models.GenericResourceModel resource_model:  # noqa: E501
        :param bool filter_empty_modules:
        """
        if not filter_empty_modules:
            # todo v2.0 - set filter_empty_modules=True by default
            warnings.warn(
                "Empty modules would be filtered by default in next major version",
                PendingDeprecationWarning,
            )
        self.resource_model = resource_model
        self._filter_empty_modules = filter_empty_modules

    def _build_branch(self, resource):
        """Build a branch.

        :type resource: cloudshell.shell.standards.core.autoload.resource_model.AbstractResource  # noqa: E501
        :rtype: cloudshell.shell.core.driver_context.AutoLoadDetails
        """
        resource.shell_name = resource.shell_name or self.resource_model.shell_name
        relative_address = str(resource.relative_address)
        unique_identifier = str(resource.unique_identifier)

        autoload_details = AutoLoadDetails([], [])

        if relative_address:
            autoload_details.resources = [
                AutoLoadResource(
                    model=resource.cloudshell_model_name,
                    name=resource.name,
                    relative_address=relative_address,
                    unique_identifier=unique_identifier,
                )
            ]

        autoload_details.attributes = [
            AutoLoadAttribute(
                relative_address=relative_address,
                attribute_name=str(name),
                attribute_value=str(value),
            )
            for name, value in resource.attributes.items()
            if value is not None
        ]
        for child_resource in resource.extract_sub_resources():
            # skip modules and sub modules without children
            if self._filter_empty_modules and is_module_without_children(
                child_resource
            ):
                continue
            child_details = self._build_branch(child_resource)
            autoload_details.resources.extend(child_details.resources)
            autoload_details.attributes.extend(child_details.attributes)
        return autoload_details

    def build_details(self):
        """Build resource details.

        :rtype: cloudshell.shell.core.driver_context.AutoLoadDetails
        """
        return self._build_branch(self.resource_model)


def is_module_without_children(resource):
    from cloudshell.shell.standards.autoload_generic_models import (
        GenericModule,
        GenericSubModule,
    )

    children = resource.extract_sub_resources()
    if isinstance(resource, GenericSubModule):
        return not children
    elif isinstance(resource, GenericModule):
        return all(map(is_module_without_children, children))
    else:
        return False
