from cloudshell.shell_standards import attribute_names
from cloudshell.shell_standards.core.resource_config_entities import ResourceAttrRO, GenericResourceConfig


class GenericSnmpConfig(GenericResourceConfig):
    snmp_read_community = ResourceAttrRO(attribute_names.SNMP_READ_COMMUNITY, ResourceAttrRO.NAMESPACE.SHELL_NAME)
    snmp_write_community = ResourceAttrRO(attribute_names.SNMP_WRITE_COMMUNITY, ResourceAttrRO.NAMESPACE.SHELL_NAME)
    snmp_v3_user = ResourceAttrRO(attribute_names.SNMP_V3_USER, ResourceAttrRO.NAMESPACE.SHELL_NAME)
    snmp_v3_password = ResourceAttrRO(attribute_names.SNMP_V3_PASSWORD, ResourceAttrRO.NAMESPACE.SHELL_NAME)
    snmp_v3_private_key = ResourceAttrRO(attribute_names.SNMP_V3_PRIVATE_KEY, ResourceAttrRO.NAMESPACE.SHELL_NAME)
    snmp_v3_auth_protocol = ResourceAttrRO(attribute_names.SNMP_V3_AUTH_PROTOCOL, ResourceAttrRO.NAMESPACE.SHELL_NAME)
    snmp_v3_priv_protocol = ResourceAttrRO(attribute_names.SNMP_V3_PRIVACY_PROTOCOL,
                                           ResourceAttrRO.NAMESPACE.SHELL_NAME)
    snmp_version = ResourceAttrRO(attribute_names.SNMP_VERSION, ResourceAttrRO.NAMESPACE.SHELL_NAME)
    enable_snmp = ResourceAttrRO(attribute_names.ENABLE_SNMP, ResourceAttrRO.NAMESPACE.SHELL_NAME)
    disable_snmp = ResourceAttrRO(attribute_names.DISABLE_SNMP, ResourceAttrRO.NAMESPACE.SHELL_NAME)


class GenericCLIConfig(GenericResourceConfig):
    user = ResourceAttrRO(attribute_names.USER, ResourceAttrRO.NAMESPACE.SHELL_NAME)
    password = ResourceAttrRO(attribute_names.PASSWORD, ResourceAttrRO.NAMESPACE.SHELL_NAME)
    enable_password = ResourceAttrRO(attribute_names.ENABLE_PASSWORD, ResourceAttrRO.NAMESPACE.SHELL_NAME)
    cli_connection_type = ResourceAttrRO(attribute_names.CLI_CONNECTION_TYPE, ResourceAttrRO.NAMESPACE.SHELL_NAME)
    cli_tcp_port = ResourceAttrRO(attribute_names.CLI_TCP_PORT, ResourceAttrRO.NAMESPACE.SHELL_NAME)
    sessions_concurrency_limit = ResourceAttrRO(attribute_names.SESSION_CONCURRENCY_LIMIT,
                                                ResourceAttrRO.NAMESPACE.SHELL_NAME)


class GenericConsoleServerConfig(GenericResourceConfig):
    console_server_ip_address = ResourceAttrRO(attribute_names.CONSOLE_SERVER_IP_ADDRESS,
                                               ResourceAttrRO.NAMESPACE.SHELL_NAME)
    console_user = ResourceAttrRO(attribute_names.CONSOLE_USER, ResourceAttrRO.NAMESPACE.SHELL_NAME)
    console_port = ResourceAttrRO(attribute_names.CONSOLE_PORT, ResourceAttrRO.NAMESPACE.SHELL_NAME)
    console_password = ResourceAttrRO(attribute_names.CONSOLE_PASSWORD, ResourceAttrRO.NAMESPACE.SHELL_NAME)


class GenericBackupConfig(GenericResourceConfig):
    backup_location = ResourceAttrRO(attribute_names.BACKUP_LOCATION, ResourceAttrRO.NAMESPACE.SHELL_NAME)
    backup_type = ResourceAttrRO(attribute_names.BACKUP_TYPE, ResourceAttrRO.NAMESPACE.SHELL_NAME)
    backup_user = ResourceAttrRO(attribute_names.BACKUP_USER, ResourceAttrRO.NAMESPACE.SHELL_NAME)
    backup_password = ResourceAttrRO(attribute_names.BACKUP_PASSWORD, ResourceAttrRO.NAMESPACE.SHELL_NAME)