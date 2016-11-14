from parser.ldap_search import ldap_search
from parser.pop_ip import pop_ip
from parser.pop_ldap import pop_ldap
from reports.models import LogEntry


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

                    if data[2].replace(':', '') == 'OUT':
                        entry = LogEntry()
                        entry.uid = uid
                        entry.emp_number = details['employeenumber']
                        entry.emp_type = details['employeetype']
                        entry.department = details['department']
                        entry.package = data[3].replace('"', '')
                        entry.out_time = data[0]
                        entry.save()
                    elif data[2].replace(':', '') == 'DENIED':
                        entry = LogEntry()
                        entry.uid = uid
                        entry.emp_number = details['employeenumber']
                        entry.emp_type = details['employeetype']
                        entry.department = details['department']
                        entry.package = data[3].replace('"', '')
                        entry.out_time = data[0]
                        entry.in_time = 'DENIED'
                        entry.save()
                    else:
                        entry = LogEntry.objects.filter(
                            uid=uid,
                            emp_number=details['employeenumber'],
                            emp_type=details['employeetype'],
                            department=details['department'],
                            package=data[3].replace('"', ''))[0]
                        entry.in_time = data[0]
                        entry.save()
    return None


if __name__ == '__main__':
    active_csv = 'data/matlab_DB_active.csv'
    archive_csv = 'data/matlab_DB_archive.csv'
    matlab_log = 'data/LM_TMW.log'
    port_activity_log = 'data/src_ip_log'
    process(active_csv, archive_csv, matlab_log, port_activity_log)
