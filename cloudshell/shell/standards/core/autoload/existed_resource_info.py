from __future__ import annotations

from functools import wraps
from threading import Event, Thread
from typing import TypeVar

from cloudshell.api.cloudshell_api import CloudShellAPISession, ResourceInfo

from cloudshell.shell.standards.exceptions import BaseStandardException

T = TypeVar("T")


def _wait_until_loaded(fn: T) -> T:
    @wraps(fn)
    def wrapped(self, *args, **kwargs):
        if not self._started.is_set():
            raise BaseStandardException("You have to start loading first")
        self._loaded.wait()
        return fn(self, *args, **kwargs)

    return wrapped


class ExistedResourceInfo:
    def __init__(self, name: str, api: CloudShellAPISession):
        self.name = name
        self._api = api
        self._started = Event()
        self._loaded = Event()
        self._uniq_id = None
        self._full_name_to_uniq_id: dict[str, str] | None = None
        self._full_name_to_address: dict[str, str] | None = None

    @property
    @_wait_until_loaded
    def uniq_id(self) -> str:
        return self._uniq_id

    @_wait_until_loaded
    def get_uniq_id(self, full_name: str) -> str | None:
        return self._full_name_to_uniq_id.get(full_name)

    @_wait_until_loaded
    def get_address(self, full_name: str) -> str | None:
        return self._full_name_to_address.get(full_name)

    def load_data(self) -> None:
        self._started.set()
        Thread(target=self._load_data).start()

    def _load_data(self):
        r_info = self._api.GetResourceDetails(self.name)
        self._uniq_id = r_info.UniqeIdentifier
        self._full_name_to_uniq_id = {}
        self._full_name_to_address = {}

        for child in r_info.ChildResources:
            # Root resource contains invalid uniq id for children but newly loaded child
            # info contains valid uniq id for itself and its children
            updated_child = self._api.GetResourceDetails(child.Name)
            self._build_maps_for_resource(updated_child)

        self._loaded.set()

    def _build_maps_for_resource(self, r_info: ResourceInfo) -> None:
        self._full_name_to_uniq_id[r_info.Name] = r_info.UniqeIdentifier
        self._full_name_to_address[r_info.Name] = r_info.FullAddress
        for child_info in r_info.ChildResources:
            self._build_maps_for_resource(child_info)
