python manage.py makemigrations appsch
python manage.py makemigrations
python manage.py migrate

gunicorn --bind 8000 --workers 3 Schedule.wsgi