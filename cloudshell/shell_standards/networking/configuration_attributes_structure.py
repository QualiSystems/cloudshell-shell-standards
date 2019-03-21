#!/usr/bin/python
# -*- coding: utf-8 -*-
from cloudshell.shell_standards.base_configuration_attr_structure import BaseGenericResource, \
    ROResourceAttr
from cloudshell.shell_standards.attribute import RESOURCE


class GenericNetworkingResource(BaseGenericResource):
    backup_location = ROResourceAttr(ROResourceAttr.LVL.NAMESPACE, RESOURCE.ATTRIBUTE.BACKUP_LOCATION)
    backup_type = ROResourceAttr(ROResourceAttr.LVL.NAMESPACE, 'Backup Type')
    backup_user = ROResourceAttr(ROResourceAttr.LVL.NAMESPACE, 'Backup User')
    backup_password = ROResourceAttr(ROResourceAttr.LVL.NAMESPACE, 'Backup Password')
    vrf_management_name = ROResourceAttr(ROResourceAttr.LVL.NAMESPACE, 'VRF Management Name')
    user = ROResourceAttr(ROResourceAttr.LVL.NAMESPACE, 'User')
    password = ROResourceAttr(ROResourceAttr.LVL.NAMESPACE, 'Password')
    enable_password = ROResourceAttr(ROResourceAttr.LVL.NAMESPACE, 'Enable Password')
    power_management = ROResourceAttr(ROResourceAttr.LVL.NAMESPACE, 'Power Management')
    sessions_concurrency_limit = ROResourceAttr(
        ROResourceAttr.LVL.NAMESPACE, 'Sessions Concurrency Limit')
    snmp_read_community = ROResourceAttr(ROResourceAttr.LVL.NAMESPACE, 'SNMP Read Community')
    snmp_write_community = ROResourceAttr(ROResourceAttr.LVL.NAMESPACE, 'SNMP Write Community')
    snmp_v3_user = ROResourceAttr(ROResourceAttr.LVL.NAMESPACE, 'SNMP V3 User')
    snmp_v3_password = ROResourceAttr(ROResourceAttr.LVL.NAMESPACE, 'SNMP V3 Password')
    snmp_v3_private_key = ROResourceAttr(ROResourceAttr.LVL.NAMESPACE, 'SNMP V3 Private Key')
    snmp_v3_auth_protocol = ROResourceAttr(
        ROResourceAttr.LVL.NAMESPACE, 'SNMP V3 Authentication Protocol')
    snmp_v3_priv_protocol = ROResourceAttr(ROResourceAttr.LVL.NAMESPACE, 'SNMP V3 Privacy Protocol')
    snmp_version = ROResourceAttr(ROResourceAttr.LVL.NAMESPACE, 'SNMP Version')
    enable_snmp = ROResourceAttr(ROResourceAttr.LVL.NAMESPACE, 'Enable SNMP')
    disable_snmp = ROResourceAttr(ROResourceAttr.LVL.NAMESPACE, 'Disable SNMP')
    console_server_ip_address = ROResourceAttr(
        ROResourceAttr.LVL.NAMESPACE, 'Console Server IP Address')
    console_user = ROResourceAttr(ROResourceAttr.LVL.NAMESPACE, 'Console User')
    console_port = ROResourceAttr(ROResourceAttr.LVL.NAMESPACE, 'Console Port')
    console_password = ROResourceAttr(ROResourceAttr.LVL.NAMESPACE, 'Console Password')
    cli_connection_type = ROResourceAttr(ROResourceAttr.LVL.NAMESPACE, 'CLI Connection Type')
    cli_tcp_port = ROResourceAttr(ROResourceAttr.LVL.NAMESPACE, 'CLI TCP Port')
