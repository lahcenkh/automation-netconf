from jinja2 import Environment , FileSystemLoader
env = Environment(loader=FileSystemLoader("utils/gen_conf_template/templates/"))


def cisco_interface_basic_config(interface_info):
    #get the l2vpn and l3vpn of router by passing router name
    #chose the single homeing template config
    template = env.get_template("interface_config_csr100v.jinja")
    #render config by passing variables dataplan from the form and l2pvn, l2vpn from database
    output = template.render(interface_info=interface_info)
    return output

def huawei_interface_basic_config(interface_info):
    #get the l2vpn and l3vpn of router by passing router name
    #chose the single homeing template config
    template = env.get_template("interface_config_cx600.jinja")
    #render config by passing variables dataplan from the form and l2pvn, l2vpn from database
    output = template.render(interface_info=interface_info)
    return output

