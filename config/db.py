import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SQLITE={
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3')
    }
}
MYSQL = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DBNAME'),
        'HOST': os.environ.get('DBHOST'),
        'USER': os.environ.get('DBUSER'),
        'PASSWORD': os.environ.get('DBPASS'),
    }
}
# hacer dumpdata excluyengo los contenttype
#python manage.py dumpdata --exclude=contenttypes --indent 2 > backup.json