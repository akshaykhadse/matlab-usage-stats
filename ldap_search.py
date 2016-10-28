from ldap3 import Connection


def ldap_search(uid):
    """
    Gets LDAP details for given user id

    Args:
    -----
    uid: String
        User ID to query ldap server.

    Returns:
    -------
    details: Dict
        Returns a dictionary with employeenumber, employeetype and department
        as keys and respective results as values.
    """
    basedn = 'ou=People,dc=iitb,dc=ac,dc=in'
    attrs = ['employeenumber', 'employeetype']
    query = '(uid=' + uid + ')'

    conn = Connection('ldap.iitb.ac.in', auto_bind=True)
    conn.search(basedn, query, attributes=attrs)
    details = {}
    if len(conn.entries) > 0:
        details['employeenumber'] = str(conn.entries[0].employeenumber)
        details['employeetype'] = str(conn.entries[0].employeetype)
        details['department'] = str(conn.response[0]['dn'].split(',')[2].
                                    split('=')[1])
    else:
        details['employeenumber'] = 'NA'
        details['employeetype'] = 'NA'
        details['department'] = 'NA'
    return(details)
