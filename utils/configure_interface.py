from ncclient import manager

def edit_interface_config(router_ipaddress,router_technology,port,username,password, template):
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

            result = m.edit_config(target='running', config=template)
        
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
         
            result = m.edit_config(target='running', config=template)
        
        return result
    
    except Exception as e:
        print(f"Error:\n{e}")
        return f"configuration failed!"
    finally:
        m.close_session()

