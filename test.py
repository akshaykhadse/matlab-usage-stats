from os import remove
import unittest
from pop_ip import pop_ip
from pop_ldap import pop_ldap


class Test_pop_ip(unittest.TestCase):
    def setUp(self):
        with open('temp_ip', 'w') as temp:
            temp.write('22:18:29   10.107.66.226   27000\n')
            temp.write('20:17:57   10.107.42.121   27000')

    def tearDown(self):
        remove('temp_ip')

    def test_dict_in_pop_ip_output(self):
        time_ip_dict = pop_ip('temp_ip')
        self.assertEqual(time_ip_dict, {'22:18:29': '10.107.66.226',
                         '20:17:57': '10.107.42.121'})

    def test_keys_in_pop_ip_output(self):
        time_stamp_list = set(pop_ip('temp_ip').keys())
        self.assertEqual(time_stamp_list, {'22:18:29', '20:17:57'})


class Test_pop_ldap(unittest.TestCase):
    def setUp(self):
        with open('temp_ldap_archive', 'w') as temp:
            temp.write('"userid1","10.14.47.9","2016-08-09 11:00:44am","1470720\
                       644","2016-08-09 11:01:28am","1470720688"\n')
            temp.write('"userid2","10.177.2.142","2016-08-09 11:02:49am","147\
                       0720769","2016-08-09 11:03:03am","1470720783"')

        with open('temp_ldap_active', 'w') as temp:
            temp.write('"userid3","10.107.63.198","2016-09-27 00:11:17am",\
                       "1474915277"\n')
            temp.write('"userid4","10.107.48.227","2016-10-07 21:41:17pm",\
                       "1475856677"')

    def tearDown(self):
        remove('temp_ldap_active')
        remove('temp_ldap_archive')

    def test_pop_ldap_success(self):
        uid = pop_ldap('10.14.47.9', 'temp_ldap_archive',
                       'temp_ldap_active')
        self.assertEqual(uid, 'userid1')

    def test_pop_ldap_failure(self):
        uid = pop_ldap('10.107.63.197', 'temp_ldap_archive',
                       'temp_ldap_active')
        self.assertEqual(uid, 'NA')


if __name__ == '__main__':
    unittest.main()
