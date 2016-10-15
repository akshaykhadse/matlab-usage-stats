from ldap3 import Server, Connection, ALL

def get_ldap_details(uid):
    basedn = 'ou=People,dc=iitb,dc=ac,dc=in'
    attrs = ['employeenumber', 'employeetype']
    query = '(uid=' + uid + ')'

    conn = Connection('ldap.iitb.ac.in', auto_bind=True)
    result = conn.search(basedn, query, attributes = attrs)

    details = {}
    details['employeenumber'] = str(conn.entries[0].employeenumber)
    details['employeetype'] = str(conn.entries[0].employeetype)
    details['department'] = str(conn.response[0]['dn'].split(',')[2].split('=')[1])
    return(details)

if __name__ == '__main__':
    print(get_ldap_details('153079005'))
