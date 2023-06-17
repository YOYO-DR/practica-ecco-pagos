pip install -r requirements.txt
python manage.py migrate
gunicorn  config.wsgi