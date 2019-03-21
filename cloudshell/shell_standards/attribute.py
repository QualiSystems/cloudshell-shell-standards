from cloudshell.shell_standards.utils import attr_length_validator


class AttributeContainer(object):
    def __init__(self):
        self.attributes = {}


class ResourceAttribute(object):
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

    class LVL(object):
        NAMESPACE = 'namespace'
        FAMILY_TYPE = 'family_type'

    MAX_LENGTH = 2000

    def __init__(self, prefix_attr, name, default=None):
        self.prefix_attr = prefix_attr
        self.name = name
        self.default = default

    def get_key(self, instance):
        return '{}.{}'.format(getattr(instance, self.prefix_attr), self.name)

    def __get__(self, instance, owner):
        """
        :type instance: AttributeContainer
        """

        if instance is None:
            return self

        return instance.attributes.get(self.get_key(instance), self.default)

    @attr_length_validator(MAX_LENGTH)
    def __set__(self, instance, value):
        value = value if value is not None else self.default

        instance.attributes[self.get_key(instance)] = value
