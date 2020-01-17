from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand

from django_quickbooks import get_realm_model
from django_quickbooks.models import create_qwc

Realm = get_realm_model()


class Command(BaseCommand):
    help = "Create QWC file for a realm."

    requires_system_checks = False

    def add_arguments(self, parser):
        parser.add_argument(
            '--realm_id', '-r', default='', dest='realm',
            help='Create a realm for a realm if given or ask for a realm',
        )
        parser.add_argument(
            '--file', '-f', default='',
            help='Create a file with a given path',
        )

    def handle(self, *app_labels, **options):

        if options.get('realm'):
            realm_id = options['realm']
        else:
            while True:
                realm_id = input("Enter Realm id ('?' to list realms): ")
                if realm_id == '?':
                    print('\n'.join(["%s - %s" % (realm.pk, realm.name) for realm in Realm.objects.all()]))
                elif not realm_id:
                    exit(-1)
                else:
                    break
        try:
            realm = Realm.objects.get(pk=realm_id.strip())
        except ObjectDoesNotExist:
            exit('Invalid or Not existing realm id')

        app_name = input('app_name: Default[Weltlink TMS] ') or 'Weltlink TMS'
        app_id = input('app_id: Default[] ') or ''
        app_url = input('app_url: Default[http://localhost:8000/qwc/] ') or 'http://localhost:8000/qwc/'
        app_desc = input('app_desc: Default[Weltlink TMS Description] ') or 'Weltlink TMS Description'
        app_support = input(
            'app_support: Default[http://localhost:8000/qwc/support/] ') or 'http://localhost:8000/qwc/support/'
        owner_id = input(
            'owner_id: Default[{55a9fd50-79e9-44e4-8fef-98411c2e8785}] ') or '{55a9fd50-79e9-44e4-8fef-98411c2e8785}'
        file_id = input(
            'file_id: Default[{30830c9c-c1b7-4773-a12d-b193437a8fef}] ') or '{30830c9c-c1b7-4773-a12d-b193437a8fef}'
        qb_type = input('qb_type: Default[QBFS] ') or 'QBFS'
        schedule_n_minutes = input('schedule_n_minutes: Default[15] ') or '15'

        qwc = create_qwc(
            realm=realm, app_name=app_name, app_id=app_id,
            app_url=app_url, app_desc=app_desc, app_support=app_support,
            owner_id=owner_id, file_id=file_id, qb_type=qb_type, schedule_n_minutes=schedule_n_minutes
        ).decode('utf-8')

        if options['file']:
            try:
                with open(options['file'], 'w') as f:
                    f.write(qwc)
                    f.close()
            except IOError:
                print('Error in file writing')
                exit(-1)
            print('QWC is written to file')
        else:
            print(qwc)
            print('QWC is written to console successfully')
