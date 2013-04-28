#-*- coding: utf-8 -*-

import csv
import re
from datetime import datetime
from urlparse import urlparse

import random
import string

from django.core.management.base import BaseCommand
from django.core.validators import email_re

from django.contrib.auth.models import User

fields = (
    'last_name',
    'first_name',
    'second_name',
    'email',
    'phone',
)

class Command(BaseCommand):
    args = '<file.csv>'
    help = 'Import form data from csv file'

    def handle(self, *args, **options):
        reader = csv.DictReader(open(args[0], 'rb'), fields)
        
        csvfile = open('new_' + args[0], 'wb')
        writer = csv.writer(csvfile)

        for row in reader:
            for key in row:
                if isinstance(row[key], str):
                    row[key] = unicode(row[key], 'UTF-8').strip()
                if isinstance(row[key], basestring):
                    row[key] = row[key].strip()

            login = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(6))
            password = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(6))

            user = User(
                username=login,
                first_name=row['first_name'],
                last_name=row['last_name'],
                email=row['email']
            )
            user.set_password(password)
            user.save()

            new_row = [row['last_name'], row['first_name'], row['second_name'], row['email'], row['phone'], login, password]

            new_row = [s.encode('UTF-8') for s in new_row]

            writer.writerow(new_row)
            
        csvfile.close()
            