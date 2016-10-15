from ldap_search import *
from pop_ip import *
from pop_ldap import *

ip_time_table = populate_ip('data/src_ip_log1')
ldap_dict = popluate_ldap('data/matlab_DB_active.csv')
matlab_log = 'data/LM_TMW3.log'

x = 0
y = 0
with open(matlab_log) as matlab:
    for line in matlab:
        x=x+1
        if '(MLM)' in line:
            data = line.rstrip().split(' ')
            try:
                if data[2] in ['IN:', 'OUT:', 'DENIED:']:
                    #print(data[0], data[1], data[2], data[3])
                    ip = ip_time_table[data[0]]
                    uid = ldap_dict[ip]
                    details = get_ldap_details(uid)
                    with open('output.txt', 'a') as output:
                        line = [data[0],data[2].replace(':', ''),
                                data[3].replace('"', ''), ip, uid]
                        for keys in details:
                            line.append(details[keys])
                        output.write(' '.join(line) + '\n')
                        print(' '.join(line))
            except KeyError:
                try:
                    ip = ip_time_table[data[0]]
                    print(data[0],data[2].replace(':', ''),data[3].replace('"', ''), ip)
                except KeyError:
                    y = y+1
                    print(x, y)
