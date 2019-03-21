from cloudshell.shell_standards.attribute import ResourceAttribute
from cloudshell.shell_standards.utils import attr_length_validator


class InstanceAttribute(object):
    def __init__(self):
        self.value = None

    def __get__(self, instance, owner):
        if instance is None:
            return self

        return self.value

    @attr_length_validator(ResourceAttribute.MAX_LENGTH)
    def __set__(self, instance, value):
        self.value = value


class AbstractResource(StructureUnit):
    RESOURCE_MODEL = ''
    RELATIVE_PATH_TEMPLATE = ''

    name = InstanceAttribute()
    unique_identifier = InstanceAttribute()

    def __init__(self, shell_name, name, unique_id):
        """

        :param str shell_name:
        :param str name:
        :param str unique_id:
        """

        if not shell_name:
            raise DeprecationWarning('1gen Shells doesn\'t supported')

        if ' ' in self.RESOURCE_MODEL:
            raise ValueError('Resource Model must be without spaces')

        self.name = name
        self.shell_name = shell_name
        self.namespace = '{shell_name}.{resource_model}'.format(
            shell_name=self.shell_name, resource_model=self.RESOURCE_MODEL)
        self.unique_identifier = unique_id
        self.attributes = {}
        self.resources = {}

        self._parent_resource = None

    def connect_parent(self, parent_resource):
        self._parent_resource = parent_resource

    def add_sub_resource(self, sub_resource):
        """Add sub resource
        :type sub_resource: AbstractResource
        """
        # existing_sub_resources = self.resources.get(sub_resource.RELATIVE_PATH_TEMPLATE, defaultdict(list))
        # existing_sub_resources[relative_id].append(sub_resource)
        # self.resources.update({sub_resource.RELATIVE_PATH_TEMPLATE: existing_sub_resources})
        sub_resource.connect_parent(self)

    @property
    def cloudshell_model_name(self):
        """Return the name of the CloudShell model"""

        return self.namespace


class BaseResource(AbstractResource):
    class FAMILY_TYPES:
        SWITCH = 'CS_Switch'
        ROUTER = 'CS_Router'
        WIRELESS_CONTROLLER = 'CS_WirelessController'

    AVAILABLE_CS_FAMILY_TYPES = []

    FAMILY_TYPE = FAMILY_TYPES.SWITCH

    def __init__(self, shell_name, name, unique_id, cs_family_type=None):
        super(BaseResource, self).__init__(shell_name, name, unique_id)

        self.family_type = cs_family_type or self.FAMILY_TYPE

        if cs_family_type not in self.AVAILABLE_CS_FAMILY_TYPES:
            msg = 'Unavailable CS Family Type {}. CS Family Type should be one of: {}'.format(
                cs_family_type, ', '.join(self.AVAILABLE_CS_FAMILY_TYPES))
            raise Exception(self.__class__.__name__, msg)


class BasePhysicalResource(BaseResource):
    RESOURCE_MODEL = 'GenericResource'
    RELATIVE_PATH_TEMPLATE = ''

    contact_name = ResourceAttribute(ResourceAttribute.LVL.FAMILY_TYPE, ResourceAttribute.NAME.CONTACT_NAME)
    location = ResourceAttribute(ResourceAttribute.LVL.CS_FAMILY_TYPE, ATTRIBUTE_NAME.LOCATION)
    model = ResourceAttribute(ResourceAttribute.LVL.CS_FAMILY_TYPE, ATTRIBUTE_NAME.MODEL)
    os_version = ResourceAttribute(ResourceAttribute.LVL.CS_FAMILY_TYPE, ATTRIBUTE_NAME.OS_VERSION)
    system_name = ResourceAttribute(ResourceAttribute.LVL.CS_FAMILY_TYPE, ATTRIBUTE_NAME.SYSTEM_NAME)
    vendor = ResourceAttribute(ResourceAttribute.LVL.CS_FAMILY_TYPE, ATTRIBUTE_NAME.VENDOR)


class BaseGenericPort(AbstractResource):
    RESOURCE_MODEL = 'GenericPort'
    RELATIVE_PATH_TEMPLATE = 'P'
    CS_FAMILY_TYPE = 'CS_Port'

    adjacent = ResourceAttribute(ResourceAttribute.LVL.NAMESPACE, ATTRIBUTE_NAME.ADJACENT)
    ipv4_address = ResourceAttribute(ResourceAttribute.LVL.NAMESPACE, ATTRIBUTE_NAME.IPV4_ADDRESS)
    ipv6_address = ResourceAttribute(ResourceAttribute.LVL.NAMESPACE, ATTRIBUTE_NAME.IPV6_ADDRESS)
    mac_address = ResourceAttribute(ResourceAttribute.LVL.NAMESPACE, ATTRIBUTE_NAME.MAC_ADDRESS)
    port_description = ResourceAttribute(ResourceAttribute.LVL.NAMESPACE, ATTRIBUTE_NAME.PORT_DESCRIPTION)


