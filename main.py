from ldap_search import ldap_search
from pop_ip import pop_ip
from pop_ldap import pop_ldap


def process(active_csv, archive_csv, matlab_log, port_activity_log):
    """
    Processes Matlab debug log file line by line to produce a file output.txt.
    Output has columns with timestamp, action, toolbox, ip, uid, rollnumber,
    type and department.

    Args:
    -----
    active_csv: String
        Path to CSV file for active users.

    archive_csv: String
        Path to CSV file for previous users.

    matlab_log: String
        Path to matlab debug log file.

    port_activity_log: String
        Path to port activity log file.

    Returns:
    --------
    None
    """
    ip_time_table = pop_ip(port_activity_log)
    with open(matlab_log) as matlab:
        for line in matlab:
            if '(MLM)' in line.rstrip():
                data = line.split(' ')
                if data[2] in ['IN:', 'OUT:', 'DENIED:']:
                    try:
                        ip = ip_time_table[data[0]]
                    except KeyError:
                        ip = 'NA'
                    uid = pop_ldap(ip, active_csv, archive_csv)
                    details = ldap_search(uid)

                    with open('output.txt', 'a') as output:
                        line = [data[0], data[2].replace(':', ''),
                                data[3].replace('"', ''), ip, uid]
                        for keys in details:
                            line.append(details[keys])
                        output.write(' '.join(line) + '\n')
    return None


if __name__ == '__main__':
    active_csv = 'data/matlab_DB_active.csv'
    archive_csv = 'data/matlab_DB_archive3.csv'
    matlab_log = 'data/LM_TMW3.log'
    port_activity_log = 'data/src_ip_log1'
    process(active_csv, archive_csv, matlab_log, port_activity_log)
