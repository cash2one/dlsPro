import os
import sys
sys.path.append("C:/django/DjangoWorkspaces/DlsPro")
sys.stdout = sys.stderr
sys.path.append("C:/django/DjangoWorkspaces/DlsPro/DlsPro")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DlsPro.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()