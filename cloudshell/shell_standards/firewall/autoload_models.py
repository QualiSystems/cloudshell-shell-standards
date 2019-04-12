#!/usr/bin/python
# -*- coding: utf-8 -*-
from cloudshell.shell_standards.autoload_generic_models import GenericResource, GenericChassis, GenericModule, \
    GenericSubModule, GenericNetworkPort, GenericPowerPort, GenericPortChannel

__all__ = ['GenericResource', 'GenericChassis', 'GenericModule', 'GenericSubModule',
           'GenericPortChannel', 'GenericPowerPort', 'GenericNetworkPort']


class FirewallResource(GenericResource):
    SUPPORTED_FAMILY_NAMES = ['CS_Firewall']
