from __future__ import annotations

from functools import lru_cache
from typing import TYPE_CHECKING

from typing_extensions import Self

from cloudshell.shell.core.driver_context import ResourceCommandContext

from cloudshell.shell.standards.core.namespace import NAMESPACE
from cloudshell.shell.standards.exceptions import ResourceConfigException

if TYPE_CHECKING:
    from cloudshell.api.cloudshell_api import CloudShellAPISession


class ResourceAttrRO:
    def __init__(
        self, name: str, namespace: NAMESPACE = NAMESPACE.SHELL_NAME, default=None
    ):
        self.name = name
        self.namespace = namespace
        self.default = default

    def get_key(self, instance: GenericResourceConfig) -> str:
        return f"{getattr(instance, self.namespace.value)}.{self.name}"

    def __get__(self, instance: GenericResourceConfig, owner):
        if instance is None:
            return self

        return instance.attributes.get(self.get_key(instance), self.default)


class PasswordAttrRO(ResourceAttrRO):
    @lru_cache()
    def _decrypt_password(
        self, api: CloudShellAPISession | None, attr_value: str
    ) -> str:
        if api:
            return api.DecryptPassword(attr_value).Value
        raise ResourceConfigException("Cannot decrypt password, API is not defined")

    def __get__(self, instance: GenericResourceConfig, owner):
        val = super().__get__(instance, owner)
        if val is self or val is self.default:
            return val
        return self._decrypt_password(instance.api, val)


class ResourceListAttrRO(ResourceAttrRO):
    def __init__(
        self,
        name: str,
        namespace: NAMESPACE = NAMESPACE.SHELL_NAME,
        sep: str = ";",
        default=None,
    ):
        if default is None:
            default = []
        super().__init__(name, namespace, default)
        self._sep = sep

    def __get__(self, instance: GenericResourceConfig, owner):
        val = super().__get__(instance, owner)
        if val is self or val is self.default or not isinstance(val, str):
            return val
        return list(filter(bool, map(str.strip, val.split(self._sep))))


class ResourceBoolAttrRO(ResourceAttrRO):
    TRUE_VALUES = {"true", "yes", "y"}
    FALSE_VALUES = {"false", "no", "n"}

    def __init__(
        self, name: str, namespace: NAMESPACE = NAMESPACE.SHELL_NAME, default=False
    ):
        super().__init__(name, namespace, default)

    def __get__(self, instance: GenericResourceConfig, owner):
        val = super().__get__(instance, owner)
        if val is self or val is self.default or not isinstance(val, str):
            return val
        if val.lower() in self.TRUE_VALUES:
            return True
        if val.lower() in self.FALSE_VALUES:
            return False
        raise ValueError(f"{self.name} is boolean attr, but value is {val}")


class GenericResourceConfig:
    def __init__(
        self,
        shell_name: str | None = None,
        name: str | None = None,
        fullname: str | None = None,
        address: str | None = None,
        family_name: str | None = None,
        attributes: dict | None = None,
        supported_os: list[str] | None = None,
        api: CloudShellAPISession | None = None,
        cs_resource_id: str | None = None,
    ):
        self.attributes = attributes or {}
        self.shell_name = shell_name
        self.name = name
        self.supported_os = supported_os or []
        self.fullname = fullname
        self.address = address  # The IP address of the resource
        self.family_name = family_name  # The resource family
        self.namespace_prefix = f"{self.shell_name}"
        self.api = api
        self.cs_resource_id = cs_resource_id

        if not shell_name:
            raise DeprecationWarning("1gen Shells doesn't supported")

    @classmethod
    def from_context(
        cls,
        shell_name: str,
        context: ResourceCommandContext,
        api: CloudShellAPISession | None = None,
        supported_os: list[str] | None = None,
    ) -> Self:
        """Creates an instance of a Resource by given context."""
        return cls(
            shell_name=shell_name,
            name=context.resource.name,
            fullname=context.resource.fullname,
            address=context.resource.address,
            family_name=context.resource.family,
            attributes=dict(context.resource.attributes),
            supported_os=supported_os,
            api=api,
            cs_resource_id=context.resource.id,
        )
