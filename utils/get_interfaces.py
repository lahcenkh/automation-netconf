from ncclient import manager
import xmltodict
from pprint import pprint
from tabulate import tabulate
import sqlite3

DATABASE_PATH = "../database/database.db"
def get_db_info(query):
    try:
        connection = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
            # Create a cursor
        cursor = connection.cursor()
        # Execute a SELECT statement
        cursor.execute(query)
        # Fetch the data
        results = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        result_dicts = [dict(zip(columns, row)) for row in results]
        # Close the connection
        connection.close()
        return result_dicts
        
    except Exception as e:
        print(f"Error Happened:\n{e}")
        connection.close()
        return "Error"
def update_interfaces_table(query):
    try:
        connection = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
        # Create a cursor object
        cursor = connection.cursor()
        # Insert data into the table
        cursor.execute(query)
        # Commit the changes
        connection.commit()
        # Close the connection
        connection.close()
        return "added"
    except Exception as e:
        print(f"Error Happened:\n {e}")
        connection.close()
        return "Error!"

def interfaces_status(router_ipaddress,router_technology,port,username,password):
    try:
        if str(router_technology).lower() == "huawei".lower():
            m = manager.connect(
                host=router_ipaddress,
                port=port,
                username=username,
                password=password,
                hostkey_verify=False,
                device_params={'name': "huaweiyang"},
                allow_agent=False,
                look_for_keys=False
            )
            filter_interfaces = """
                            <filter type="subtree">
                            <system xmlns="http://www.huawei.com/netconf/vrp/huawei-system">
                                <systemInfo>
                                    <sysName></sysName>
                                </systemInfo>
                            </system>
                            <ifm xmlns="http://www.huawei.com/netconf/vrp/huawei-ifm">
                                <interfaces>
                                <interface>
                                    <ifName></ifName>
                                    <ifAdminStatus></ifAdminStatus>
                                    <ifDescr></ifDescr>
                                    <ifDynamicInfo>
                                        <ifOperStatus></ifOperStatus>
                                        <ifPhyStatus></ifPhyStatus>
                                        <ifOperSpeed></ifOperSpeed>
                                        <ifV4State></ifV4State>
                                        <ifV6State></ifV6State>
                                        <ifCtrlFlapDamp></ifCtrlFlapDamp>
                                        <ifOperMac></ifOperMac>
                                    </ifDynamicInfo>
                                    <mainIpAddr>
                                        <ifIpAddr></ifIpAddr>
                                        <subnetMask></subnetMask>
                                    </mainIpAddr>
                                    <ifClearedStat>
                                        <inUseRate></inUseRate>
                                        <outUseRate></outUseRate>
                                    </ifClearedStat>
                                </interface>
                                </interfaces>
                            </ifm>
                            </filter>
                            """
            reply = m.get(filter_interfaces).data_xml
            data_inter_dict = xmltodict.parse(reply)
            
            interfaces_huawei = {}
            for interface in data_inter_dict["data"]["ifm"]["interfaces"]["interface"]:
                if interface.get("ifName") not in interfaces_huawei:
                        interfaces_huawei[interface.get("ifName")] = {}
                        interfaces_huawei[interface.get("ifName")]["router_name"] = data_inter_dict["data"]["system"]["systemInfo"]["sysName"]
                        interfaces_huawei[interface.get("ifName")]["interface_name"] = interface.get("ifName")
                        interfaces_huawei[interface.get("ifName")]["admin_state"] = interface.get("ifAdminStatus")
                        interfaces_huawei[interface.get("ifName")]["description"] = interface.get("ifDescr")
                        interfaces_huawei[interface.get("ifName")]["operation_state"] = interface.get("ifDynamicInfo").get("ifOperStatus")
                        interfaces_huawei[interface.get("ifName")]["speed"] = interface.get("ifDynamicInfo").get("ifOperSpeed")
                        interfaces_huawei[interface.get("ifName")]["mac_address"] = interface.get("ifDynamicInfo").get("ifOperMac")
                        interfaces_huawei[interface.get("ifName")]["ipaddress"] = interface.get("mainIpAddr").get("ifIpAddr")
                        interfaces_huawei[interface.get("ifName")]["mask"] = interface.get("mainIpAddr").get("subnetMask")
        
            return interfaces_huawei
        
        elif str(router_technology).lower() == "cisco".lower():
            m = manager.connect(
                host=router_ipaddress,
                port=port,
                username=username,
                password=password,
                hostkey_verify=False,
                device_params={'name': "csr"},
                timeout=700,
            )
            filter_interfaces = """
                                <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                                    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                                    <hostname></hostname>
                                    </native> 
                                    <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                                    </interfaces>
                                    <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                                    </interfaces-state>
                                </filter>
                                """
            reply = m.get(filter_interfaces).data_xml
            data_inter_dict = xmltodict.parse(reply)
            
            interfaces_cisco = {}
            for interface in data_inter_dict["data"]["interfaces"]["interface"]:
                if interface.get("name") not in interfaces_cisco:
                        interfaces_cisco[interface.get("name")] = {}
                        interfaces_cisco[interface.get("name")]["router_name"] = data_inter_dict["data"]["native"]["hostname"]
                        interfaces_cisco[interface.get("name")]["interface_name"] = interface.get("name")
                        interfaces_cisco[interface.get("name")]["description"] = interface.get("description")
                        
                        if "address" in interface.get("ipv4"):
                            interfaces_cisco[interface.get("name")]["ipaddress"] = interface.get("ipv4").get("address").get("ip")
                            interfaces_cisco[interface.get("name")]["mask"] = interface.get("ipv4").get("address").get("netmask")
                        else:
                            interfaces_cisco[interface.get("name")]["ipaddress"] = "None"
                            interfaces_cisco[interface.get("name")]["mask"] = "None"
          
            for interface_state in data_inter_dict["data"]["interfaces-state"]["interface"]:
                for inter_key in interfaces_cisco.keys():
                    if inter_key in interface_state["name"]:
                        interfaces_cisco[inter_key]["admin_state"] = interface_state["admin-status"]
                        interfaces_cisco[inter_key]["operation_state"] = interface_state["oper-status"]
                        interfaces_cisco[inter_key]["mac_address"] = interface_state["phys-address"]
                        interfaces_cisco[inter_key]["speed"] = interface_state["speed"]

            return interfaces_cisco
        
    except Exception as e:
        print(f"Error:\n{e}")
        return "Error!"
    finally:
        m.close_session()

