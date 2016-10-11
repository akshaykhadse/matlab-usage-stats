with open('data/LM_TMW-2016-10-11-00-09-55.log') as matlab:
    for line in matlab:
        if '(MLM)' in line:
            data = line.rstrip().split(' ')
            if data[2] in ['IN:', 'OUT:', 'DENIED:']:
                print(data[0], data[1], data[2], data[3])
