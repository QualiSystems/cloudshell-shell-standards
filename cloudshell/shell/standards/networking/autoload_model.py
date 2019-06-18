#!/usr/bin/python
# -*- coding: utf-8 -*-
from cloudshell.shell.standards.autoload_generic_models import GenericResourceModel, GenericChassis, GenericModule, \
    GenericSubModule, GenericNetworkPort, GenericPowerPort, GenericPortChannel
from cloudshell.shell.standards.core.autoload.resource_model import ResourceAttribute
import cloudshell.shell.standards.attribute_names as attribute_names

__all__ = ['NetworkingResourceModel', 'GenericResourceModel', 'GenericChassis', 'GenericModule', 'GenericSubModule',
           'GenericPortChannel', 'GenericPowerPort', 'GenericNetworkPort']


#
# class NetworkingPort(GenericNetworkPort):
#     pass


class NetworkingResourceModel(GenericResourceModel):
    SUPPORTED_FAMILY_NAMES = ['CS_Switch', 'CS_Router', 'CS_WirelessController']

    model_name = ResourceAttribute(attribute_names.MODEL_NAME, ResourceAttribute.NAMESPACE.FAMILY_NAME)

    class NetworkingPort(GenericNetworkPort):
        pass

    @property
    def entities(self):
        class _NetworkingEntities:
            Chassis = GenericChassis
            Module = GenericModule
            SubModule = GenericSubModule
            Port = self.NetworkingPort
            PortChannel = GenericPortChannel
            PowerPort = GenericPowerPort

        return _NetworkingEntities


class NNResourceModel(NetworkingResourceModel):
    # SUPPORTED_FAMILY_NAMES = []

    class NNPort(NetworkingResourceModel.NetworkingPort):
        pass

    @property
    def entities(self):
        class _NNEntities:
            Chassis = GenericChassis
            Module = GenericModule
            SubModule = GenericSubModule
            Port = self.NNPort
            PortChannel = GenericPortChannel
            PowerPort = GenericPowerPort

        return _NNEntities


class NNNResourceModel(NNResourceModel):
    # SUPPORTED_FAMILY_NAMES = []

    class NNNPort(NNResourceModel.NNPort):
        pass

    @property
    def entities(self):
        class _NNNEntities:
            Chassis = GenericChassis
            Module = GenericModule
            SubModule = GenericSubModule
            Port = self.NNNPort
            PortChannel = GenericPortChannel
            PowerPort = GenericPowerPort

        return _NNNEntities
