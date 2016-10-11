def populate_ip(path):
    ip_time_table = {}
    with open(path) as tcpdump:
        for line in tcpdump:
            if line != '\n':
                data = line.split(' ')
                data.remove('>')
                if 'matlab.27000' in data:
                    data.remove('matlab.27000')
                else:
                    data.remove('matlab.27000:')
                time_clean = data[0].split('.')[0]
                in_ip = data[2].split('.')
                ip_clean = in_ip[0]+'.'+in_ip[1]+'.'+in_ip[2]+'.'+in_ip[3]
                ip_time_table[time_clean] = ip_clean
    return ip_time_table
