def cidr_to_netmask(cidr):
    return '.'.join([str((0xffffffff << (32 - int(cidr)) >> i) & 0xff) for i in [24, 16, 8, 0]])

def netmask_to_cidr(netmask):
    return sum([bin(int(bits)).count("1") for bits in netmask.split(".")])