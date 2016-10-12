from ldap_search import *
from pop_ip import *
from pop_ldap import *

ip_time_table = populate_ip('tcpdump.log')
ldap_dict = popluate_ldap('matlab_DB_logs.csv')

with open('LM_TMW-2016-10-11-00-09-55.log') as matlab:
    for line in matlab:
        if '(MLM)' in line:
            data = line.rstrip().split(' ')
            if data[2] in ['IN:', 'OUT:', 'DENIED:']:
                print(data[0], data[1], data[2], data[3])
                ip = ip_time_table[data[0]]
                uid = ldap_dict[ip]
                details = get_ldap_details(uid)
                with open('output.txt', 'a') as output:
                    line = [data[0],data[2].replace(':', ''),
                            data[3].replace('"', ''), ip, uid]
                    for keys in details:
                        line.append(details[keys])
                    output.write(' '.join(line) + '\n')
                
