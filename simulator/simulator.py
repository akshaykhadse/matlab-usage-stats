#!/usr/bin/python3.5

from random import uniform, choice, randint
from time import sleep, mktime
from datetime import datetime, timedelta
from ldap3 import Connection
from weakref import ref


def aggregate_license_info(path_to_lmstat):
    packages = []
    with open(path_to_lmstat) as lmstat:
        for line in lmstat:
            if 'Users of' in line:
                fields = line.replace(':', '').split(' ')
                packages.append(Package(fields[2], fields[6]))
    return packages


def aggregate_ldap_info():
    attrs = ['uid']

    ldap = []
    conn = Connection('ldap.iitb.ac.in', auto_bind=True)

    for dept in ['EE', 'AERO', 'CIVIL', 'CSE', 'MATH']:
        basedn = 'ou=' + dept + ',ou=People,dc=iitb,dc=ac,dc=in'
        query = '(&(uid=*)(|(employeetype=dd)(employeetype=fac)(employeetype=pg)\
                           (employeetype=rs)(employeetype=prjstf)(employeetype=stf)\
                           (employeetype=ug)))'
        result = conn.search(basedn, query, attributes=attrs)
        if result is True and len(conn.entries) != 0:
            for item in conn.entries:
                ldap.append(str(item.uid))
    return ldap


def get_portal_logout_time(time):
    add_time = randint(0, 3600)
    return time + timedelta(seconds=add_time)


class Package():
    _instances = set()

    def __init__(self, name, limit):
        self.name = name
        self.limit = int(limit)
        self.users = []
        self._instances.add(ref(self))

    def request(self, user):
        if len(self.users) < self.limit:
            self.users.append(user)
            user.portal_login()
            with open('simulator/output/LM_TMW', 'a') as matlab_log:
                time = datetime.now().strftime("%H:%M:%S")
                matlab_log.write(time + ' (MLM) OUT: "' + self.name +
                                 '" xxx@xxx\n')
            return 'OUT'
        else:
            with open('simulator/output/LM_TMW', 'a') as matlab_log:
                time = datetime.now().strftime("%H:%M:%S")
                matlab_log.write(time + ' (MLM) DENIED: "' + self.name +
                                 '" xxx@xxx\n')
            return 'DENIED'

    @classmethod
    def getinstances(cls):
        dead = set()
        for rf in cls._instances:
            obj = rf()
            if obj is not None:
                yield obj
            else:
                dead.add(rf)
        cls._instances -= dead

    def __repr__(self):
        return str(self.name)


class User():
    _instances = set()

    def __init__(self, uid):
        self.uid = uid
        self.ip = '10.' + str(randint(0, 255)) + '.' + str(randint(0, 255)) +\
                  '.' + str(randint(0, 255))
        self.package = ''
        self.timeout = ''
        self.status = ''
        self.portal_id = ''
        self._instances.add(ref(self))

    def portal_login(self):
        time = datetime.now()
        date = time.strftime("%y-%m-%d %H:%M:%S")
        sub_time = randint(60, 3600)
        login_time = time - timedelta(seconds=sub_time)
        self.portal_id = str(int(mktime(login_time.timetuple())))
        with open('simulator/output/matlab_DB_active.csv', 'a') as \
                portal_active_log:
            portal_active_log.write('"' + self.uid + '","' + self.ip +
                                    '","' + date + '","' + self.portal_id +
                                    '"\n')

    def portal_logout(self):
        time = datetime.now()
        date = time.strftime("%y-%m-%d %H:%M:%S")
        add_time = randint(60, 3600)
        logout_time = time + timedelta(seconds=add_time)
        logout_id = str(int(mktime(logout_time.timetuple())))
        with open('simulator/output/matlab_DB_active.csv', 'r+') as \
                portal_active_log:
            for line in portal_active_log:
                if self.portal_id in line:
                    login_entry = line.replace('\n', '')
                    line = ''
        with open('simulator/output/matlab_DB_archive.csv', 'a') as \
                portal_archive_log:
            portal_archive_log.write(login_entry + '","' + date + '", "' +
                                     logout_id + '"\n')

    def get_package(self, package):
        self.status = package.request(self)
        with open('simulator/output/src_ip_log', 'a') as port_log:
            time = datetime.now().strftime("%H:%M:%S")
            port_log.write(time + '   ' + self.ip + '   27000\n')
        if self.status == 'OUT':
            self.timeout = (datetime.now() +
                            timedelta(seconds=randint(60, 3600))).\
                            strftime("%H:%M:%S")
            self.package = package

    @classmethod
    def getinstances(cls):
        dead = set()
        for rf in cls._instances:
            obj = rf()
            if obj is not None:
                yield obj
            else:
                dead.add(rf)
        cls._instances -= dead

    @classmethod
    def check_expired(cls):
        for obj in cls.getinstances():
            timeout = str(obj.timeout)
            if datetime.now().strftime("%H:%M:%S") > timeout and timeout != '':
                obj.timeout = ''
                with open('simulator/output/src_ip_log', 'a') as port_log:
                    port_log.write(timeout + '   ' + obj.ip + '   27000\n')
                with open('simulator/output/LM_TMW', 'a') as matlab_log:
                    matlab_log.write(timeout + ' (MLM) IN: "' +
                                     str(obj.package) + '" xxx@xxx\n')
                obj.portal_logout()

    def __repr__(self):
        return str(self.uid)

    def __del__(self):
        return


def simulate():
    path_to_lmstat = 'simulator/data/lmstat.txt'
    packages = aggregate_license_info(path_to_lmstat)
    ldap = aggregate_ldap_info()

    while True:
        user = User(choice(ldap))
        user.get_package(packages[choice(range(len(packages)))])
        User.getinstances()
        User.check_expired()
        delay = uniform(1.0, 10.0)
        sleep(delay)


if __name__ == '__main__':
    simulate()
