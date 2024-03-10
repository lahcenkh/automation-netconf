from flask import Flask, url_for, render_template, request, flash, redirect, Response
from database.db_functions import *
from utils.forms import Add_router_form
from utils.get_interfaces import get_routers_interfaces_state, get_router_interface_info
from utils.gen_conf_template.template_generator import cisco_interface_basic_config, huawei_interface_basic_config
from utils.configure_interface import edit_interface_config
from utils.cirde_to_mask import *

app = Flask(__name__)
app.config["SECRET_KEY"] = "@njbNK4654NKN#"

@app.route("/", methods=["GET", "POST"])
def index():
    form_add = Add_router_form()
    data = {}
    if form_add.validate_on_submit():
        data = {"router_name": form_add.router_name.data,
        "router_ipaddress": form_add.router_ipaddress.data,
        "router_technology": form_add.router_technology.data}

    return render_template("index.html", form=form_add, data=data)

@app.route("/routers_info")
def routers_info():
    return render_template("routers_info.html")

@app.route("/get-routers_info")
def get_routers_info():
    routers = get_db_info(query='SELECT * FROM routers_info')
    return render_template("hx-routers_info.html", routers=routers)

@app.route("/edit-router_info", methods=["GET", "POST"])
def edit_router_info():

    if request.method == "GET":
        router_id = request.args["id"]
        router = get_db_info(query=f'SELECT * FROM routers_info WHERE id = "{router_id}"')
        
        return render_template("hx-from_update.html",router=router[0])
    
    elif request.method == "POST":
        r = request.form
        update_query = f"""
                        UPDATE routers_info
                        SET router_name = '{r["router_name"]}', router_ipaddress = '{r["router_ipaddress"]}', router_technology = '{r["router_technology"]}', netconf_connection = '{r["netconf_connection"]}' 
                        WHERE id = '{r["id"]}';
                        """
        db_resulte = edit_post_db(query=update_query)
        if db_resulte == "updated":
            flash("updated")
        else:
            flash("failed")
        routers = get_db_info(query='SELECT * FROM routers_info')
        return render_template("hx-routers_info.html", routers=routers)

@app.route("/delete-router_info", methods=["DELETE"])
def delete_routers_info():
    router_id = request.args["id"]
    if request.method == "DELETE":
        delete_query = f"DELETE FROM routers_info WHERE id = {router_id}"
        db_resulte = delete_post_db(query=delete_query)  
        if db_resulte == "deleted":
            flash("deleted")
        else:
            flash("failed")
        routers = get_db_info(query='SELECT * FROM routers_info')
        return render_template("hx-routers_info.html", routers=routers)      

@app.route("/add-router_info", methods=["GET", "POST"])
def add_router_info():
    if request.method == "GET":
        return render_template("hx-from_add.html")
    
    elif request.method == "POST":
        r_info = request.form
        add_router_query = f"""
                            INSERT INTO routers_info (router_name, router_ipaddress, router_technology, netconf_connection)
                            VALUES ('{r_info["router_name"]}', '{r_info["router_ipaddress"]}', '{r_info["router_technology"]}', '{r_info["netconf_connection"]}')
                            """
        db_resulte = add_post_db(query=add_router_query)
        if db_resulte == "added":
            flash("added")
        else:
            flash("failed")
        routers = get_db_info(query='SELECT * FROM routers_info')
        return render_template("hx-routers_info.html", routers=routers)    

@app.route("/get-interfaces_info")
def get_interfaces_info():
    routers_interfaces = get_db_info(query='SELECT * FROM interfaces')
    return render_template("hx-interfaces.html", interfaces=routers_interfaces)


@app.route("/interfaces", methods=["GET", "POST"])
def interfaces():
    if request.method == "GET":
        return render_template("interfaces.html")
    
    elif request.method == "POST":
        routers = get_db_info(query='SELECT * FROM routers_info')
        interfaces_info = get_routers_interfaces_state(routers)

        update_interfaces_table(query="DELETE FROM interfaces")
        for interface in interfaces_info:
            query_interfaces = f"""
            INSERT INTO interfaces (router_name, interface_name, description, admin_state, operation_state, mac_address, speed, ipaddress, mask, router_technology)
            VALUES ('{interface["router_name"]}', '{interface["interface_name"]}', '{interface["description"]}', '{interface["admin_state"]}','{interface["operation_state"]}','{interface["mac_address"]}','{interface["speed"]}', '{interface["ipaddress"]}','{interface["mask"]}','{interface["router_technology"]}')
            """
            update_interfaces_table(query_interfaces)
        
        routers_interfaces = get_db_info(query='SELECT * FROM interfaces')
        return render_template("hx-interfaces.html", interfaces=routers_interfaces)


@app.route("/interfaces/edite", methods=["GET", "POST"])
def edit_interfaces_info():
    if request.method == "GET":
        inter_to_edite = request.args.to_dict()
        interface_info = get_db_info(query=f'SELECT * FROM interfaces WHERE router_name = "{inter_to_edite["router_name"]}" AND interface_name = "{inter_to_edite["interface_name"]}"')
        return render_template("hx-edit_form_interface.html", interface_info=interface_info[0])
    elif request.method == "POST":
        new_interface_info = request.form.to_dict()
        router = get_db_info(query=f'SELECT * FROM routers_info WHERE router_name = "{new_interface_info["router_name"]}"')[0]
        
        if router["router_technology"] == "HUAWEI":
            interface_info = {
                                "interface_name":new_interface_info.get("interface_name"),
                                "description":new_interface_info.get("description"),
                                "ipaddress":new_interface_info.get("ipaddress"),
                                "mask": cidr_to_netmask(new_interface_info.get("mask")),
                                "enabled":str(new_interface_info.get("admin_state")),
                            }
            template = huawei_interface_basic_config(interface_info)
            result = edit_interface_config(router_ipaddress=router["router_ipaddress"],port=22 , router_technology=router["router_technology"],username="lahcen", password="Netconf@2021",template=template)
        elif router["router_technology"] == "CISCO":
            interface_info = {
                                "interface_name":new_interface_info.get("interface_name"),
                                "description":new_interface_info.get("description"),
                                "ipaddress":new_interface_info.get("ipaddress"),
                                "mask":new_interface_info.get("mask"),
                                "enabled":str(new_interface_info.get("admin_state")),
                            }
            template = cisco_interface_basic_config(interface_info)
            result = edit_interface_config(router_ipaddress=router["router_ipaddress"],port=830 , router_technology=router["router_technology"],username="lahcen", password="Netconf@2021",template=template)

        if "<ok/>" in str(result):
            inter_new = get_router_interface_info(router,new_interface_info.get("interface_name"))[0]
            query = f"""UPDATE interfaces
                        SET router_name = '{inter_new["router_name"]}', router_technology = '{inter_new["router_technology"]}', interface_name = '{inter_new["interface_name"]}', description = '{inter_new["description"]}' , admin_state = '{inter_new["admin_state"]}', description = '{inter_new["description"]}', operation_state = '{inter_new["operation_state"]}', speed = '{inter_new["speed"]}', mac_address = '{inter_new["mac_address"]}', ipaddress = '{inter_new["ipaddress"]}', mask = '{inter_new["mask"]}'
                        WHERE router_name = '{inter_new["router_name"]}' AND interface_name = '{inter_new["interface_name"]}';"""
            update_interfaces_table(query)
        else:
            print(result)

        routers_interfaces = get_db_info(query='SELECT * FROM interfaces')
        return render_template("hx-interfaces.html", interfaces=routers_interfaces)

