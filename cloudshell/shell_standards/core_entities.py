from collections import defaultdict

from cloudshell.shell_standards.utils import attr_length_validator, cached_property


class AttributeContainer(object):
    """Contains Attributes"""

    def __init__(self):
        self.attributes = {}


class AttributeModel(object):
    """
    Attribute descriptor
    """
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


class InstanceAttribute(object):
    """
    Validates object attribute
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


class IndexValidator(object):
    """
    Validates registered indexes
    """

    def __init__(self):
        self._address_dict = defaultdict(lambda: defaultdict(list))

    @staticmethod
    def _generate_index(index, position):
        """Generate index name, when """
        return '{}-{}'.format(index, position)

    def get_valid(self, node):
        """
        Validate index
        :type node: StructureNode
        """
        instance_list = self._address_dict.get(node.prefix, {}).get(node.native_index, [])
        if node in instance_list and len(instance_list) > 1:
            return self._generate_index(node.native_index, instance_list.index(node))
        else:
            return node.native_index

    def register(self, node):
        """
        Register node
        :type node: StructureNode
        """
        self._address_dict[node.prefix][node.native_index].append(node)


class StructureNode(object):
    ADDRESS_SEPARATOR = '/'

    def __init__(self, index, prefix='', parent_node=None):
        """
        :type index: str
        :type prefix: str
        :type parent_node: StructureNode
        """

        self._parent_node = None
        self._index_validator = IndexValidator()

        self.native_index = index
        self.prefix = prefix
        self.parent_node = parent_node

    @cached_property
    def index(self):
        """
        Validated index
        :rtype: str
        """
        if self.parent_node and self.parent_node._index_validator:
            return self.parent_node._index_validator.get_valid(self)
        else:
            return self.native_index

    @cached_property
    def relative_address(self):
        """
        Relative address
        :rtype: str
        """
        if self.parent_node:
            return '{}{}{}'.format(self.parent_node.relative_address, self.ADDRESS_SEPARATOR,
                                   self._local_address)
        elif self.index:
            return self._local_address
        else:
            return ''

    @property
    def parent_node(self):
        """
        Parent node
        :rtype: StructureNode
        """
        return self._parent_node

    @parent_node.setter
    def parent_node(self, node):
        """
        :type node: StructureNode
        """
        if node:
            self._parent_node = node
            node._index_validator.register(self)

    @property
    def _local_address(self):
        """
        Generates local relative address
        """
        local_address = '{}{}'.format(self.prefix or '', self.index)
        return local_address

    def __str__(self):
        return self._local_address


if __name__ == '__main__':
    resourcee = StructureNode(None, None)
    chassis = StructureNode(1, 'CH', resourcee)
    module1 = StructureNode('dsd', 'M', chassis)
    module2 = StructureNode('sd', 'M', chassis)
    module3 = StructureNode('sd', 'M', chassis)
    port1 = StructureNode('ff', 'P', module1)
    port2 = StructureNode('ff', 'P', module2)
    port3 = StructureNode('ff', 'P', module2)
    port4 = StructureNode('hh', 'P', module3)
    port5 = StructureNode('hh', 'P', module3)
    print(port1.relative_address)
    print(port2.relative_address)
    print(port3.relative_address)
    print(port5.relative_address)
    print(module1.relative_address)
    print(module2.relative_address)
    print(module3.relative_address)
    print(chassis.relative_address)
    print(resourcee.relative_address)
