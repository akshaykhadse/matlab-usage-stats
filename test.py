from os import remove
import unittest
from pop_ip import pop_ip


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


if __name__ == '__main__':
    unittest.main()
