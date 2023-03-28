from __future__ import annotations

from typing import TYPE_CHECKING

from cloudshell.shell.core.driver_context import (
    AutoLoadAttribute,
    AutoLoadDetails,
    AutoLoadResource,
)

from cloudshell.shell.standards.core.autoload.existed_resource_info import (
    ExistedResourceInfo,
)

if TYPE_CHECKING:
    from cloudshell.shell.standards.autoload_generic_models import GenericResourceModel
    from cloudshell.shell.standards.core.autoload.resource_model import AbstractResource


class AutoloadDetailsBuilder:
    def __init__(
        self,
        resource_model: GenericResourceModel,
        existed_resource_info: ExistedResourceInfo,
    ):
        self._resource_model = resource_model
        self._existed_resource_info = existed_resource_info
        self._updated_rel_path_map = {}

    def _build_branch(self, resource: AbstractResource) -> AutoLoadDetails:
        resource.shell_name = resource.shell_name or self._resource_model.shell_name
        autoload_details = AutoLoadDetails(
            self._get_autoload_resources(resource),
            self._get_autoload_attributes(resource),
        )

        for child_resource in resource.extract_sub_resources():
            if not is_module_without_children(child_resource):
                child_details = self._build_branch(child_resource)
                autoload_details.resources.extend(child_details.resources)
                autoload_details.attributes.extend(child_details.attributes)
        return autoload_details

    def build_details(self) -> AutoLoadDetails:
        return self._build_branch(self._resource_model)

    def _get_autoload_resources(
        self, resource: AbstractResource
    ) -> list[AutoLoadResource]:
        relative_address = self._get_relative_address(resource)
        if relative_address:
            autoload_resource = AutoLoadResource(
                model=resource.cloudshell_model_name,
                name=resource.name,
                relative_address=relative_address,
                unique_identifier=self._get_uniq_id(resource),
            )
            result = [autoload_resource]
        else:
            result = []
        return result

    def _get_autoload_attributes(
        self, resource: AbstractResource
    ) -> list[AutoLoadAttribute]:
        return [
            AutoLoadAttribute(
                relative_address=self._get_relative_address(resource),
                attribute_name=str(name),
                attribute_value=str(value),
            )
            for name, value in resource.attributes.items()
            if value is not None
        ]

    def _get_uniq_id(self, resource: AbstractResource) -> str:
        uniq_id = self._existed_resource_info.get_uniq_id(resource.full_name)
        if not uniq_id:
            uniq_id = get_unique_id(self._existed_resource_info, resource)
        return uniq_id

    def _get_relative_address(self, resource: AbstractResource) -> str:
        addr = self._existed_resource_info.get_address(resource.full_name)
        name = self._existed_resource_info.get_name_by_unique_id(
            resource.unique_identifier
        )
        if addr:
            # we should return address without root resource name
            addr = addr.split("/", 1)[-1]

        elif name and name.endswith(resource.full_name.split("/", 1)[-1]):
            addr = self._existed_resource_info.get_address(name)
            if addr:
                addr = addr.split("/", 1)[-1]

        else:
            addr = str(resource.relative_address)
            if not addr:
                return ""
            parent_rel_path = self._updated_rel_path_map.get(
                str(resource.parent.relative_address)
            )
            if parent_rel_path:
                addr = addr.replace(
                    f"{str(resource.parent.relative_address)}/", f"{parent_rel_path}/"
                )

            i = 0
            new_addr = addr
            while self._existed_resource_info.check_address_exists(addr):
                addr = f"{new_addr}-{i}"
                i += 1

        if addr != str(resource.relative_address):
            self._updated_rel_path_map[str(resource.relative_address)] = addr
        return addr


def get_unique_id(r_info: ExistedResourceInfo, resource: AbstractResource) -> str:
    """Get unique ID for the resource."""
    unique_id = f"{r_info.uniq_id}+{resource.unique_identifier}"
    return str(hash(unique_id))


def is_module_without_children(resource: AbstractResource) -> bool:
    from cloudshell.shell.standards.autoload_generic_models import (
        GenericModule,
        GenericSubModule,
    )

    children = resource.extract_sub_resources()
    if isinstance(resource, GenericSubModule):
        return not children
    elif isinstance(resource, GenericModule):
        return all(map(is_module_without_children, children))
    else:
        return False
