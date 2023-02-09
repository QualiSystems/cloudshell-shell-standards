from cloudshell.shell.standards.attribute_names import (
    DISABLE_SNMP,
    ENABLE_SNMP,
    SNMP_READ_COMMUNITY,
    SNMP_V3_AUTH_PROTOCOL,
    SNMP_V3_PASSWORD,
    SNMP_V3_PRIVACY_PROTOCOL,
    SNMP_V3_PRIVATE_KEY,
    SNMP_V3_USER,
    SNMP_VERSION,
    SNMP_WRITE_COMMUNITY,
)
from cloudshell.shell.standards.resource_config_generic_models import GenericSnmpConfig


def test_snmp_config(api):
    shell_name = "Shell name"

    attributes = {
        SNMP_READ_COMMUNITY: "community",
        SNMP_WRITE_COMMUNITY: "write community",
        SNMP_V3_USER: "snmp user",
        SNMP_V3_PASSWORD: "snmp password",
        SNMP_V3_PRIVATE_KEY: "snmp private key",
        SNMP_V3_AUTH_PROTOCOL: "snmp auth protocol",
        SNMP_V3_PRIVACY_PROTOCOL: "snmp priv protocol",
        SNMP_VERSION: "v2c",
        ENABLE_SNMP: "True",
        DISABLE_SNMP: "False",
    }
    attributes = {f"{shell_name}.{key}": value for key, value in attributes.items()}

    config = GenericSnmpConfig(
        shell_name,
        "resource name",
        "resource name",
        "address",
        "family name",
        attributes,
        api,
    )
    assert "community" == config.snmp_read_community
    assert "write community" == config.snmp_write_community
    assert "snmp user" == config.snmp_v3_user
    assert "snmp password" == config.snmp_v3_password
    assert "snmp private key" == config.snmp_v3_private_key
    assert "snmp auth protocol" == config.snmp_v3_auth_protocol
    assert "snmp priv protocol" == config.snmp_v3_priv_protocol
    assert "v2c" == config.snmp_version
    assert "True" == config.enable_snmp
    assert "False" == config.disable_snmp
