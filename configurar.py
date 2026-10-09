"""Asistente local: conectar MySQL, migrar y ejecutar Django."""
import getpass
import json
import os
from pathlib import Path
import subprocess
import sys
import MySQLdb

BASE_DIR = Path(__file__).resolve().parent
os.chdir(BASE_DIR)
config_path = BASE_DIR / 'config.local.json'


def main():
    config = json.loads(config_path.read_text(encoding='utf-8')) if config_path.exists() else {
        'NAME': 'django_api',
        'USER': input('Usuario de MySQL [root]: ').strip() or 'root',
        'PASSWORD': getpass.getpass('Contraseña de MySQL (no se muestra): '),
        'HOST': '127.0.0.1', 'PORT': '3306',
    }
    connection = MySQLdb.connect(host=config['HOST'], port=int(config['PORT']), user=config['USER'], passwd=config['PASSWORD'])
    with connection.cursor() as cursor:
        cursor.execute('CREATE DATABASE IF NOT EXISTS `django_api` CHARACTER SET utf8mb4')
    connection.close()
    config['NAME'] = 'django_api'
    config_path.write_text(json.dumps(config, indent=2), encoding='utf-8')
    os.environ.pop('DJANGO_USE_SQLITE', None)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tienda_online.settings')
    import django
    django.setup()
    from django.core.management import call_command
    from django.contrib.auth import get_user_model
    call_command('migrate')
    if not get_user_model().objects.filter(is_superuser=True).exists():
        print('Crea el usuario administrador de Django:')
        call_command('createsuperuser')
    print('API: http://127.0.0.1:8000/api/v1/')
    print('Administrador: http://127.0.0.1:8000/admin/')
    return subprocess.call([sys.executable, 'manage.py', 'runserver', '127.0.0.1:8000'])


if __name__ == '__main__':
    try:
        sys.exit(main())
    except MySQLdb.Error as error:
        print(f'No se pudo conectar o preparar MySQL: {error}')
        print('Revisa el usuario y la contraseña. Si guardaste una configuración incorrecta, edita config.local.json.')
        sys.exit(1)
