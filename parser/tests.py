from os import remove
from unittest import mock, TestCase
from .pop_ip import pop_ip
from .pop_ldap import pop_ldap
from .main import process
from .ldap_search import ldap_search


class Test_pop_ip(TestCase):
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


class Test_pop_ldap(TestCase):
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


class Test_processing(TestCase):
    def setUp(self):
        with open('temp_LM_TMW', 'w') as temp:
            temp.write('14:40:31 (MLM) OUT: "Distrib_Computing_Toolbox" \
xxx@xxx\n')
            temp.write('14:40:40 (MLM) OUT: "SimMechanics" xxx@xxx\n')
            temp.write('14:40:49 (MLM) OUT: "Real-Time_Workshop" xxx@xxx\n')
            temp.write('14:40:55 (MLM) DENIED: "MBC_Toolbox" xxx@xxx\n')
            temp.write('14:53:10 (MLM) IN: "SimMechanics" xxx@xxx\n')

        with open('temp_ldap_active', 'w') as temp:
            temp.write('"userid5","10.236.57.15","16-11-13 14:40:31",\
"1479025748"\n')
            temp.write('"userid6","10.251.233.144","16-11-13 14:40:41",\
"1479026935"\n')
            temp.write('"userid7","10.211.63.51","16-11-13 14:40:49",\
"1479027091"\n')
            temp.write('"userid8","10.177.5.173","16-11-13 14:40:55",\
"1479025940"')

        with open('temp_ldap_archive', 'w') as temp:
            temp.write('"userid9","10.9.227.242","16-11-13 14:42:43",\
"1479027417"","16-11-13 14:44:03", "1479031454"\n')
            temp.write('"userid10","10.197.33.124","16-11-13 14:42:29",\
"1479026654"","16-11-13 14:45:14", "1479030776"\n')
            temp.write('"userid11","10.17.152.216","16-11-13 14:46:35",\
"1479027284"","16-11-13 14:48:50", "1479029532"\n')
            temp.write('"userid12","10.144.233.50","16-11-13 14:43:27",\
"1479025833"","16-11-13 14:50:12", "1479031382"')

        with open('temp_ip', 'w') as temp:
            temp.write('14:40:31   10.236.57.15   27000\n')
            temp.write('14:40:41   10.251.233.144   27000\n')
            temp.write('14:40:49   10.211.63.52   27000\n')
            temp.write('14:40:55   10.177.5.173   27000')
            temp.write('14:53:10   10.251.233.144   27000\n')

    def tearDown(self):
        remove('temp_LM_TMW')
        remove('temp_ldap_active')
        remove('temp_ldap_archive')
        remove('temp_ip')

    @mock.patch('parser.main.ldap_search')
    def test_processing(self, mock_search):
        mock_search.return_value = {'employeenumber': 'NA',
                                    'employeetype': 'NA',
                                    'department': 'NA'}
        process('temp_ldap_active', 'temp_ldap_archive', 'temp_LM_TMW',
                'temp_ip')
        expected = [mock.call(i) for i in ("userid5", "NA", "NA",
                                           "userid8")]
        mock_search.assert_has_calls(expected)


@mock.patch('parser.ldap_search.Connection')
class Test_ldap_search(TestCase):
    def test_ldap_search(self, mock_connection):
        mock_connection.search.entries.__len__.return_value = 0
        basedn = 'ou=People,dc=iitb,dc=ac,dc=in'
        attrs = ['employeenumber', 'employeetype']
        query = '(uid=user2)'
        ldap_search('user2')
        expected = [mock.call('ldap.iitb.ac.in', auto_bind=True),
                    mock.call().search(basedn, query, attributes=attrs)]
        mock_connection.assert_has_calls(expected)
