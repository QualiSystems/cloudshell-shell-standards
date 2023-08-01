from __future__ import annotations

from enum import Enum
from ipaddress import IPv4Address

import pytest
from attrs import define

from cloudshell.shell.standards.core.resource_conf import BaseConfig, attr


class EnumSubClass(Enum):
    VALUE_1 = "Value 1"
    VALUE_2 = "Value 2"


@define(slots=False, str=False)
class SimpleConf(BaseConfig):
    str_res_attr: str = attr("Str Attribute")
    int_res_attr: int = attr("Int Attribute")
    enum_res_attr: EnumSubClass = attr("Enum Attribute")
    ip: IPv4Address = attr("IP Address")
    list_attr: list[str] = attr("List Attribute")


@pytest.mark.parametrize(
    ("attr_values", "expected_values"),
    (
        (
            ("str_attr", "12", "Value 2", "192.168.12.13", "a;b,c"),
            (
                "str_attr",
                12,
                EnumSubClass.VALUE_2,
                IPv4Address("192.168.12.13"),
                ["a", "b", "c"],
            ),
        ),
        (
            ("str_attr", "10", "Value 1", "127.0.0.1", ""),
            ("str_attr", 10, EnumSubClass.VALUE_1, IPv4Address("127.0.0.1"), []),
        ),
    ),
)
def test_from_context(api, context_creator, attr_values, expected_values):
    r_name = "resource name"
    r_model = "resource model"
    r_family = "resource family"
    r_address = "resource address"

    r_attributes = dict(
        zip(
            [
                "Str Attribute",
                "Int Attribute",
                "Enum Attribute",
                "IP Address",
                "List Attribute",
            ],
            attr_values,
        )
    )
    r_attributes = {f"{r_model}.{k}": v for k, v in r_attributes.items()}
    context = context_creator(r_name, r_model, r_family, r_address, r_attributes)

    conf = SimpleConf.from_context(context, api)

    str_attr, int_attr, enum_attr, ip_attr, list_attr = expected_values
    assert conf.name == r_name
    assert conf.shell_name == r_model
    assert conf.family_name == r_family
    assert conf.address == r_address
    assert conf.str_res_attr == str_attr
    assert conf.int_res_attr == int_attr
    assert conf.enum_res_attr is enum_attr
    assert conf.ip == ip_attr
    assert str(conf) == f"{type(conf).__name__}({conf.name})"