class BaseGenericNetworkPort(BaseGenericPort):
    auto_negotiation = ResourceAttribute(ResourceAttribute.LVL.NAMESPACE, ATTRIBUTE_NAME.AUTO_NEGOTIATION)
    bandwidth = ResourceAttribute(ResourceAttribute.LVL.NAMESPACE, ATTRIBUTE_NAME.BANDWIDTH, 0)
    duplex = ResourceAttribute(ResourceAttribute.LVL.NAMESPACE, ATTRIBUTE_NAME.DUPLEX, 'Half')
    l2_protocol_type = ResourceAttribute(ResourceAttribute.LVL.NAMESPACE, ATTRIBUTE_NAME.L2_PROTOCOL_TYPE)
    mtu = ResourceAttribute(ResourceAttribute.LVL.NAMESPACE, ATTRIBUTE_NAME.MTU, 0)


class GenericChassis(AbstractResource):
    RESOURCE_MODEL = 'GenericChassis'
    RELATIVE_PATH_TEMPLATE = 'CH'
    CS_FAMILY_TYPE = 'CS_Chassis'

    model = ResourceAttribute(ResourceAttribute.LVL.NAMESPACE, ATTRIBUTE_NAME.MODEL)
    serial_number = ResourceAttribute(ResourceAttribute.LVL.NAMESPACE, ATTRIBUTE_NAME.SERIAL_NUMBER)


class GenericModule(AbstractResource):
    RESOURCE_MODEL = 'GenericModule'
    RELATIVE_PATH_TEMPLATE = 'M'
    CS_FAMILY_TYPE = 'CS_Module'

    model = ResourceAttribute(ResourceAttribute.LVL.NAMESPACE, ATTRIBUTE_NAME.MODEL)
    serial_number = ResourceAttribute(ResourceAttribute.LVL.NAMESPACE, ATTRIBUTE_NAME.SERIAL_NUMBER)
    version = ResourceAttribute(ResourceAttribute.LVL.NAMESPACE, ATTRIBUTE_NAME.VERSION)


class GenericSubModule(GenericModule):
    RESOURCE_MODEL = 'GenericSubModule'
    RELATIVE_PATH_TEMPLATE = 'SM'
    CS_FAMILY_TYPE = 'CS_SubModule'


class GenericPowerPort(AbstractResource):
    RESOURCE_MODEL = 'GenericPowerPort'
    RELATIVE_PATH_TEMPLATE = 'PP'
    CS_FAMILY_TYPE = 'CS_PowerPort'

    model = ResourceAttribute(ResourceAttribute.LVL.NAMESPACE, ATTRIBUTE_NAME.MODEL)
    port_description = ResourceAttribute(ResourceAttribute.LVL.NAMESPACE, ATTRIBUTE_NAME.PORT_DESCRIPTION)
    serial_number = ResourceAttribute(ResourceAttribute.LVL.NAMESPACE, ATTRIBUTE_NAME.SERIAL_NUMBER)
    version = ResourceAttribute(ResourceAttribute.LVL.NAMESPACE, ATTRIBUTE_NAME.VERSION)


class GenericPortChannel(AbstractResource):
    RESOURCE_MODEL = 'GenericPortChannel'
    RELATIVE_PATH_TEMPLATE = 'PC'
    CS_FAMILY_TYPE = 'CS_PortChannel'

    associated_ports = ResourceAttribute(ResourceAttribute.LVL.NAMESPACE, ATTRIBUTE_NAME.ASSOCIATED_PORTS)
    ipv4_address = ResourceAttribute(ResourceAttribute.LVL.NAMESPACE, ATTRIBUTE_NAME.IPV4_ADDRESS)
    ipv6_address = ResourceAttribute(ResourceAttribute.LVL.NAMESPACE, ATTRIBUTE_NAME.IPV6_ADDRESS)
    port_description = ResourceAttribute(ResourceAttribute.LVL.NAMESPACE, ATTRIBUTE_NAME.PORT_DESCRIPTION)
