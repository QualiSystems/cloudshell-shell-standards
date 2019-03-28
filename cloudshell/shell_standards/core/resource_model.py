from abc import abstractmethod

from cloudshell.shell_standards.core.core_entities import InstanceAttribute, RelativeAddress, AttributeContainer, \
    AttributeModel


class ResourceNode(object):
    _name = InstanceAttribute()
    _unique_identifier = InstanceAttribute()

    def __init__(self, index, prefix, name=None, unique_id=None):
        """

        :param str name:
        :param str unique_id:
        """

        self.relative_address = RelativeAddress(index, prefix)

        self._name = name
        self._unique_identifier = unique_id
        self.child_resources = []

    @property
    def name(self):
        if self._name:
            return self._name
        else:
            return self._gen_name()

    @abstractmethod
    def _gen_name(self):
        pass

    @property
    def unique_identifier(self):
        if self._unique_identifier:
            return self._unique_identifier
        return self._gen_unique_id()

    def _gen_unique_id(self):
        return hash('{}+{}'.format(self.relative_address, self.name))

    def add_sub_resource(self, sub_resource):
        """Add sub resource
        :type sub_resource: AbstractResource
        """
        sub_resource.relative_address.add_parent_address(self)
        self.child_resources.append(sub_resource)


class NamespaceAttributeContainer(AttributeContainer):
    def __init__(self, shell_name, family_name):
        """
        Attribute container with defined attribute levels used by ResourceAttribute
        :param shell_name:
        :param family_name:
        """
        super().__init__()
        self.family_name = family_name
        self.shell_name = shell_name


class ResourceAttribute(AttributeModel):
    class NAMESPACE(object):
        """
        Attribute Levels, attributes defined in LVLDefinedAttributeContainer
        """
        SHELL_NAME = 'shell_name'
        FAMILY_NAME = 'family_name'

    def __init__(self, name, namespace_attribute, default_value=None):
        """
        :param name: Attribute name
        :param namespace_attribute:  Attribute name prefix, defined as Level, NAMESPACE.SHELL_NAME or NAMESPACE.FAMILY_TYPE
        :param default_value: Defailt attribute value
        """
        super().__init__(name, default_value)
        self.namespace_attribute = namespace_attribute

    def attribute_name(self, instance):
        """Generate attribute name for specified prefix"""
        return '{}.{}'.format(getattr(instance, self.namespace_attribute), self.name)


class AbstractResource(ResourceNode, NamespaceAttributeContainer):
    RELATIVE_ADDRESS_PREFIX = ''
    NAME_TEMPLATE = ''
    FAMILY_NAME = ''
    RESOURCE_MODEL = ''

    def __init__(self, index, shell_name, family_name=None, name=None, unique_id=None, ):
        ResourceNode.__init__(self, index, self.RELATIVE_ADDRESS_PREFIX, name, unique_id)
        NamespaceAttributeContainer.__init__(self, shell_name, family_name or self.FAMILY_NAME)
        self.resource_model = self.RESOURCE_MODEL

    def _gen_name(self):
        if self.NAME_TEMPLATE:
            return self.NAME_TEMPLATE.format(self.relative_address.index)
        raise Exception('NAME_TEMPLATE is empty')

    def add_sub_resource_with_type_restrictions(self, sub_resource, allowed_types):
        """
        :type sub_resource: AbstractResource
        :type allowed_types: tuple
        """
        if isinstance(sub_resource, allowed_types):
            self.add_sub_resource(sub_resource)
        else:
            raise Exception('Class {} not allowed to connect to {}'.format(sub_resource.__class__.__name__,
                                                                           self.__class__.__name__))
