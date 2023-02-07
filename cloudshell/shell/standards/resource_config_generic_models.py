from cloudshell.shell.standards import attribute_names
from cloudshell.shell.standards.core.resource_config_entities import (
    GenericResourceConfig,
    PasswordAttrRO,
    ResourceAttrRO,
)


class GenericSnmpConfig(GenericResourceConfig):
    snmp_read_community = PasswordAttrRO(attribute_names.SNMP_READ_COMMUNITY)
    snmp_write_community = PasswordAttrRO(attribute_names.SNMP_WRITE_COMMUNITY)
    snmp_v3_user = ResourceAttrRO(attribute_names.SNMP_V3_USER)
    snmp_v3_password = PasswordAttrRO(attribute_names.SNMP_V3_PASSWORD)
    snmp_v3_private_key = ResourceAttrRO(attribute_names.SNMP_V3_PRIVATE_KEY)
    snmp_v3_auth_protocol = ResourceAttrRO(attribute_names.SNMP_V3_AUTH_PROTOCOL)
    snmp_v3_priv_protocol = ResourceAttrRO(attribute_names.SNMP_V3_PRIVACY_PROTOCOL)
    snmp_version = ResourceAttrRO(attribute_names.SNMP_VERSION)
    enable_snmp = ResourceAttrRO(attribute_names.ENABLE_SNMP)
    disable_snmp = ResourceAttrRO(attribute_names.DISABLE_SNMP)


class GenericCLIConfig(GenericResourceConfig):
    user = ResourceAttrRO(attribute_names.USER)
    password = PasswordAttrRO(attribute_names.PASSWORD)
    enable_password = PasswordAttrRO(attribute_names.ENABLE_PASSWORD)
    cli_connection_type = ResourceAttrRO(attribute_names.CLI_CONNECTION_TYPE)
    cli_tcp_port = ResourceAttrRO(attribute_names.CLI_TCP_PORT)
    sessions_concurrency_limit = ResourceAttrRO(
        attribute_names.SESSION_CONCURRENCY_LIMIT
    )


class GenericConsoleServerConfig(GenericResourceConfig):
    console_server_ip_address = ResourceAttrRO(
        attribute_names.CONSOLE_SERVER_IP_ADDRESS
    )
    console_user = ResourceAttrRO(attribute_names.CONSOLE_USER)
    console_port = ResourceAttrRO(attribute_names.CONSOLE_PORT)
    console_password = PasswordAttrRO(attribute_names.CONSOLE_PASSWORD)


class GenericBackupConfig(GenericResourceConfig):
    backup_location = ResourceAttrRO(attribute_names.BACKUP_LOCATION)
    backup_type = ResourceAttrRO(attribute_names.BACKUP_TYPE)
    backup_user = ResourceAttrRO(attribute_names.BACKUP_USER)
    backup_password = PasswordAttrRO(attribute_names.BACKUP_PASSWORD)
