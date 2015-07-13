from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = """Create a default admin user if it doesn't exist.
            you SHOULD change the password and the email afterwards!"""

    username = 'admin'
    password = 'admin'
    email = 'root@example.com'

    def handle(self, *args, **options):
        admin = User.objects.filter(username=self.username)
        if not admin:
            user = User(username=self.username)
            user.set_password(self.password)
            user.email = self.email
            user.is_superuser = True
            user.is_staff = True
            user.save()
            print 'User "'+ self.username + '" created'
