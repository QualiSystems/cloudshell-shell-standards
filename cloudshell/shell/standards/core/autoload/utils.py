#!/usr/bin/python
# -*- coding: utf-8 -*-
from cloudshell.shell.core.driver_context import AutoLoadDetails, AutoLoadResource, AutoLoadAttribute


class AutoloadDetailsBuilder(object):
    def __init__(self, resource_model):
        """
        :param cloudshell.shell_standards.autoload_generic_models.GenericResourceModel resource_model:
        """
        self.resource_model = resource_model

    def _build_branch(self, resource):
        """
        :type resource: cloudshell.shell.standards.core.autoload.resource_model.AbstractResource
        :rtype: cloudshell.shell.core.driver_context.AutoLoadDetails
        """
        resource.shell_name = resource.shell_name or self.resource_model.shell_name
        autoload_details = AutoLoadDetails([AutoLoadResource(model=resource.resource_model,
                                                             name=resource.name,
                                                             relative_address=resource.relative_address,
                                                             unique_identifier=resource.unique_identifier)],
                                           [AutoLoadAttribute(relative_address=resource.relative_address,
                                                              attribute_name=str(name),
                                                              attribute_value=value) for name, value in
                                            resource.attributes.items()]
                                           )
        for child_resource in resource.extract_sub_resources():
            child_details = self._build_branch(child_resource)
            autoload_details.resources.extend(child_details.resources)
            autoload_details.attributes.extend(child_details.attributes)
        return autoload_details

    def build_details(self):
        """
        Build resource details
        :rtype: cloudshell.shell.core.driver_context.AutoLoadDetails
        """
        return self._build_branch(self.resource_model)
