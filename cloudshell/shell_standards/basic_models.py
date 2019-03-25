from cloudshell.shell_standards.core_entities import InstanceAttribute, StructureNode, AttributeContainer, \
    AttributeModel


class AbstractResource(StructureNode, AttributeContainer):
    RESOURCE_MODEL = ''
    RELATIVE_PATH_TEMPLATE = ''
    NAME_TEMPLATE = ''
    AVAILABLE_CS_FAMILY_TYPES = []
    FAMILY_TYPE = ''

    _name = InstanceAttribute()
    _unique_identifier = InstanceAttribute()

    def __init__(self, index, shell_name, name=None, prefix=None, unique_id=None, family_type=None):
        """

        :param str shell_name:
        :param str name:
        :param str unique_id:
        """

        # if not shell_name:
        #     raise DeprecationWarning('1gen Shells doesn\'t supported')
        #
        # if ' ' in self.RESOURCE_MODEL:
        #     raise ValueError('Resource Model must be without spaces')
        StructureNode.__init__(self, index, prefix or self.RELATIVE_PATH_TEMPLATE)
        AttributeContainer.__init__(self)

        self._name = name
        self.shell_name = shell_name
        self.namespace = '{shell_name}.{resource_model}'.format(shell_name=self.shell_name,
                                                                resource_model=self.RESOURCE_MODEL)
        self.family_type = family_type or self.FAMILY_TYPE
        self._unique_identifier = unique_id
        if family_type not in self.AVAILABLE_CS_FAMILY_TYPES:
            msg = 'Unavailable CS Family Type {}. CS Family Type should be one of: {}'.format(
                family_type, ', '.join(self.AVAILABLE_CS_FAMILY_TYPES))
            raise Exception(self.__class__.__name__, msg)
        self.child_resources = []

        self._parent_resource = None

    @property
    def name(self):
        if self._name:
            return self._name
        else:
            return self.gen_name()

    def gen_name(self):
        if self.NAME_TEMPLATE:
            return self.NAME_TEMPLATE.format(self.index)
        raise Exception('NAME_TEMPLATE is empty')

    @property
    def unique_identifier(self):
        if self._unique_identifier:
            return self._unique_identifier
        return self.gen_unique_id()

    def gen_unique_id(self):
        return '{}.{}.{}'.format(self._local_address, self.name, self.shell_name)

    def add_sub_resource(self, sub_resource):
        """Add sub resource
        :type sub_resource: AbstractResource
        """
        # existing_sub_resources = self.resources.get(sub_resource.RELATIVE_PATH_TEMPLATE, defaultdict(list))
        # existing_sub_resources[relative_id].append(sub_resource)
        # self.resources.update({sub_resource.RELATIVE_PATH_TEMPLATE: existing_sub_resources})
        sub_resource.parent_node = self
        self.child_resources.append(sub_resource)

    @property
    def cloudshell_model_name(self):
        """Return the name of the CloudShell model"""

        return self.namespace


class ResourceAttribute(AttributeModel):
    class LVL(object):
        NAMESPACE = 'namespace'
        FAMILY_TYPE = 'family_type'

    class NAME:
        MODEL = 'Model'
        MODEL_NAME = 'Model Name'
        SERIAL_NUMBER = 'Serial Number'
        VERSION = 'Version'
        OS_VERSION = 'OS Version'
        SYSTEM_NAME = 'System Name'
        VENDOR = 'Vendor'
        LOCATION = 'Location'
        BACKUP_LOCATION = 'Backup Location'
        CONTACT_NAME = 'Contact Name'
        ADJACENT = 'Adjacent'
        IPV4_ADDRESS = 'IPv4 Address'
        IPV6_ADDRESS = 'IPv6 Address'
        MAC_ADDRESS = 'MAC Address'
        PORT_DESCRIPTION = 'Port Description'
        AUTO_NEGOTIATION = 'Auto Negotiation'
        BANDWIDTH = 'Bandwidth'
        DUPLEX = 'Duplex'
        L2_PROTOCOL_TYPE = 'L2 Protocol Type'
        MTU = 'MTU'
        ASSOCIATED_PORTS = 'Associated Ports'


class BasePhysicalResource(AbstractResource):
    RESOURCE_MODEL = 'GenericResource'
    RELATIVE_PATH_TEMPLATE = ''

    contact_name = ResourceAttribute(ResourceAttribute.LVL.FAMILY_TYPE, ResourceAttribute.NAME.CONTACT_NAME)
    location = ResourceAttribute(ResourceAttribute.LVL.FAMILY_TYPE, ResourceAttribute.NAME.LOCATION)
    model = ResourceAttribute(ResourceAttribute.LVL.FAMILY_TYPE, ResourceAttribute.NAME.MODEL)
    os_version = ResourceAttribute(ResourceAttribute.LVL.FAMILY_TYPE, ResourceAttribute.NAME.OS_VERSION)
    system_name = ResourceAttribute(ResourceAttribute.LVL.FAMILY_TYPE, ResourceAttribute.NAME.SYSTEM_NAME)
    vendor = ResourceAttribute(ResourceAttribute.LVL.FAMILY_TYPE, ResourceAttribute.NAME.VENDOR)


