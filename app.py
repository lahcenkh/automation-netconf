from flask import Flask, url_for, render_template, request, flash, redirect, Response
from database.db_functions import *
from utils.forms import Add_router_form

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
                        SET router_name = '{r["router_name"]}', router_ipaddress = '{r["router_ipaddress"]}', router_technology = '{r["router_technology"]}'
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
                            INSERT INTO routers_info (router_name, router_ipaddress, router_technology)
                            VALUES ('{r_info["router_name"]}', '{r_info["router_ipaddress"]}', '{r_info["router_technology"]}')
                            """
        db_resulte = add_post_db(query=add_router_query)
        if db_resulte == "added":
            flash("added")
        else:
            flash("failed")
        routers = get_db_info(query='SELECT * FROM routers_info')
        return render_template("hx-routers_info.html", routers=routers)      

# 
@app.route("/interfaces")
def interfaces():
    return render_template("interfaces.html")
