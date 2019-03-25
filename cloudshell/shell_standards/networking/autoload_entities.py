#!/usr/bin/python
# -*- coding: utf-8 -*-
import cloudshell.shell_standards.attribute as attributes
import cloudshell.shell_standards.family_types as family_types
from cloudshell.shell_standards.basic_models import BaseGenericNetworkPort as GenericPort
from cloudshell.shell_standards.basic_models import GenericChassis, GenericModule, \
    GenericSubModule, GenericPowerPort, GenericPortChannel, BasePhysicalResource

__all__ = ['GenericResource', 'GenericChassis', 'GenericModule', 'GenericSubModule',
           'GenericPortChannel', 'GenericPowerPort', 'GenericPort']


class GenericResource(BasePhysicalResource):
    AVAILABLE_CS_FAMILY_TYPES = [family_types.SWITCH, family_types.ROUTER, family_types.WIRELESS_CONTROLLER]
    model_name = ResourceAttribute(ResourceAttribute.LVL.CS_FAMILY_TYPE, ResourceAttribute.NAME.MODEL_NAME)
