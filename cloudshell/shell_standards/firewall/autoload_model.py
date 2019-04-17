#!/usr/bin/python
# -*- coding: utf-8 -*-
from cloudshell.shell_standards.autoload_generic_models import GenericResourceModel, GenericChassis, GenericModule, \
    GenericSubModule, GenericNetworkPort, GenericPowerPort, GenericPortChannel

__all__ = ['FirewallResourceModel', 'GenericResourceModel', 'GenericChassis', 'GenericModule', 'GenericSubModule',
           'GenericPortChannel', 'GenericPowerPort', 'GenericNetworkPort']


class FirewallResourceModel(GenericResourceModel):
    SUPPORTED_FAMILY_NAMES = ['CS_Firewall']

    @property
    def Entities(self):
        class _FirewallEntities:
            Chassis = GenericChassis
            Module = GenericModule
            SubModule = GenericSubModule
            Port = FirewallPort
            PortChannel = GenericPortChannel
            PowerPort = GenericPowerPort

        return _FirewallEntities


class FirewallPort(GenericNetworkPort):
    pass
