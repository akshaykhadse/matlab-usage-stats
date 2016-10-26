import os
import unittest
from pop_ip import pop_ip


class Test_pop_ip(unittest.TestCase):
    def setUp(self):
        with open('temp_ip', 'w') as temp:
            temp.write('1476463709   10.107.66.226   27000\n')
            temp.write('1476456477   10.107.42.121   27000')

    def tearDown(self):
        os.remove('temp_ip')

    def test_pop_ip_func(self):
        time_ip_dict = pop_ip('temp_ip')
        print(time_ip_dict)
        self.assertEqual(time_ip_dict, {'22:18:29': '10.107.66.226',
                         '20:17:57': '10.107.42.121'})


class Test_(unittest.TestCase):
    def setUp(self):
        with open('temp_ip', 'w') as temp:
            temp.write('1476463709   10.107.66.226   27000\n')
            temp.write('1476456477   10.107.42.121   27000')

    def tearDown(self):
        os.remove('temp_ip')

    def test_pop_ip(self):
        time_ip_dict = pop_ip('temp_ip')
        print(time_ip_dict)
        self.assertEqual(time_ip_dict, {'22:18:29': '10.107.66.226',
                         '20:17:57': '10.107.42.121'})


if __name__ == '__main__':
    unittest.main()
