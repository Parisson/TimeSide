from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class Command(BaseCommand):
    help = """Create a default admin user if it doesn't exist.
            you SHOULD change the password, the email and the token afterwards!"""

    username = 'admin'
    password = 'admin'
    email = 'root@example.com'
    token = 'Dummy_Token'
    
    def handle(self, *args, **options):
        admin = User.objects.filter(username=self.username)
        if not admin:
            user = User.objects.create_user(username=self.username,
                                            email=self.email,
                                            password=self.password)
                                            
            user.is_superuser = True
            user.is_staff = True
            user.save()
            print 'User "%s" created"' % self.username
            Token.objects.create(user=user, key=self.token)
            print 'Token created for User "%s"' % self.username
