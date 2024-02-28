from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import Regexp, DataRequired, IPAddress

class Add_router_form(FlaskForm):
    router_name = StringField("router_name", validators=[DataRequired()])
    router_ipaddress = StringField("router_ipaddress", validators=[DataRequired(), IPAddress()])
    router_technology = SelectField("router_technology", choices=[("TECH","choose Router Tech"),("HUAWEI", "Huawei"), ("ZTE","ZTE"), ("NOKIA","Nokia"), ("CISCO","Cisco")])
    submit = SubmitField("ADD Router")