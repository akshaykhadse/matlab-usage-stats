import datetime

def time(x):
    return datetime.datetime.fromtimestamp(int(x)).strftime('%H:%M:%S')

def populate_ip(path):
    """tcpdump log"""
    ip_time_table = {}
    with open(path) as tcpdump:
        for line in tcpdump:
            if line != '\n':
                data = line.split('   ')
                time_clean = time(data[0])
                ip_clean = data[1]
                ip_time_table[time_clean] = ip_clean
    return ip_time_table