class BaseGenericPort(AbstractResource):
    RESOURCE_MODEL = 'GenericPort'
    RELATIVE_PATH_TEMPLATE = 'P'
    CS_FAMILY_TYPE = 'CS_Port'

    adjacent = ResourceAttribute(ResourceAttribute.LVL.NAMESPACE,  ResourceAttribute.NAME.ADJACENT)
    ipv4_address = ResourceAttribute(ResourceAttribute.LVL.NAMESPACE,  ResourceAttribute.NAME.IPV4_ADDRESS)
    ipv6_address = ResourceAttribute(ResourceAttribute.LVL.NAMESPACE,  ResourceAttribute.NAME.IPV6_ADDRESS)
    mac_address = ResourceAttribute(ResourceAttribute.LVL.NAMESPACE,  ResourceAttribute.NAME.MAC_ADDRESS)
    port_description = ResourceAttribute(ResourceAttribute.LVL.NAMESPACE,  ResourceAttribute.NAME.PORT_DESCRIPTION)


class BaseGenericNetworkPort(BaseGenericPort):
    auto_negotiation = ResourceAttribute(ResourceAttribute.LVL.NAMESPACE,  ResourceAttribute.NAME.AUTO_NEGOTIATION)
    bandwidth = ResourceAttribute(ResourceAttribute.LVL.NAMESPACE,  ResourceAttribute.NAME.BANDWIDTH, 0)
    duplex = ResourceAttribute(ResourceAttribute.LVL.NAMESPACE,  ResourceAttribute.NAME.DUPLEX, 'Half')
    l2_protocol_type = ResourceAttribute(ResourceAttribute.LVL.NAMESPACE,  ResourceAttribute.NAME.L2_PROTOCOL_TYPE)
    mtu = ResourceAttribute(ResourceAttribute.LVL.NAMESPACE,  ResourceAttribute.NAME.MTU, 0)


class GenericChassis(AbstractResource):
    RESOURCE_MODEL = 'GenericChassis'
    RELATIVE_PATH_TEMPLATE = 'CH'
    CS_FAMILY_TYPE = 'CS_Chassis'

    model = ResourceAttribute(ResourceAttribute.LVL.NAMESPACE,  ResourceAttribute.NAME.MODEL)
    serial_number = ResourceAttribute(ResourceAttribute.LVL.NAMESPACE,  ResourceAttribute.NAME.SERIAL_NUMBER)


class GenericModule(AbstractResource):
    RESOURCE_MODEL = 'GenericModule'
    RELATIVE_PATH_TEMPLATE = 'M'
    CS_FAMILY_TYPE = 'CS_Module'

    model = ResourceAttribute(ResourceAttribute.LVL.NAMESPACE,  ResourceAttribute.NAME.MODEL)
    serial_number = ResourceAttribute(ResourceAttribute.LVL.NAMESPACE,  ResourceAttribute.NAME.SERIAL_NUMBER)
    version = ResourceAttribute(ResourceAttribute.LVL.NAMESPACE,  ResourceAttribute.NAME.VERSION)


class GenericSubModule(GenericModule):
    RESOURCE_MODEL = 'GenericSubModule'
    RELATIVE_PATH_TEMPLATE = 'SM'
    CS_FAMILY_TYPE = 'CS_SubModule'


class GenericPowerPort(AbstractResource):
    RESOURCE_MODEL = 'GenericPowerPort'
    RELATIVE_PATH_TEMPLATE = 'PP'
    CS_FAMILY_TYPE = 'CS_PowerPort'

    model = ResourceAttribute(ResourceAttribute.LVL.NAMESPACE,  ResourceAttribute.NAME.MODEL)
    port_description = ResourceAttribute(ResourceAttribute.LVL.NAMESPACE,  ResourceAttribute.NAME.PORT_DESCRIPTION)
    serial_number = ResourceAttribute(ResourceAttribute.LVL.NAMESPACE,  ResourceAttribute.NAME.SERIAL_NUMBER)
    version = ResourceAttribute(ResourceAttribute.LVL.NAMESPACE,  ResourceAttribute.NAME.VERSION)


class GenericPortChannel(AbstractResource):
    RESOURCE_MODEL = 'GenericPortChannel'
    RELATIVE_PATH_TEMPLATE = 'PC'
    CS_FAMILY_TYPE = 'CS_PortChannel'

    associated_ports = ResourceAttribute(ResourceAttribute.LVL.NAMESPACE,  ResourceAttribute.NAME.ASSOCIATED_PORTS)
    ipv4_address = ResourceAttribute(ResourceAttribute.LVL.NAMESPACE,  ResourceAttribute.NAME.IPV4_ADDRESS)
    ipv6_address = ResourceAttribute(ResourceAttribute.LVL.NAMESPACE,  ResourceAttribute.NAME.IPV6_ADDRESS)
    port_description = ResourceAttribute(ResourceAttribute.LVL.NAMESPACE,  ResourceAttribute.NAME.PORT_DESCRIPTION)
