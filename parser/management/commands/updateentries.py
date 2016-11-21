from django.core.management import BaseCommand
from parser.main import process


class Command(BaseCommand):
    help = "Update Logs"

    def handle(self, *args, **options):
        self.stdout.write("Updating Entries")
        self.stdout.write("Please Wait")
        active_csv = 'data/matlab_DB_active.csv'
        archive_csv = 'data/matlab_DB_archive.csv'
        matlab_log = 'data/LM_TMW.log'
        port_activity_log = 'data/src_ip_log'
        process(active_csv, archive_csv, matlab_log, port_activity_log)
        self.stdout.write("Done Updating Entries")
