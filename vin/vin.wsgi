import os
import sys

activate_this = '/home/jp/vindicate/myenv/bin/activate_this.py'
with open(activate_this) as f:
     code = compile(f.read(), activate_this, 'exec')
     exec(code, dict(__file__=activate_this))

path = '/home/jp/vindicate/vindjango/vin'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'vin.settings'

if not os.getenv("SECRET_KEY"):
    raise Exception("SECRET_KEY not found in environment variables!")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
