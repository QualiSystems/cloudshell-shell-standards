from collections import defaultdict

from cloudshell.shell_standards.utils import attr_length_validator, cached_property


class AttributeContainer(object):
    """Contains Attributes"""

    def __init__(self):
        self.attributes = {}


class AttributeUnit(object):
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

    def __get__(self, instance, owner):
        if instance is None:
            return self

        return self.value

    @attr_length_validator(AttributeUnit.MAX_LENGTH)
    def __set__(self, instance, value):
        self.value = value


class IndexValidator(object):
    """
    Index validator
    """

    def __init__(self):
        self._address_dict = defaultdict(lambda: defaultdict(list))

    def _generate_index(self, index, position):
        return '{}-{}'.format(index, position)

    def get_valid(self, resource):
        """
        :type resource: Resource
        """
        instance_list = self._address_dict[resource.prefix][resource.native_index]
        if len(instance_list) > 1:
            return self._generate_index(resource.native_index, instance_list.index(resource))
        else:
            return resource.native_index

    def register(self, resource):
        """
        :type resource: Resource
        """
        self._address_dict[resource.prefix][resource.native_index].append(resource)


class RelativeAddress(object):
    ADDRESS_SEPARATOR = '/'

    def __init__(self, address_separator=ADDRESS_SEPARATOR):
        self._address_separator = address_separator

    @staticmethod
    def _get_local_address(prefix, index):
        local_address = '{}{}'.format(prefix or '', index)
        return local_address

    def __get__(self, instance, owner):
        if instance is None:
            return self

        if instance.parent and instance.parent.address and instance.index:
            return '{}{}{}'.format(instance.parent.address, self._address_separator,
                                   self._get_local_address(instance.prefix, instance.index))
        elif instance.index:
            return self._get_local_address(instance.prefix, instance.index)
        else:
            return ''


class StructureUnit(object):
    _address = RelativeAddress()

    def __init__(self, index, prefix, parent=None):
        """
        :type index: str
        :type parent: Resource
        """
        self.parent = None

        self.native_index = index
        self.prefix = prefix

        self.connect_parent(parent)

        self.index_validator = IndexValidator()

    @cached_property
    def index(self):
        if self.parent and self.parent.index_validator:
            return self.parent.index_validator.get_valid(self)
        else:
            return self.native_index

    @cached_property
    def address(self):
        return self._address

    def connect_parent(self, parent):
        """
        :type parent: Resource
        """
        if parent:
            self.parent = parent
            self.parent.index_validator.register(self)


if __name__ == '__main__':
    resource = StructureUnit(None, None)
    chassis = StructureUnit(1, 'CH', resource)
    module1 = StructureUnit('dsd', 'M', chassis)
    module2 = StructureUnit('sd', 'M', chassis)
    port1 = StructureUnit('ff', 'P', module1)
    port2 = StructureUnit('ff', 'P', module2)
    port3 = StructureUnit('ff', 'P', module2)
    print(port1.address)
    print(port2.address)
    print(port3.address)
    print(module1.address)
    print(module2.address)
    print(chassis.address)
    print(resource.address)