routers = get_db_info(query='SELECT * FROM routers_info')

def main(routers):
    interfaces = []
    for router in routers:
        if router["router_technology"].lower() == "HUAWEI".lower():
            result = interfaces_status(router_ipaddress=router["router_ipaddress"], router_technology=router["router_technology"], port=22,username="lahcen", password="Netconf@2021")
        elif router["router_technology"].lower() == "CSICO".lower():
            result = interfaces_status(router_ipaddress=router["router_ipaddress"], router_technology=router["router_technology"], port=830,username="lahcen", password="Netconf@2021")
        else:
            result = interfaces_status(router_ipaddress=router["router_ipaddress"], router_technology=router["router_technology"], port=830,username="lahcen", password="Netconf@2021")

        for inter in result.keys():
            interfaces.append(result[inter])
    
    return interfaces
                

result = main(routers)

update_interfaces_table(query="DELETE FROM interfaces")
for interface in result:
    query_interfaces = f"""
    INSERT INTO interfaces (router_name, interface_name, description, admin_state, operation_state, mac_address, speed, ipaddress, mask)
    VALUES ('{interface["router_name"]}', '{interface["interface_name"]}', '{interface["description"]}', '{interface["admin_state"]}','{interface["operation_state"]}','{interface["mac_address"]}','{interface["speed"]}', '{interface["ipaddress"]}','{interface["mask"]}')
    """
    update_interfaces_table(query_interfaces)

        