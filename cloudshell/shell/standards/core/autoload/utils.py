from __future__ import annotations

from typing import TYPE_CHECKING

from cloudshell.api.cloudshell_api import ResourceInfo
from cloudshell.shell.core.driver_context import (
    AutoLoadAttribute,
    AutoLoadDetails,
    AutoLoadResource,
)

if TYPE_CHECKING:
    from cloudshell.shell.standards.autoload_generic_models import GenericResourceModel
    from cloudshell.shell.standards.core.autoload.resource_model import AbstractResource


class AutoloadDetailsBuilder:
    def __init__(
        self, resource_model: GenericResourceModel, existed_resource_info: ResourceInfo
    ):
        self._resource_model = resource_model
        self._cs_resource_id = resource_model.cs_resource_id
        self._existed_resource_info = existed_resource_info
        self._full_name_to_resource = _build_map_name_to_resource(existed_resource_info)

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
        res = self._full_name_to_resource.get(resource.full_name)
        if res:
            uniq_id = res.UniqeIdentifier
        else:
            uniq_id = get_unique_id(self._cs_resource_id, resource)
        return uniq_id

    def _get_relative_address(self, resource: AbstractResource) -> str:
        res = self._full_name_to_resource.get(resource.full_name)
        if res:
            relative_address = res.FullAddress
        else:
            relative_address = str(resource.relative_address)
        return relative_address


def get_unique_id(cs_resource_id: str, resource: AbstractResource) -> str:
    """Get unique ID for the resource.

    If we have cs_resource_id use it for creating unique id.
    """
    if cs_resource_id:
        unique_id = f"{cs_resource_id}+{resource.unique_identifier}"
        unique_id = str(hash(unique_id))
    else:
        unique_id = str(resource.unique_identifier)
    return unique_id


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


def _build_map_name_to_resource(
    existed_resource_info: ResourceInfo,
) -> dict[str, ResourceInfo]:
    dict_ = {existed_resource_info.Name: existed_resource_info}
    for child_info in existed_resource_info.ChildResources:
        dict_.update(_build_map_name_to_resource(child_info))
    return dict_
