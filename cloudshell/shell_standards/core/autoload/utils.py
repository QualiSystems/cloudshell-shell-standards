#!/usr/bin/python
# -*- coding: utf-8 -*-
from cloudshell.shell.core.driver_context import AutoLoadDetails, AutoLoadAttribute, AutoLoadResource


class AutoloadDetailsBuilder(object):

    @staticmethod
    def build_details(resource):
        """
        :type resource: cloudshell.shell_standards.core.resource_model.AbstractResource
        """
        autoload_details = AutoLoadDetails([AutoLoadResource(model=resource.resource_model,
                                                             name=resource.name,
                                                             relative_address=resource.relative_address,
                                                             unique_identifier=resource.unique_identifier)],
                                           [AutoLoadAttribute(relative_address=resource.relative_address,
                                                              attribute_name=name,
                                                              attribute_value=value) for name, value in
                                            resource.attributes.items()]
                                           )
        for child_resource in resource.extract_sub_resources():
            child_details = AutoloadDetailsBuilder.build_details(child_resource)
            autoload_details.resources.extend(child_details.resources)
            autoload_details.attributes.extend(child_details.attributes)
        return autoload_details
