#!/usr/bin/python
# -*- coding: utf-8 -*-

from abc import abstractmethod

from cloudshell.shell_standards.core.autoload.core_entities import InstanceAttribute, RelativeAddress, \
    AttributeContainer, \
    AttributeModel
from cloudshell.shell_standards.exceptions import ResourceModelException


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
        self._child_resources = []

    @property
    def name(self):
        if self._name:
            return self._name
        else:
            return self._gen_name()

    @abstractmethod
    def _gen_name(self):
        """
        Generates resource name
        """
        raise NotImplemented

    @property
    def unique_identifier(self):
        if self._unique_identifier:
            return self._unique_identifier
        return self._gen_unique_id()

    def _gen_unique_id(self):
        """
        Generates unique id
        :rtype: str
        """
        return str(hash('{}+{}'.format(self.relative_address, self.name)))

    def _add_sub_resource(self, sub_resource):
        """Add sub resource
        :type sub_resource: ResourceNode
        """
        sub_resource.relative_address.parent_node = self.relative_address
        self._child_resources.append(sub_resource)

    def extract_sub_resources(self):
        return self._child_resources


class NamespaceAttributeContainer(AttributeContainer):

    def __init__(self, shell_name, family_name):
        """
        Attribute container with defined attribute levels used by ResourceAttribute
        :param shell_name:
        :param family_name:
        """
        super(NamespaceAttributeContainer, self).__init__()
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
        # super(ResourceAttribute).__init__(name, default_value)
        super(ResourceAttribute, self).__init__(name, default_value)
        self.namespace_attribute = namespace_attribute

    def attribute_name(self, instance):
        """Generate attribute name for the specified prefix
        :param NamespaceAttributeContainer instance:
        """
        return '{}.{}'.format(getattr(instance, self.namespace_attribute), self.name)


class AbstractResource(ResourceNode, NamespaceAttributeContainer):
    _RELATIVE_ADDRESS_PREFIX = ''
    _NAME_TEMPLATE = ''
    _FAMILY_NAME = ''
    _RESOURCE_MODEL = ''

    def __init__(self, index, shell_name=None, family_name=None, name=None, unique_id=None):
        ResourceNode.__init__(self, index, self._RELATIVE_ADDRESS_PREFIX, name, unique_id)
        NamespaceAttributeContainer.__init__(self, shell_name, family_name or self._FAMILY_NAME)
        self.resource_model = self._RESOURCE_MODEL

    def _gen_name(self):
        """Generate resource name"""
        if self._NAME_TEMPLATE:
            return self._NAME_TEMPLATE.format(self.relative_address.index)
        raise ResourceModelException('NAME_TEMPLATE is empty')

    def _add_sub_resource_with_type_restrictions(self, sub_resource, allowed_types):
        """
        Register child resource which in the list of allowed types
        :param AbstractResource sub_resource: Registered resource
        :param collections.Iterable allowed_types: Allowed types
        """
        if isinstance(sub_resource, tuple(allowed_types)):
            self._add_sub_resource(sub_resource)
        else:
            raise ResourceModelException('Class {} not allowed to connect to {}'.format(sub_resource.__class__.__name__,
                                                                           self.__class__.__name__))
