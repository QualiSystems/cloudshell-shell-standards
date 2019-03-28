import cloudshell.shell_standards.attribute_names as attribute_names
from cloudshell.shell_standards.core.resource_model import AbstractResource, ResourceAttribute


class GenericResource(AbstractResource):
    RESOURCE_MODEL = 'GenericResource'

    contact_name = ResourceAttribute(attribute_names.CONTACT_NAME, ResourceAttribute.NAMESPACE.FAMILY_NAME)
    system_name = ResourceAttribute(attribute_names.SYSTEM_NAME, ResourceAttribute.NAMESPACE.FAMILY_NAME)

    location = ResourceAttribute(attribute_names.LOCATION, ResourceAttribute.NAMESPACE.FAMILY_NAME)
    model = ResourceAttribute(attribute_names.MODEL, ResourceAttribute.NAMESPACE.FAMILY_NAME)
    os_version = ResourceAttribute(attribute_names.OS_VERSION, ResourceAttribute.NAMESPACE.FAMILY_NAME)
    vendor = ResourceAttribute(attribute_names.VENDOR, ResourceAttribute.NAMESPACE.FAMILY_NAME)

    def __init__(self, resource_name, shell_name, family_name):
        super().__init__(None, shell_name, name=resource_name, family_name=family_name)


class GenericChassis(AbstractResource):
    RELATIVE_ADDRESS_PREFIX = 'CH'
    NAME_TEMPLATE = 'Chassis {}'
    FAMILY_NAME = 'CS_Chassis'
    RESOURCE_MODEL = 'GenericChassis'

    model = ResourceAttribute(attribute_names.MODEL, ResourceAttribute.NAMESPACE.SHELL_NAME)
    serial_number = ResourceAttribute(attribute_names.SERIAL_NUMBER, ResourceAttribute.NAMESPACE.SHELL_NAME)
    model_name = ResourceAttribute(attribute_names.MODEL_NAME, ResourceAttribute.NAMESPACE.FAMILY_NAME)

    def connect_port(self, port):
        """
        :type port: AbstractResource
        """
        self.add_sub_resource_with_type_restrictions(port, (GenericPort,))


class GenericModule(AbstractResource):
    RELATIVE_ADDRESS_PREFIX = 'M'
    NAME_TEMPLATE = 'Module {}'
    FAMILY_NAME = 'CS_Module'
    RESOURCE_MODEL = 'GenericModule'

    model = ResourceAttribute(attribute_names.MODEL, ResourceAttribute.NAMESPACE.SHELL_NAME)
    version = ResourceAttribute(attribute_names.VERSION, ResourceAttribute.NAMESPACE.SHELL_NAME)
    serial_number = ResourceAttribute(attribute_names.SERIAL_NUMBER, ResourceAttribute.NAMESPACE.SHELL_NAME)
    model_name = ResourceAttribute(attribute_names.MODEL_NAME, ResourceAttribute.NAMESPACE.FAMILY_NAME)


class GenericSubModule(GenericModule):
    RELATIVE_ADDRESS_PREFIX = 'SM'
    NAME_TEMPLATE = 'SubModule {}'
    FAMILY_NAME = 'CS_SubModule'
    RESOURCE_MODEL = 'GenericSubModule'


class GenericPort(AbstractResource):
    RELATIVE_ADDRESS_PREFIX = 'P'
    NAME_TEMPLATE = 'Port {}'
    FAMILY_NAME = 'CS_Port'
    RESOURCE_MODEL = 'GenericPort'

    adjacent = ResourceAttribute(attribute_names.ADJACENT, ResourceAttribute.NAMESPACE.SHELL_NAME)
    ipv4_address = ResourceAttribute(attribute_names.IPV4_ADDRESS, ResourceAttribute.NAMESPACE.SHELL_NAME)
    ipv6_address = ResourceAttribute(attribute_names.IPV6_ADDRESS, ResourceAttribute.NAMESPACE.SHELL_NAME)
    mac_address = ResourceAttribute(attribute_names.MAC_ADDRESS, ResourceAttribute.NAMESPACE.SHELL_NAME)
    port_description = ResourceAttribute(attribute_names.PORT_DESCRIPTION, ResourceAttribute.NAMESPACE.SHELL_NAME)


class BaseGenericNetworkPort(GenericPort):
    auto_negotiation = ResourceAttribute(attribute_names.AUTO_NEGOTIATION, ResourceAttribute.NAMESPACE.SHELL_NAME)
    bandwidth = ResourceAttribute(attribute_names.BANDWIDTH, ResourceAttribute.NAMESPACE.SHELL_NAME, 0)
    duplex = ResourceAttribute(attribute_names.DUPLEX, ResourceAttribute.NAMESPACE.SHELL_NAME, 'Half')
    l2_protocol_type = ResourceAttribute(attribute_names.L2_PROTOCOL_TYPE, ResourceAttribute.NAMESPACE.SHELL_NAME)
    mtu = ResourceAttribute(attribute_names.MTU, ResourceAttribute.NAMESPACE.SHELL_NAME, 0)


class GenericPowerPort(AbstractResource):
    RESOURCE_MODEL = 'GenericPowerPort'
    RELATIVE_ADDRESS_PREFIX = 'PP'
    NAME_TEMPLATE = 'Power Port {}'
    FAMILY_NAME = 'CS_PowerPort'

    model = ResourceAttribute(attribute_names.MODEL, ResourceAttribute.NAMESPACE.SHELL_NAME)
    port_description = ResourceAttribute(attribute_names.PORT_DESCRIPTION, ResourceAttribute.NAMESPACE.SHELL_NAME)
    serial_number = ResourceAttribute(attribute_names.SERIAL_NUMBER, ResourceAttribute.NAMESPACE.SHELL_NAME)
    version = ResourceAttribute(attribute_names.VERSION, ResourceAttribute.NAMESPACE.SHELL_NAME)


class GenericPortChannel(AbstractResource):
    RESOURCE_MODEL = 'GenericPortChannel'
    RELATIVE_ADDRESS_PREFIX = 'PC'
    NAME_TEMPLATE = 'Port Channel{}'
    FAMILY_NAME = 'CS_PortChannel'

    associated_ports = ResourceAttribute(attribute_names.ASSOCIATED_PORTS, ResourceAttribute.NAMESPACE.SHELL_NAME)
    ipv4_address = ResourceAttribute(attribute_names.IPV4_ADDRESS, ResourceAttribute.NAMESPACE.SHELL_NAME)
    ipv6_address = ResourceAttribute(attribute_names.IPV6_ADDRESS, ResourceAttribute.NAMESPACE.SHELL_NAME)
    port_description = ResourceAttribute(attribute_names.PORT_DESCRIPTION, ResourceAttribute.NAMESPACE.SHELL_NAME)
