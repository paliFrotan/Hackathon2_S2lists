import os

os.environ['DJANGO_SECRET_KEY'] = 'dev-only-change-me'
os.environ['DJANGO_DEBUG'] = 'True'  # or 'False'

if os.environ['DJANGO_DEBUG'] == 'False':
    os.environ['DJANGO_ALLOWED_HOSTS'] = 'appname.herokuapp.com'
else:
    os.environ['DJANGO_ALLOWED_HOSTS'] = '127.0.0.1,localhost'
