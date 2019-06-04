#!/usr/bin/python
# -*- coding: utf-8 -*-
from collections import defaultdict

from cloudshell.shell.standards.core.utils import attr_length_validator


class AttributeContainer(object):
    """Contains Attributes"""

    def __init__(self):
        self.attributes = {}


class AttributeModel(object):
    """
    Attribute descriptor
    """
    MAX_LENGTH = 2000

    def __init__(self, name, default_value=None):
        self.name = name
        self.default_value = default_value

    def attribute_name(self, instance):
        return self.name

    def __get__(self, instance, owner):
        """
        :type instance: AttributeContainer
        """

        if instance is None:
            return self

        return instance.attributes.get(self.attribute_name(instance), self.default_value)

    @attr_length_validator(MAX_LENGTH)
    def __set__(self, instance, value):
        """
        :type instance: AttributeContainer
        :return:
        """
        value = value if value is not None else self.default_value
        instance.attributes[self.attribute_name(instance)] = value


class InstanceAttribute(object):
    """
    Validates instance attribute
    """

    def __init__(self):
        self.value_container = {}

    def __get__(self, instance, owner):
        if instance is None:
            return self

        return self.value_container.get(instance, None)

    @attr_length_validator(AttributeModel.MAX_LENGTH)
    def __set__(self, instance, value):
        self.value_container[instance] = value


class RelativeAddress(object):
    ADDRESS_SEPARATOR = '/'

    class IndexValidator(object):
        """
        Validate registered indexes
        """

        def __init__(self):
            self._address_dict = defaultdict(lambda: defaultdict(list))

        @staticmethod
        def _generate_index(index, position):
            """Generate index if needed"""
            return '{}-{}'.format(index, position)

        def get_valid(self, node):
            """
            Validate index
            :type node: RelativeAddress
            """
            instance_list = self._address_dict.get(node._prefix, {}).get(node.native_index, [])
            if node in instance_list and len(instance_list) > 1:
                return self._generate_index(node.native_index, instance_list.index(node))
            else:
                return node.native_index

        def register(self, node):
            """
            Register node
            :type node: RelativeAddress
            """
            self._address_dict[node._prefix][node.native_index].append(node)

    def __init__(self, index, prefix='', parent_node=None):
        """
        :type index: str
        :type prefix: str
        :type parent_node: RelativeAddress
        """

        self.__parent_node = None
        self.__index_validator = RelativeAddress.IndexValidator()

        self.native_index = index
        self._prefix = prefix
        self.parent_node = parent_node

    @property
    def index(self):
        """
        Validated index
        :rtype: str
        """
        if self.parent_node and self.parent_node.__index_validator:
            return self.parent_node.__index_validator.get_valid(self)
        else:
            return self.native_index

    @index.setter
    def index(self, value):
        self.native_index = value

    @property
    def _full_address(self):
        """
        Relative address
        :rtype: str
        """
        if self.parent_node and self.parent_node._full_address:
            return '{}{}{}'.format(self.parent_node._full_address, self.ADDRESS_SEPARATOR,
                                   self._local_address)
        elif self.index:
            return self._local_address
        else:
            return ''

    @property
    def _parent_node(self):
        """
        Parent node
        :rtype: RelativeAddress
        """
        return self.__parent_node

    @_parent_node.setter
    def _parent_node(self, node):
        """
        :type node: RelativeAddress
        """
        if node:
            self.__parent_node = node
            node.__index_validator.register(self)

    @property
    def _local_address(self):
        """
        Generates local relative address
        """
        local_address = '{}{}'.format(self._prefix or '', self.index or '')
        return local_address

    def to_string(self):
        return self._full_address

    def __str__(self):
        return self.to_string()

    def __repr__(self):
        self.__str__()

