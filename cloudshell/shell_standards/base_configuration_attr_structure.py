class ROResourceAttr(object):
    class LVL(object):
        NAMESPACE = 'namespace_prefix'

    def __init__(self, prefix_attr, name, default=None):
        self.prefix_attr = prefix_attr
        self.name = name
        self.default = default

    def get_key(self, instance):
        return '{}.{}'.format(getattr(instance, self.prefix_attr), self.name)

    def __get__(self, instance, owner):
        if instance is None:
            return self

        return instance.attributes.get(self.get_key(instance), self.default)


class BaseGenericResource(object):
    def __init__(self, shell_name=None, name=None, fullname=None, address=None, family=None,
                 attributes=None, supported_os=None):
        """Init method

        :param str shell_name: Shell Name
        :param str name: Resource Name
        :param list supported_os: list of supported OS
        """

        self.attributes = attributes or {}
        self.shell_name = shell_name
        self.name = name
        self.supported_os = supported_os or []
        self.fullname = fullname
        self.address = address  # The IP address of the resource
        self.family = family  # The resource family
        self.namespace_prefix = '{}'.format(self.shell_name)

        if not shell_name:
            raise DeprecationWarning('1gen Shells doesn\'t supported')

    @classmethod
    def from_context(cls, shell_name, context, supported_os=None):
        """Creates an instance of a Resource by given context

        :param str shell_name: Shell Name
        :param list supported_os: list of supported OS
        :param cloudshell.shell.core.driver_context.ResourceCommandContext context:
        :rtype: BaseGenericResource
        """

        return cls(
            shell_name=shell_name,
            name=context.resource.name,
            fullname=context.resource.fullname,
            address=context.resource.address,
            family=context.resource.family,
            attributes=dict(context.resource.attributes),
            supported_os=supported_os,
        )
