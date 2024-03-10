from ncclient import manager
import xmltodict
from pprint import pprint

def interfaces_status(router_ipaddress,router_technology,port,username,password, filter_interfaces):
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
            print(f"|--------------conncting to Router: {router_ipaddress}")
            reply = m.get(filter_interfaces).data_xml
            
            data_inter_dict = xmltodict.parse(reply)
            
            interfaces_huawei = {}
            for interface in data_inter_dict["data"]["ifm"]["interfaces"]["interface"]:
                if interface.get("ifName") not in interfaces_huawei:
                        interfaces_huawei[interface.get("ifName")] = {}
                        interfaces_huawei[interface.get("ifName")]["router_name"] = data_inter_dict["data"]["system"]["systemInfo"]["sysName"]
                        interfaces_huawei[interface.get("ifName")]["router_technology"] = router_technology
                        interfaces_huawei[interface.get("ifName")]["interface_name"] = interface.get("ifName")
                        interfaces_huawei[interface.get("ifName")]["admin_state"] = interface.get("ifAdminStatus")
                        interfaces_huawei[interface.get("ifName")]["description"] = interface.get("ifDescr")
                        interfaces_huawei[interface.get("ifName")]["operation_state"] = interface.get("ifDynamicInfo").get("ifOperStatus")
                        interfaces_huawei[interface.get("ifName")]["speed"] = interface.get("ifDynamicInfo").get("ifOperSpeed")
                        interfaces_huawei[interface.get("ifName")]["mac_address"] = interface.get("ifDynamicInfo").get("ifOperMac")
                        if interface.get("mainIpAddr").get("ifIpAddr") == "0.0.0.0" or interface.get("mainIpAddr").get("subnetMask") == "0.0.0.0":
                            interfaces_huawei[interface.get("ifName")]["ipaddress"] = "None"
                            interfaces_huawei[interface.get("ifName")]["mask"] = "None"
                        else:
                            interfaces_huawei[interface.get("ifName")]["ipaddress"] = interface.get("mainIpAddr").get("ifIpAddr")
                            interfaces_huawei[interface.get("ifName")]["mask"] = interface.get("mainIpAddr").get("subnetMask")
            m.close_session()
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
            print(f"|--------------conncting to Router: {router_ipaddress}")
            reply = m.get(filter_interfaces).data_xml
            data_inter_dict = xmltodict.parse(reply)
            
            interfaces_cisco = {}
            for interface in data_inter_dict["data"]["interfaces"]["interface"]:
                if interface.get("name") not in interfaces_cisco:
                        interfaces_cisco[interface.get("name")] = {}
                        interfaces_cisco[interface.get("name")]["router_name"] = data_inter_dict["data"]["native"]["hostname"]
                        interfaces_cisco[interface.get("name")]["router_technology"] = router_technology
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
            m.close_session()
            return interfaces_cisco
        else:
            return "not supported"
        
    except Exception as e:
        print(f"Error:\n{e}")
        return "Error"

