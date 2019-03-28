from collections import defaultdict

from cloudshell.shell_standards.core.utils import attr_length_validator, cached_property


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
            instance_list = self._address_dict.get(node._prefix, {}).get(node._native_index, [])
            if node in instance_list and len(instance_list) > 1:
                return self._generate_index(node._native_index, instance_list.index(node))
            else:
                return node._native_index

        def register(self, node):
            """
            Register node
            :type node: RelativeAddress
            """
            self._address_dict[node._prefix][node._native_index].append(node)

    def __init__(self, index, prefix='', parent_node=None):
        """
        :type index: str
        :type prefix: str
        :type parent_node: RelativeAddress
        """

        self.__parent_node = None
        self.__index_validator = RelativeAddress.IndexValidator()

        self._native_index = index
        self._prefix = prefix
        self._parent_node = parent_node

    @cached_property
    def index(self):
        """
        Validated index
        :rtype: str
        """
        if self._parent_node and self._parent_node.__index_validator:
            return self._parent_node.__index_validator.get_valid(self)
        else:
            return self._native_index

    @cached_property
    def _full_address(self):
        """
        Relative address
        :rtype: str
        """
        if self._parent_node and self._parent_node._full_address:
            return '{}{}{}'.format(self._parent_node._full_address, self.ADDRESS_SEPARATOR,
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

    def add_parent_address(self, parent_node):
        self._parent_node = parent_node

    def to_string(self):
        return self._full_address

    def __str__(self):
        return self.to_string()

    def __repr__(self):
        self.__str__()


if __name__ == '__main__':
    resourcee = RelativeAddress(None, None)
    chassis = RelativeAddress(1, 'CH', resourcee)
    module1 = RelativeAddress('dsd', 'M', chassis)
    module2 = RelativeAddress('sd', 'M', chassis)
    module3 = RelativeAddress('sd', 'M', chassis)
    port1 = RelativeAddress('ff', 'P', module1)
    port2 = RelativeAddress('ff', 'P', module2)
    port3 = RelativeAddress('ff', 'P', module2)
    port4 = RelativeAddress('hh', 'P', module3)
    port5 = RelativeAddress('hh', 'P', module3)
    print(port1)
    print(port2)
    print(port3)
    print(port5)
    print(module1)
    print(module2)
    print(module3)
    print(chassis)
    print(resourcee)
