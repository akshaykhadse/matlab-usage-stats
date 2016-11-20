from django.test import TestCase
from reports.models import LogEntry
from django.test.utils import setup_test_environment
from django.test import Client
setup_test_environment()


class Test_reports_models(TestCase):
    def test_trivial_LogEntry_creation(self):
        entry = LogEntry()
        self.assertTrue(isinstance(entry, LogEntry))
        self.assertEqual(entry.__str__(), entry.out_time + ' ' + entry.package)

    def test_str_metdod_LogEntry(self):
        entry = LogEntry(uid='testuid1', package='sample matlab package',
                         out_time='13:05:57', emp_number='123456789',
                         emp_type='xx', department='DEPT', in_time='22:10:16')
        self.assertTrue(isinstance(entry, LogEntry))
        self.assertEqual(entry.__str__(), entry.out_time + ' ' + entry.package)

    def test_save_objects_LogEntry(self):
        LogEntry.objects.all().delete()
        entry = LogEntry(uid='testuid2')
        entry.save()
        del entry
        self.assertEqual(len(LogEntry.objects.filter(uid='testuid2')), 1)


class Test_reports_views(TestCase):
    def setUp(self):
        entry = LogEntry(uid='testuid1', package='some matlab package',
                         out_time='22:22:22', emp_number='123456789',
                         department='DEPT', emp_type='xx', in_time='23:23:23')
        entry.save()

    def tearDown(self):
        LogEntry.objects.all().delete()

    def test_report_view_status(self):
        c = Client()
        response = c.get('/reports/')
        self.assertEqual(response.status_code, 200)

    def test_report_view_context(self):
        c = Client()
        response = c.get('/reports/')
        self.assertEqual(len(response.context['entry_list']), 1)

    def test_report_view_content(self):
        c = Client()
        response = c.get('/reports/')
        self.assertIn('testuid1', str(response.content))
        self.assertIn('some matlab package', str(response.content))
        self.assertIn('DEPT', str(response.content))


class Test_reports_graph_view(TestCase):
    def setUp(self):
        entry = LogEntry(uid='testuid1', package='matlab package1',
                         out_time='22:22:00', emp_number='123456789',
                         department='DEPT1', emp_type='xx', in_time='23:23:23')
        entry.save()
        entry = LogEntry(uid='testuid2', package='matlab package2',
                         out_time='22:22:01', emp_number='123456781',
                         department='DEPT2', emp_type='xx', in_time='23:23:22')
        entry.save()
        entry = LogEntry(uid='testuid3', package='matlab package2',
                         out_time='22:22:02', emp_number='123456771',
                         department='DEPT2', emp_type='xx', in_time='23:23:25')
        entry.save()
        entry = LogEntry(uid='testuid4', package='matlab package2',
                         out_time='22:22:03', emp_number='123456782',
                         department='DEPT2', emp_type='xx', in_time='23:23:47')
        entry.save()
        entry = LogEntry(uid='testuid5', package='matlab package3',
                         out_time='22:22:04', emp_number='123456783',
                         department='DEPT3', emp_type='xx', in_time='23:23:50')
        entry.save()

    def tearDown(self):
        LogEntry.objects.all().delete()

    def test_graph_view_status(self):
        c = Client()
        response = c.get('/reports/graphs/')
        self.assertEqual(response.status_code, 200)

    def test_graph_view_content(self):
        c = Client()
        response = c.get('/reports/graphs/')
        self.assertIn('matlab package1', str(response.content))
        self.assertIn('matlab package2', str(response.content))
        self.assertIn('matlab package3', str(response.content))
        self.assertIn('DEPT1', str(response.content))
        self.assertIn('DEPT2', str(response.content))
        self.assertIn('DEPT3', str(response.content))

    def test_department_view_form(self):
        c = Client()
        response = c.get('/reports/departments/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('name="department"', str(response.context['form']))

    def test_department_view_graph(self):
        c = Client()
        response = c.post('/reports/departments/', {'department': 'DEPT2'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('name="department"', str(response.context['form']))
        self.assertIn('graph', response.context)

    def test_time_view_form(self):
        c = Client()
        response = c.get('/reports/time/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('name="start_time"', str(response.context['form']))
        self.assertIn('name="end_time"', str(response.context['form']))

    def test_time_view_graph_success(self):
        c = Client()
        response = c.post('/reports/time/', {'start_time': '22:00:00',
                                             'end_time': '23:00:00'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', str(response.context))
        self.assertIn('graph', response.context)

    def test_time_view_graph_failure(self):
        c = Client()
        response = c.post('/reports/time/', {'start_time': '00:00:00',
                                             'end_time': '01:00:00'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', str(response.context))
        self.assertNotIn('graph', response.context)