def interface_status(router_ipaddress,router_technology,port,username,password, filter_interfaces):
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
            print(f"|--------------conncting to Router: {router_ipaddress}")
            reply = m.get(filter_interfaces).data_xml
            
            data_inter_dict = xmltodict.parse(reply)
            
            interfaces_huawei = {}
            interface = data_inter_dict["data"]["ifm"]["interfaces"]["interface"]
            if interface.get("ifName") not in interfaces_huawei:
                    interfaces_huawei[interface.get("ifName")] = {}
                    interfaces_huawei[interface.get("ifName")]["router_name"] = data_inter_dict["data"]["system"]["systemInfo"]["sysName"]
                    interfaces_huawei[interface.get("ifName")]["router_technology"] = router_technology
                    interfaces_huawei[interface.get("ifName")]["interface_name"] = interface.get("ifName")
                    interfaces_huawei[interface.get("ifName")]["admin_state"] = interface.get("ifAdminStatus")
                    interfaces_huawei[interface.get("ifName")]["description"] = interface.get("ifDescr")
                    interfaces_huawei[interface.get("ifName")]["operation_state"] = interface.get("ifDynamicInfo").get("ifOperStatus")
                    interfaces_huawei[interface.get("ifName")]["speed"] = interface.get("ifDynamicInfo").get("ifOperSpeed")
                    interfaces_huawei[interface.get("ifName")]["mac_address"] = interface.get("ifDynamicInfo").get("ifOperMac")
                    if interface.get("mainIpAddr").get("ifIpAddr") == "0.0.0.0" or interface.get("mainIpAddr").get("subnetMask") == "0.0.0.0":
                        interfaces_huawei[interface.get("ifName")]["ipaddress"] = "None"
                        interfaces_huawei[interface.get("ifName")]["mask"] = "None"
                    else:
                        interfaces_huawei[interface.get("ifName")]["ipaddress"] = interface.get("mainIpAddr").get("ifIpAddr")
                        interfaces_huawei[interface.get("ifName")]["mask"] = interface.get("mainIpAddr").get("subnetMask")
            m.close_session()
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
            print(f"|--------------conncting to Router: {router_ipaddress}")
            reply = m.get(filter_interfaces).data_xml
            data_inter_dict = xmltodict.parse(reply)
            interfaces_cisco = {}
            interface = data_inter_dict["data"]["interfaces"]["interface"]
            if interface.get("name")["#text"] not in interfaces_cisco:
                interfaces_cisco[interface.get("name")["#text"]] = {}
                interfaces_cisco[interface.get("name")["#text"]]["router_name"] = data_inter_dict["data"]["native"]["hostname"]
                interfaces_cisco[interface.get("name")["#text"]]["router_technology"] = router_technology
                interfaces_cisco[interface.get("name")["#text"]]["interface_name"] = interface.get("name")["#text"]
                interfaces_cisco[interface.get("name")["#text"]]["description"] = interface.get("description")
                
                if "address" in interface.get("ipv4"):
                    interfaces_cisco[interface.get("name")["#text"]]["ipaddress"] = interface.get("ipv4").get("address").get("ip")
                    interfaces_cisco[interface.get("name")["#text"]]["mask"] = interface.get("ipv4").get("address").get("netmask")
                else:
                    interfaces_cisco[interface.get("name")["#text"]]["ipaddress"] = "None"
                    interfaces_cisco[interface.get("name")["#text"]]["mask"] = "None"
          
            interface_state = data_inter_dict["data"]["interfaces-state"]["interface"]
            for inter_key in interfaces_cisco.keys():
                if inter_key in interface_state["name"]["#text"]:
                    interfaces_cisco[inter_key]["admin_state"] = interface_state["admin-status"]
                    interfaces_cisco[inter_key]["operation_state"] = interface_state["oper-status"]
                    interfaces_cisco[inter_key]["mac_address"] = interface_state["phys-address"]
                    interfaces_cisco[inter_key]["speed"] = interface_state["speed"]
            m.close_session()
            return interfaces_cisco
        else:
            return "not supported"
        
    except Exception as e:
        print(f"Error:\n{e}")
        return "Error"        

def get_routers_interfaces_state(routers):
    interfaces = []
    for router in routers:
        if router["router_technology"].lower() == "HUAWEI".lower():
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
            result = interfaces_status(router_ipaddress=router["router_ipaddress"], router_technology=router["router_technology"], port=22,username="lahcen", password="Netconf@2021", filter_interfaces=filter_interfaces)
        elif router["router_technology"].lower() == "CISCO".lower():
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
            result = interfaces_status(router_ipaddress=router["router_ipaddress"], router_technology=router["router_technology"], port=830,username="lahcen", password="Netconf@2021", filter_interfaces=filter_interfaces)
        else:
            result = "Not supported"
        if "Error" not in result:
            for inter in result.keys():
                interfaces.append(result[inter])
        
    return interfaces

def get_router_interface_info(router_info, interface):
    interfaces = []
    if router_info["router_technology"].lower() == "HUAWEI".lower():
            filter_interfaces = f"""
                            <filter type="subtree">
                            <system xmlns="http://www.huawei.com/netconf/vrp/huawei-system">
                                <systemInfo>
                                    <sysName></sysName>
                                </systemInfo>
                            </system>
                            <ifm xmlns="http://www.huawei.com/netconf/vrp/huawei-ifm">
                                <interfaces>
                                <interface>
                                    <ifName>{interface}</ifName>
                                </interface>
                                </interfaces>
                            </ifm>
                            </filter>
                            """
            result = interface_status(router_ipaddress=router_info["router_ipaddress"], router_technology=router_info["router_technology"], port=22,username="lahcen", password="Netconf@2021", filter_interfaces=filter_interfaces)
            
    elif router_info["router_technology"].lower() == "CISCO".lower():
        filter_interfaces = f"""
                                <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                                    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                                    <hostname></hostname>
                                    </native> 
                                    <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                                    <interface>
                                        <name>{interface}</name>
                                    </interface>
                                    </interfaces>
                                    <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                                    <interface>
                                        <name>{interface}</name>
                                    </interface>
                                    </interfaces-state>
                                </filter>
                                """
        result = interface_status(router_ipaddress=router_info["router_ipaddress"], router_technology=router_info["router_technology"], port=830,username="lahcen", password="Netconf@2021", filter_interfaces=filter_interfaces)
    else:
        result = "Not supported"
    if "Error" not in result:
        for inter in result.keys():
            interfaces.append(result[inter])
        
    return interfaces