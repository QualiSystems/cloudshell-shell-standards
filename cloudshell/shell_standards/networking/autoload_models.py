#!/usr/bin/python
# -*- coding: utf-8 -*-
from cloudshell.shell_standards.autoload_generic_models import GenericResource, GenericChassis, GenericModule, \
    GenericSubModule, GenericNetworkPort, GenericPowerPort, GenericPortChannel
from cloudshell.shell_standards.core.autoload.resource_model import ResourceAttribute
import cloudshell.shell_standards.attribute_names as attribute_names

__all__ = ['GenericResource', 'GenericChassis', 'GenericModule', 'GenericSubModule',
           'GenericPortChannel', 'GenericPowerPort', 'GenericNetworkPort']


class NetworkingResource(GenericResource):
    _SUPPORTED_FAMILY_NAMES = ['CS_Switch', 'CS_Router', 'CS_WirelessController']
    model_name = ResourceAttribute(attribute_names.MODEL_NAME, ResourceAttribute.NAMESPACE.FAMILY_NAME)
