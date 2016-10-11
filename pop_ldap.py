def popluate_ldap(path):
    ldap_dict = {}
    with open(path) as ldap_ip:
        for line in ldap_ip:
            entry = line.split(',')[:2]
            ldap_dict[entry[1].replace('"', '')] = entry[0].replace('"', '')
    return ldap_dict
