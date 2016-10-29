def pop_ldap(ip, active_csv, archive_csv):
    """
    Finds LDAP UID for given IP from Portal Log Files. For multiple entries in
    log, latest UID will be returned.

    First active file will be queried followed by archived file.

    Args:
    -----
    ip: String
        IP address of client.

    active_csv: String
        Path to CSV file for active users.

    archive_csv: String
        Path to CSV file for previous users.

    Returns:
    -------
    uid: String
        Latest UID from Database matching with the input IP Address
    """
    for file in [active_csv, archive_csv]:
        with open(file) as data:
            for line in data:
                fields = line.split(',')
                if fields[1].replace('"', '') == ip:
                    return fields[0].replace('"', '')
    return 'NA'
